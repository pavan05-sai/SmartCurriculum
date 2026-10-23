# SmartCurriculum - AI Routes (MongoDB)
# Handles AI-powered features: skill gap analysis, content generation, and syllabus/job parsing

import logging
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import get_db
from models.user import User
from models.curriculum import Curriculum, Topic
from models.skill import Skill
from ai_engine.recommender import CurriculumRecommender
from ai_engine.nlp_analyzer import NLPAnalyzer
from ai_engine.llm_generator import LLMGenerator

logger = logging.getLogger(__name__)

# Create blueprint for AI routes
ai_bp = Blueprint('ai', __name__)


@ai_bp.route('/skill-gap', methods=['POST'])
@jwt_required()
def analyze_skill_gap():
    """
    Analyze skill gaps based on user profile and target role.

    Expected JSON body:
    {
        "target_role": "Full Stack Developer",
        "job_description": "Optional job description text..."
    }
    """
    user_id = get_jwt_identity()
    db = get_db()
    user = User.find_by_id(db, user_id)

    if not user:
        return jsonify({
            'error': 'Not Found',
            'message': 'User not found'
        }), 404

    data = request.get_json() or {}

    try:
        recommender = CurriculumRecommender()

        # Get user's current skills from MongoDB
        user_skills = Skill.find_by_user(db, user_id=user_id)
        current_skills = [s.name for s in user_skills]

        target_role = data.get('target_role') or user.career_goal or 'Full Stack Developer'

        skill_analysis = recommender.analyze_skill_gap(
            user=user,
            target_role=target_role,
            current_skills=current_skills,
            job_description=data.get('job_description')
        )

        return jsonify({
            'skill_analysis': skill_analysis
        }), 200

    except Exception as e:
        logger.error(f"Error in skill-gap analysis: {e}")
        return jsonify({
            'error': 'Analysis Failed',
            'message': str(e)
        }), 500


@ai_bp.route('/generate-notes', methods=['POST'])
@jwt_required()
def generate_notes():
    """
    Generate learning notes for a topic using LLM.

    Expected JSON body:
    {
        "topic_id": "653...",
        "or"
        "topic_title": "Introduction to Python",
        "detail_level": "comprehensive"  // basic, intermediate, comprehensive
    }
    """
    user_id = get_jwt_identity()
    db = get_db()
    data = request.get_json() or {}

    topic_title = data.get('topic_title')
    topic_description = ""
    topic_skills = []

    # If topic_id provided, look up topic from MongoDB and verify ownership
    if data.get('topic_id'):
        topic = Topic.find_by_id(db, str(data['topic_id']))
        if not topic:
            return jsonify({
                'error': 'Not Found',
                'message': 'Topic not found'
            }), 404

        # Verify curriculum belongs to this user
        curriculum = Curriculum.find_one_by_user_and_id(db, topic.curriculum_id, user_id)
        if not curriculum:
            return jsonify({
                'error': 'Forbidden',
                'message': 'You do not have access to this topic'
            }), 403

        topic_title = topic.title
        topic_description = topic.description
        topic_skills = topic.skills_gained

    if not topic_title:
        return jsonify({
            'error': 'Validation Error',
            'message': 'topic_id or topic_title is required'
        }), 400

    try:
        llm = LLMGenerator()
        notes = llm.generate_notes(
            topic=topic_title,
            detail_level=data.get('detail_level', 'intermediate'),
            context={
                'description': topic_description,
                'skills': topic_skills
            }
        )

        return jsonify({
            'topic': topic_title,
            'notes': notes
        }), 200

    except Exception as e:
        logger.error(f"Error generating notes: {e}")
        return jsonify({
            'error': 'Generation Failed',
            'message': str(e)
        }), 500


@ai_bp.route('/generate-mcqs', methods=['POST'])
@jwt_required()
def generate_mcqs():
    """
    Generate MCQs for a topic using LLM.

    Expected JSON body:
    {
        "topic_id": "653...",
        "or"
        "topic_title": "Introduction to Python",
        "count": 5,
        "difficulty": "intermediate"
    }
    """
    user_id = get_jwt_identity()
    db = get_db()
    data = request.get_json() or {}

    topic_title = data.get('topic_title')
    topic_description = ""

    if data.get('topic_id'):
        topic = Topic.find_by_id(db, str(data['topic_id']))
        if not topic:
            return jsonify({
                'error': 'Not Found',
                'message': 'Topic not found'
            }), 404

        curriculum = Curriculum.find_one_by_user_and_id(db, topic.curriculum_id, user_id)
        if not curriculum:
            return jsonify({
                'error': 'Forbidden',
                'message': 'You do not have access to this topic'
            }), 403

        topic_title = topic.title
        topic_description = topic.description

    if not topic_title:
        return jsonify({
            'error': 'Validation Error',
            'message': 'topic_id or topic_title is required'
        }), 400

    try:
        llm = LLMGenerator()
        count = min(int(data.get('count', 5)), 10)
        difficulty = data.get('difficulty', 'intermediate')

        mcqs = llm.generate_mcqs(
            topic=topic_title,
            count=count,
            difficulty=difficulty,
            context={'description': topic_description}
        )

        return jsonify({
            'topic': topic_title,
            'mcqs': mcqs
        }), 200

    except Exception as e:
        logger.error(f"Error generating MCQs: {e}")
        return jsonify({
            'error': 'Generation Failed',
            'message': str(e)
        }), 500


@ai_bp.route('/generate-projects', methods=['POST'])
@jwt_required()
def generate_projects():
    """
    Generate project ideas for a topic using LLM.

    Expected JSON body:
    {
        "topic_id": "653...",
        "or"
        "topic_title": "Web Development with React",
        "count": 3,
        "difficulty": "intermediate"
    }
    """
    user_id = get_jwt_identity()
    db = get_db()
    data = request.get_json() or {}

    topic_title = data.get('topic_title')
    if data.get('topic_id'):
        topic = Topic.find_by_id(db, str(data['topic_id']))
        if not topic:
            return jsonify({
                'error': 'Not Found',
                'message': 'Topic not found'
            }), 404

        curriculum = Curriculum.find_one_by_user_and_id(db, topic.curriculum_id, user_id)
        if not curriculum:
            return jsonify({
                'error': 'Forbidden',
                'message': 'You do not have access to this topic'
            }), 403

        topic_title = topic.title

    if not topic_title:
        return jsonify({
            'error': 'Validation Error',
            'message': 'topic_id or topic_title is required'
        }), 400

    try:
        llm = LLMGenerator()
        projects = llm.generate_projects(
            topic=topic_title,
            count=min(int(data.get('count', 3)), 5),
            difficulty=data.get('difficulty', 'intermediate')
        )

        return jsonify({
            'topic': topic_title,
            'projects': projects
        }), 200

    except Exception as e:
        logger.error(f"Error generating projects: {e}")
        return jsonify({
            'error': 'Generation Failed',
            'message': str(e)
        }), 500


@ai_bp.route('/generate-coding-problems', methods=['POST'])
@jwt_required()
def generate_coding_problems():
    """
    Generate coding problems for a topic using LLM.

    Expected JSON body:
    {
        "topic_title": "Data Structures - Arrays",
        "count": 3,
        "difficulty": "intermediate",
        "language": "python"
    }
    """
    data = request.get_json() or {}

    if not data.get('topic_title'):
        return jsonify({
            'error': 'Validation Error',
            'message': 'topic_title is required'
        }), 400

    try:
        llm = LLMGenerator()
        problems = llm.generate_coding_problems(
            topic=data['topic_title'],
            count=min(int(data.get('count', 3)), 5),
            difficulty=data.get('difficulty', 'intermediate'),
            language=data.get('language', 'python')
        )

        return jsonify({
            'topic': data['topic_title'],
            'problems': problems
        }), 200

    except Exception as e:
        logger.error(f"Error generating coding problems: {e}")
        return jsonify({
            'error': 'Generation Failed',
            'message': str(e)
        }), 500


@ai_bp.route('/analyze-syllabus', methods=['POST'])
@jwt_required()
def analyze_syllabus():
    """
    Analyze syllabus text using NLP to extract topics and skills.

    Expected JSON body:
    {
        "syllabus_text": "Course syllabus content..."
    }
    """
    data = request.get_json() or {}

    if not data.get('syllabus_text'):
        return jsonify({
            'error': 'Validation Error',
            'message': 'syllabus_text is required'
        }), 400

    try:
        nlp = NLPAnalyzer()
        analysis = nlp.analyze_syllabus(data['syllabus_text'])

        return jsonify({
            'analysis': analysis
        }), 200

    except Exception as e:
        logger.error(f"Error analyzing syllabus: {e}")
        return jsonify({
            'error': 'Analysis Failed',
            'message': str(e)
        }), 500


@ai_bp.route('/analyze-job', methods=['POST'])
@jwt_required()
def analyze_job_description():
    """
    Analyze job description to extract required skills.

    Expected JSON body:
    {
        "job_description": "Job posting text..."
    }
    """
    data = request.get_json() or {}

    if not data.get('job_description'):
        return jsonify({
            'error': 'Validation Error',
            'message': 'job_description is required'
        }), 400

    try:
        nlp = NLPAnalyzer()
        analysis = nlp.analyze_job_description(data['job_description'])

        return jsonify({
            'analysis': analysis
        }), 200

    except Exception as e:
        logger.error(f"Error analyzing job description: {e}")
        return jsonify({
            'error': 'Analysis Failed',
            'message': str(e)
        }), 500


@ai_bp.route('/adaptive-update', methods=['POST'])
@jwt_required()
def get_adaptive_update():
    """
    Get adaptive curriculum updates based on user performance.
    """
    user_id = get_jwt_identity()
    db = get_db()
    user = User.find_by_id(db, user_id)

    if not user:
        return jsonify({
            'error': 'Not Found',
            'message': 'User not found'
        }), 404

    try:
        recommender = CurriculumRecommender()

        # Gather user's active curricula and their topics
        curricula = Curriculum.find_by_user(db, user_id=user_id, status='active')
        topics = []
        for c in curricula:
            topics.extend(Topic.find_by_curriculum(db, c.id))

        recommendations = recommender.get_adaptive_recommendations(
            user=user,
            progress_records=topics
        )

        return jsonify({
            'recommendations': recommendations
        }), 200

    except Exception as e:
        logger.error(f"Error getting adaptive recommendations: {e}")
        return jsonify({
            'error': 'Analysis Failed',
            'message': str(e)
        }), 500
