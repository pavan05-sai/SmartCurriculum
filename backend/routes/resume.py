# SmartCurriculum - Resume Routes
# Handles skill mapping for resume generation

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from models.user import User
from models.skill import Skill, get_skill_category
from ai_engine.llm_generator import LLMGenerator

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
    
    # Build query
    query = Skill.query.filter_by(user_id=user_id)
    
    # Apply filters
    category = request.args.get('category')
    if category:
        query = query.filter_by(category=category)
    
    show_on_resume = request.args.get('show_on_resume')
    if show_on_resume is not None:
        query = query.filter_by(show_on_resume=show_on_resume.lower() == 'true')
    
    skills = query.order_by(Skill.proficiency_score.desc()).all()
    
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


@resume_bp.route('/skills/<int:skill_id>', methods=['PUT'])
@jwt_required()
def update_skill(skill_id):
    """
    Update a skill (e.g., edit resume bullet, toggle visibility).
    
    Expected JSON body:
    {
        "resume_bullet": "Custom bullet point text",
        "show_on_resume": true,
        "level": "advanced"
    }
    """
    user_id = get_jwt_identity()
    
    skill = Skill.query.filter_by(id=skill_id, user_id=user_id).first()
    
    if not skill:
        return jsonify({
            'error': 'Not Found',
            'message': 'Skill not found'
        }), 404
    
    data = request.get_json()
    
    # Update fields
    if 'resume_bullet' in data:
        skill.resume_bullet = data['resume_bullet']
    if 'show_on_resume' in data:
        skill.show_on_resume = data['show_on_resume']
    if 'level' in data:
        skill.level = data['level']
    if 'proficiency_score' in data:
        skill.update_proficiency(data['proficiency_score'])
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Skill updated',
            'skill': skill.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
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
    data = request.get_json()
    
    if not data.get('name'):
        return jsonify({
            'error': 'Validation Error',
            'message': 'Skill name is required'
        }), 400
    
    # Check if skill already exists
    existing = Skill.query.filter_by(
        user_id=user_id,
        name=data['name']
    ).first()
    
    if existing:
        return jsonify({
            'error': 'Already Exists',
            'message': 'You already have this skill'
        }), 409
    
    try:
        skill = Skill(
            user_id=user_id,
            name=data['name'],
            category=get_skill_category(data['name']),
            level=data.get('level', 'beginner'),
            source=data.get('source', 'self_declared')
        )
        
        # Set initial proficiency based on level
        level_scores = {
            'beginner': 25,
            'intermediate': 50,
            'advanced': 75,
            'expert': 95
        }
        skill.proficiency_score = level_scores.get(skill.level, 25)
        
        db.session.add(skill)
        db.session.commit()
        
        return jsonify({
            'message': 'Skill added',
            'skill': skill.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Add Failed',
            'message': str(e)
        }), 500


@resume_bp.route('/skills/<int:skill_id>', methods=['DELETE'])
@jwt_required()
def delete_skill(skill_id):
    """
    Delete a skill from the user's profile.
    """
    user_id = get_jwt_identity()
    
    skill = Skill.query.filter_by(id=skill_id, user_id=user_id).first()
    
    if not skill:
        return jsonify({
            'error': 'Not Found',
            'message': 'Skill not found'
        }), 404
    
    try:
        db.session.delete(skill)
        db.session.commit()
        return jsonify({
            'message': 'Skill deleted'
        }), 200
    except Exception as e:
        db.session.rollback()
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
        "skill_ids": [1, 2, 3],  // Optional, generates for all if not provided
        "style": "impactful"  // impactful, technical, concise
    }
    """
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    
    # Get skills
    if data.get('skill_ids'):
        skills = Skill.query.filter(
            Skill.id.in_(data['skill_ids']),
            Skill.user_id == user_id
        ).all()
    else:
        skills = Skill.query.filter_by(
            user_id=user_id,
            show_on_resume=True
        ).all()
    
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
            
            skill.resume_bullet = bullet
            generated_bullets.append({
                'skill_id': skill.id,
                'skill_name': skill.name,
                'bullet': bullet
            })
        
        db.session.commit()
        
        return jsonify({
            'message': 'Resume bullets generated',
            'bullets': generated_bullets
        }), 200
        
    except Exception as e:
        db.session.rollback()
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
    user = User.query.get(user_id)
    
    # Get all resume-visible skills
    skills = Skill.query.filter_by(
        user_id=user_id,
        show_on_resume=True
    ).order_by(Skill.proficiency_score.desc()).all()
    
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
    skill_names = [s.name for s in skills[:10]]  # Top 10 skills
    summary_line = ', '.join(skill_names)
    
    return jsonify({
        'user_name': user.name if user else 'User',
        'summary': f"Proficient in: {summary_line}",
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
    data = request.get_json()
    
    if not data.get('job_description'):
        return jsonify({
            'error': 'Validation Error',
            'message': 'job_description is required'
        }), 400
    
    # Get user's skills
    skills = Skill.query.filter_by(user_id=user_id).all()
    user_skills = {s.name.lower(): s for s in skills}
    
    try:
        from ai_engine.nlp_analyzer import NLPAnalyzer
        nlp = NLPAnalyzer()
        
        # Analyze job description
        job_analysis = nlp.analyze_job_description(data['job_description'])
        required_skills = job_analysis.get('required_skills', [])
        
        # Match skills
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
        return jsonify({
            'error': 'Analysis Failed',
            'message': str(e)
        }), 500
