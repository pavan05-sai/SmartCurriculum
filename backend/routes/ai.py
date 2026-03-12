# SmartCurriculum - AI Routes
# Handles AI-powered features: skill gap analysis, content generation

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from models.user import User
from models.curriculum import Curriculum, Topic
from ai_engine.recommender import CurriculumRecommender
from ai_engine.nlp_analyzer import NLPAnalyzer
from ai_engine.llm_generator import LLMGenerator

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
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({
            'error': 'Not Found',
            'message': 'User not found'
        }), 404
    
    data = request.get_json() or {}
    
    try:
        recommender = CurriculumRecommender()
        
        # Get user's current skills
        from models.skill import Skill
        user_skills = Skill.query.filter_by(user_id=user_id).all()
        current_skills = [s.name for s in user_skills]
        
        # Analyze skill gap
        skill_analysis = recommender.analyze_skill_gap(
            user=user,
            target_role=data.get('target_role', user.career_goal),
            current_skills=current_skills,
            job_description=data.get('job_description')
        )
        
        return jsonify({
            'skill_analysis': skill_analysis
        }), 200
        
    except Exception as e:
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
        "topic_id": 1,
        "or"
        "topic_title": "Introduction to Python",
        "detail_level": "comprehensive"  // basic, intermediate, comprehensive
    }
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    
    topic_title = data.get('topic_title')
    
    # If topic_id provided, get topic from database
    if data.get('topic_id'):
        topic = Topic.query.join(Curriculum).filter(
            Topic.id == data['topic_id'],
            Curriculum.user_id == user_id
        ).first()
        
        if not topic:
            return jsonify({
                'error': 'Not Found',
                'message': 'Topic not found'
            }), 404
        
        topic_title = topic.title
    
    if not topic_title:
        return jsonify({
            'error': 'Validation Error',
            'message': 'topic_id or topic_title is required'
        }), 400
    
    try:
        llm = LLMGenerator()
        
        notes = llm.generate_notes(
            topic=topic_title,
            detail_level=data.get('detail_level', 'intermediate')
        )
        
        return jsonify({
            'topic': topic_title,
            'notes': notes
        }), 200
        
    except Exception as e:
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
        "topic_id": 1,
        "or"
        "topic_title": "Introduction to Python",
        "count": 5,
        "difficulty": "intermediate"
    }
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    
    topic_title = data.get('topic_title')
    
    # If topic_id provided, get topic from database
    if data.get('topic_id'):
        topic = Topic.query.join(Curriculum).filter(
            Topic.id == data['topic_id'],
            Curriculum.user_id == user_id
        ).first()
        
        if not topic:
            return jsonify({
                'error': 'Not Found',
                'message': 'Topic not found'
            }), 404
        
        topic_title = topic.title
    
    if not topic_title:
        return jsonify({
            'error': 'Validation Error',
            'message': 'topic_id or topic_title is required'
        }), 400
    
    try:
        llm = LLMGenerator()
        
        mcqs = llm.generate_mcqs(
            topic=topic_title,
            count=data.get('count', 5),
            difficulty=data.get('difficulty', 'intermediate')
        )
        
        return jsonify({
            'topic': topic_title,
            'mcqs': mcqs
        }), 200
        
    except Exception as e:
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
        "topic_id": 1,
        "or"
        "topic_title": "Web Development with React",
        "count": 3,
        "difficulty": "intermediate"
    }
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    
    topic_title = data.get('topic_title')
    
    # If topic_id provided, get topic from database
    if data.get('topic_id'):
        topic = Topic.query.join(Curriculum).filter(
            Topic.id == data['topic_id'],
            Curriculum.user_id == user_id
        ).first()
        
        if not topic:
            return jsonify({
                'error': 'Not Found',
                'message': 'Topic not found'
            }), 404
        
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
            count=data.get('count', 3),
            difficulty=data.get('difficulty', 'intermediate')
        )
        
        return jsonify({
            'topic': topic_title,
            'projects': projects
        }), 200
        
    except Exception as e:
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
    data = request.get_json()
    
    if not data.get('topic_title'):
        return jsonify({
            'error': 'Validation Error',
            'message': 'topic_title is required'
        }), 400
    
    try:
        llm = LLMGenerator()
        
        problems = llm.generate_coding_problems(
            topic=data['topic_title'],
            count=data.get('count', 3),
            difficulty=data.get('difficulty', 'intermediate'),
            language=data.get('language', 'python')
        )
        
        return jsonify({
            'topic': data['topic_title'],
            'problems': problems
        }), 200
        
    except Exception as e:
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
    data = request.get_json()
    
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
    data = request.get_json()
    
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
        return jsonify({
            'error': 'Analysis Failed',
            'message': str(e)
        }), 500


@ai_bp.route('/adaptive-update', methods=['POST'])
@jwt_required()
def get_adaptive_update():
    """
    Get adaptive curriculum updates based on user performance.
    
    This endpoint analyzes the user's curriculum and suggests
    improvements or additional topics.
    """
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({
            'error': 'Not Found',
            'message': 'User not found'
        }), 404
    
    try:
        recommender = CurriculumRecommender()
        
        # Get user's curriculum data
        curricula = Curriculum.query.filter_by(user_id=user_id, status='active').all()
        
        # Get adaptive recommendations based on curriculum data
        recommendations = recommender.get_adaptive_recommendations(
            user=user,
            curricula=curricula
        )
        
        return jsonify({
            'recommendations': recommendations
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Analysis Failed',
            'message': str(e)
        }), 500
