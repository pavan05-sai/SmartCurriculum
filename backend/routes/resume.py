# SmartCurriculum - Resume Routes (MongoDB)
# Handles skill mapping for resume generation

import logging
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import get_db
from models.user import User
from models.skill import Skill, get_skill_category
from ai_engine.llm_generator import LLMGenerator

logger = logging.getLogger(__name__)

# Create blueprint for resume routes
resume_bp = Blueprint('resume', __name__)


@resume_bp.route('/skills', methods=['GET'])
@jwt_required()
def get_skills():
    """
    Get all skills for the current user, formatted for resume.

    Query params:
    - category: Filter by category
    - show_on_resume: Filter by resume visibility (true/false)
    """
    user_id = get_jwt_identity()
    db = get_db()

    category = request.args.get('category')
    show_on_resume_param = request.args.get('show_on_resume')
    show_on_resume = None
    if show_on_resume_param is not None:
        show_on_resume = show_on_resume_param.lower() == 'true'

    skills = Skill.find_by_user(
        db,
        user_id=user_id,
        category=category,
        show_on_resume=show_on_resume
    )

    # Group by category
    skills_by_category = {}
    for skill in skills:
        cat = skill.category or 'other'
        if cat not in skills_by_category:
            skills_by_category[cat] = []
        skills_by_category[cat].append(skill.to_dict())

    return jsonify({
        'skills': [s.to_dict() for s in skills],
        'skills_by_category': skills_by_category,
        'total': len(skills)
    }), 200


@resume_bp.route('/skills/<skill_id>', methods=['PUT'])
@jwt_required()
def update_skill(skill_id):
    """
    Update a skill (e.g., edit resume bullet, toggle visibility).

    Expected JSON body:
    {
        "resume_bullet": "Custom bullet point text",
        "show_on_resume": true,
        "level": "advanced",
        "proficiency_score": 85
    }
    """
    user_id = get_jwt_identity()
    db = get_db()

    skill = Skill.find_by_user_and_id(db, user_id=user_id, skill_id=skill_id)
    if not skill:
        return jsonify({
            'error': 'Not Found',
            'message': 'Skill not found'
        }), 404

    data = request.get_json() or {}
    updates = {}

    if 'resume_bullet' in data:
        updates['resume_bullet'] = data['resume_bullet']
    if 'show_on_resume' in data:
        updates['show_on_resume'] = bool(data['show_on_resume'])
    if 'level' in data:
        updates['level'] = data['level']
    if 'proficiency_score' in data:
        score = int(data['proficiency_score'])
        updates['proficiency_score'] = score
        if 'level' not in data:
            if score >= 90:
                updates['level'] = 'expert'
            elif score >= 70:
                updates['level'] = 'advanced'
            elif score >= 40:
                updates['level'] = 'intermediate'
            else:
                updates['level'] = 'beginner'

    try:
        if updates:
            skill.update(updates)
        return jsonify({
            'message': 'Skill updated',
            'skill': skill.to_dict()
        }), 200
    except Exception as e:
        logger.error(f"Error updating skill {skill_id}: {e}")
        return jsonify({
            'error': 'Update Failed',
            'message': str(e)
        }), 500


@resume_bp.route('/skills', methods=['POST'])
@jwt_required()
def add_skill():
    """
    Manually add a skill to the user's profile.

    Expected JSON body:
    {
        "name": "Python",
        "level": "intermediate",
        "source": "self_declared"
    }
    """
    user_id = get_jwt_identity()
    db = get_db()
    data = request.get_json() or {}

    skill_name = data.get('name', '').strip()
    if not skill_name:
        return jsonify({
            'error': 'Validation Error',
            'message': 'Skill name is required'
        }), 400

    # Check if skill already exists
    existing = Skill.find_by_user_and_name(db, user_id=user_id, name=skill_name)
    if existing:
        return jsonify({
            'error': 'Already Exists',
            'message': 'You already have this skill in your profile'
        }), 409

    level = data.get('level', 'beginner')
    level_scores = {
        'beginner': 25,
        'intermediate': 50,
        'advanced': 75,
        'expert': 95
    }
    proficiency_score = data.get('proficiency_score', level_scores.get(level, 25))

    try:
        skill = Skill.create(
            db,
            user_id=user_id,
            name=skill_name,
            category=data.get('category', get_skill_category(skill_name)),
            level=level,
            proficiency_score=proficiency_score,
            source=data.get('source', 'self_declared')
        )

        return jsonify({
            'message': 'Skill added successfully',
            'skill': skill.to_dict()
        }), 201

    except Exception as e:
        logger.error(f"Error adding skill: {e}")
        return jsonify({
            'error': 'Add Failed',
            'message': str(e)
        }), 500


@resume_bp.route('/skills/<skill_id>', methods=['DELETE'])
@jwt_required()
def delete_skill(skill_id):
    """
    Delete a skill from the user's profile.
    """
    user_id = get_jwt_identity()
    db = get_db()

    skill = Skill.find_by_user_and_id(db, user_id=user_id, skill_id=skill_id)
    if not skill:
        return jsonify({
            'error': 'Not Found',
            'message': 'Skill not found'
        }), 404

    try:
        skill.delete()
        return jsonify({
            'message': 'Skill deleted successfully'
        }), 200
    except Exception as e:
        logger.error(f"Error deleting skill {skill_id}: {e}")
        return jsonify({
            'error': 'Delete Failed',
            'message': str(e)
        }), 500


@resume_bp.route('/generate-bullets', methods=['POST'])
@jwt_required()
def generate_resume_bullets():
    """
    Generate AI-powered resume bullet points for skills.

    Expected JSON body:
    {
        "skill_ids": ["653..."],  // Optional, generates for all if not provided
        "style": "impactful"      // impactful, technical, concise
    }
    """
    user_id = get_jwt_identity()
    db = get_db()
    data = request.get_json() or {}

    # Get skills
    if data.get('skill_ids'):
        skills = Skill.find_by_ids_and_user(db, user_id=user_id, skill_ids=data['skill_ids'])
    else:
        skills = Skill.find_by_user(db, user_id=user_id, show_on_resume=True)

    if not skills:
        return jsonify({
            'error': 'No Skills',
            'message': 'No skills found to generate bullets for'
        }), 404

    try:
        llm = LLMGenerator()
        style = data.get('style', 'impactful')

        generated_bullets = []
        for skill in skills:
            bullet = llm.generate_resume_bullet(
                skill_name=skill.name,
                skill_level=skill.level,
                style=style
            )

            skill.update({'resume_bullet': bullet})
            generated_bullets.append({
                'skill_id': skill.id,
                'skill_name': skill.name,
                'bullet': bullet
            })

        return jsonify({
            'message': 'Resume bullets generated',
            'bullets': generated_bullets
        }), 200

    except Exception as e:
        logger.error(f"Error generating resume bullets: {e}")
        return jsonify({
            'error': 'Generation Failed',
            'message': str(e)
        }), 500


@resume_bp.route('/export', methods=['GET'])
@jwt_required()
def export_skills_for_resume():
    """
    Export skills in a format ready for resume.
    Groups skills by category with bullet points.
    """
    user_id = get_jwt_identity()
    db = get_db()

    user = User.find_by_id(db, user_id)
    skills = Skill.find_by_user(db, user_id=user_id, show_on_resume=True)

    # Group by category
    resume_sections = {}
    for skill in skills:
        cat = skill.category or 'other'
        cat_title = cat.replace('_', ' ').title()

        if cat_title not in resume_sections:
            resume_sections[cat_title] = {
                'skills': [],
                'bullets': []
            }

        resume_sections[cat_title]['skills'].append(skill.name)
        if skill.resume_bullet:
            resume_sections[cat_title]['bullets'].append(skill.resume_bullet)

    # Create summary line
    skill_names = [s.name for s in skills[:10]]
    summary_line = ', '.join(skill_names)

    return jsonify({
        'user_name': user.name if user else 'User',
        'summary': f"Proficient in: {summary_line}" if summary_line else "No skills listed yet",
        'sections': resume_sections,
        'total_skills': len(skills)
    }), 200


@resume_bp.route('/match-job', methods=['POST'])
@jwt_required()
def match_skills_to_job():
    """
    Match user's skills to a job description.

    Expected JSON body:
    {
        "job_description": "Job posting text..."
    }
    """
    user_id = get_jwt_identity()
    db = get_db()
    data = request.get_json() or {}

    job_description = data.get('job_description', '').strip()
    if not job_description:
        return jsonify({
            'error': 'Validation Error',
            'message': 'job_description is required'
        }), 400

    skills = Skill.find_by_user(db, user_id=user_id)
    user_skills = {s.name.lower(): s for s in skills}

    try:
        from ai_engine.nlp_analyzer import NLPAnalyzer
        nlp = NLPAnalyzer()

        job_analysis = nlp.analyze_job_description(job_description)
        required_skills = job_analysis.get('required_skills', [])

        matched = []
        missing = []

        for req_skill in required_skills:
            skill_lower = req_skill.lower()
            if skill_lower in user_skills or any(skill_lower in us for us in user_skills.keys()):
                matched.append(req_skill)
            else:
                missing.append(req_skill)

        match_percentage = (len(matched) / len(required_skills) * 100) if required_skills else 0

        return jsonify({
            'match_percentage': round(match_percentage, 1),
            'matched_skills': matched,
            'missing_skills': missing,
            'total_required': len(required_skills),
            'recommendation': 'Great match!' if match_percentage >= 70 else 'Consider learning the missing skills'
        }), 200

    except Exception as e:
        logger.error(f"Error matching skills to job: {e}")
        return jsonify({
            'error': 'Analysis Failed',
            'message': str(e)
        }), 500
