# SmartCurriculum - Curriculum Routes
# Handles curriculum generation, retrieval, and PDF export

from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from models.user import User
from models.curriculum import Curriculum, Topic
from ai_engine.recommender import CurriculumRecommender
from utils.pdf_generator import generate_curriculum_pdf
import io

# Create blueprint for curriculum routes
curriculum_bp = Blueprint('curriculum', __name__)


@curriculum_bp.route('', methods=['GET'])
@jwt_required()
def get_curricula():
    """
    Get all curricula for the current user.
    
    Query params:
    - status: Filter by status (active, completed, archived)
    """
    user_id = get_jwt_identity()
    
    # Get filter params
    status = request.args.get('status')
    
    # Build query
    query = Curriculum.query.filter_by(user_id=user_id)
    if status:
        query = query.filter_by(status=status)
    
    curricula = query.order_by(Curriculum.created_at.desc()).all()
    
    return jsonify({
        'curricula': [c.to_dict() for c in curricula],
        'total': len(curricula)
    }), 200


@curriculum_bp.route('/<int:curriculum_id>', methods=['GET'])
@jwt_required()
def get_curriculum(curriculum_id):
    """
    Get a specific curriculum with all topics.
    """
    user_id = get_jwt_identity()
    
    curriculum = Curriculum.query.filter_by(
        id=curriculum_id, 
        user_id=user_id
    ).first()
    
    if not curriculum:
        return jsonify({
            'error': 'Not Found',
            'message': 'Curriculum not found'
        }), 404
    
    return jsonify({
        'curriculum': curriculum.to_dict(include_topics=True)
    }), 200


@curriculum_bp.route('/generate', methods=['POST'])
@jwt_required()
def generate_curriculum():
    """
    Generate a personalized curriculum based on user profile and selected program.
    
    Expected JSON body:
    {
        "domain": "computer-science",  // Domain ID from available options
        "intensity": "regular",        // casual, regular, intensive
        "hours_per_week": 20
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
        # Import domain datasets
        from data.curriculum_datasets import get_curriculum_for_domain
        
        # Get domain-specific curriculum
        domain_id = data.get('domain', 'engineering-cs')
        domain_curriculum = get_curriculum_for_domain(domain_id)
        
        # Calculate intensity multiplier for duration
        intensity = data.get('intensity', 'regular')
        intensity_multipliers = {
            'casual': 1.5,    # Takes longer at casual pace
            'regular': 1.0,   # Normal pace
            'intensive': 0.6  # Faster at intensive pace
        }
        multiplier = intensity_multipliers.get(intensity, 1.0)
        
        # Calculate total hours and credits from all semesters
        total_hours = 0
        total_credits = 0
        topics_data = []
        order_index = 0
        
        for semester in domain_curriculum['semesters']:
            semester_num = semester['semester']
            
            for subject in semester['subjects']:
                # Calculate hours based on credits (1 credit ≈ 15 hours)
                base_hours = subject.get('credits', 3) * 15
                adjusted_hours = int(base_hours * multiplier)
                total_hours += adjusted_hours
                total_credits += subject.get('credits', 3)
                
                topics_data.append({
                    'title': subject['title'],
                    'description': subject.get('description', ''),
                    'week': semester_num,  # Using week field for semester number
                    'semester': semester_num,
                    'order_index': order_index,
                    'difficulty': domain_curriculum['difficulty'],
                    'estimated_hours': adjusted_hours,
                    'credits': subject.get('credits', 3),
                    'course_code': subject.get('code', ''),
                    'resources': subject.get('resources', []),
                    'skills_gained': subject.get('skills', []),
                    'phase': semester['name']
                })
                order_index += 1
        
        # Calculate duration in weeks based on total semesters
        total_semesters = domain_curriculum.get('total_semesters', 8)
        # Each semester is approximately 16 weeks
        calculated_weeks = total_semesters * 16
        
        # Create curriculum in database
        curriculum = Curriculum(
            user_id=user_id,
            title=domain_curriculum['title'],
            description=domain_curriculum['description'],
            difficulty=domain_curriculum['difficulty'],
            duration_weeks=calculated_weeks,
            career_focus=user.career_goal,
            total_hours=total_hours
        )
        
        db.session.add(curriculum)
        db.session.flush()  # Get curriculum ID
        
        # Create topics
        for topic_data in topics_data:
            topic = Topic(
                curriculum_id=curriculum.id,
                title=topic_data['title'],
                description=topic_data['description'],
                week=topic_data['week'],
                order_index=topic_data['order_index'],
                phase=topic_data['phase'],
                difficulty=topic_data['difficulty'],
                estimated_hours=topic_data['estimated_hours']
            )
            topic.set_resources(topic_data.get('resources', []))
            topic.set_skills_gained(topic_data.get('skills_gained', []))
            # Store credits and course code in a JSON field if needed
            db.session.add(topic)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Curriculum generated successfully',
            'curriculum': curriculum.to_dict(include_topics=True)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Generation Failed',
            'message': str(e)
        }), 500


@curriculum_bp.route('/roadmap', methods=['GET'])
@jwt_required()
def get_roadmap():
    """
    Get the weekly learning roadmap for the user's active curriculum.
    """
    user_id = get_jwt_identity()
    
    # Get the active curriculum
    curriculum = Curriculum.query.filter_by(
        user_id=user_id,
        status='active'
    ).order_by(Curriculum.created_at.desc()).first()
    
    if not curriculum:
        return jsonify({
            'error': 'Not Found',
            'message': 'No active curriculum found. Generate one first.'
        }), 404
    
    # Build roadmap data
    roadmap = {
        'curriculum_id': curriculum.id,
        'title': curriculum.title,
        'duration_weeks': curriculum.duration_weeks,
        'progress': curriculum.calculate_progress(),
        'weeks': curriculum.get_topics_by_week()
    }
    
    return jsonify({
        'roadmap': roadmap
    }), 200


@curriculum_bp.route('/<int:curriculum_id>/pdf', methods=['GET'])
@jwt_required()
def download_curriculum_pdf(curriculum_id):
    """
    Download the curriculum as a PDF roadmap.
    """
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    curriculum = Curriculum.query.filter_by(
        id=curriculum_id,
        user_id=user_id
    ).first()
    
    if not curriculum:
        return jsonify({
            'error': 'Not Found',
            'message': 'Curriculum not found'
        }), 404
    
    try:
        # Generate PDF
        pdf_buffer = generate_curriculum_pdf(curriculum, user)
        
        # Return as downloadable file
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'curriculum_{curriculum.id}_roadmap.pdf'
        )
        
    except Exception as e:
        return jsonify({
            'error': 'PDF Generation Failed',
            'message': str(e)
        }), 500


@curriculum_bp.route('/<int:curriculum_id>', methods=['PUT'])
@jwt_required()
def update_curriculum(curriculum_id):
    """
    Update curriculum details.
    
    Expected JSON body:
    {
        "title": "New Title",
        "description": "New description",
        "status": "completed"
    }
    """
    user_id = get_jwt_identity()
    
    curriculum = Curriculum.query.filter_by(
        id=curriculum_id,
        user_id=user_id
    ).first()
    
    if not curriculum:
        return jsonify({
            'error': 'Not Found',
            'message': 'Curriculum not found'
        }), 404
    
    data = request.get_json()
    
    # Update fields
    if 'title' in data:
        curriculum.title = data['title']
    if 'description' in data:
        curriculum.description = data['description']
    if 'status' in data:
        curriculum.status = data['status']
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Curriculum updated',
            'curriculum': curriculum.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Update Failed',
            'message': str(e)
        }), 500


@curriculum_bp.route('/<int:curriculum_id>', methods=['DELETE'])
@jwt_required()
def delete_curriculum(curriculum_id):
    """
    Delete a curriculum and all its topics.
    """
    user_id = get_jwt_identity()
    
    curriculum = Curriculum.query.filter_by(
        id=curriculum_id,
        user_id=user_id
    ).first()
    
    if not curriculum:
        return jsonify({
            'error': 'Not Found',
            'message': 'Curriculum not found'
        }), 404
    
    try:
        db.session.delete(curriculum)
        db.session.commit()
        return jsonify({
            'message': 'Curriculum deleted'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Delete Failed',
            'message': str(e)
        }), 500


@curriculum_bp.route('/topic/<int:topic_id>', methods=['GET'])
@jwt_required()
def get_topic(topic_id):
    """
    Get details of a specific topic.
    """
    user_id = get_jwt_identity()
    
    topic = Topic.query.join(Curriculum).filter(
        Topic.id == topic_id,
        Curriculum.user_id == user_id
    ).first()
    
    if not topic:
        return jsonify({
            'error': 'Not Found',
            'message': 'Topic not found'
        }), 404
    
    return jsonify({
        'topic': topic.to_dict()
    }), 200


@curriculum_bp.route('/topic/<int:topic_id>/complete', methods=['POST'])
@jwt_required()
def complete_topic(topic_id):
    """
    Mark a topic as completed.
    """
    user_id = get_jwt_identity()
    
    topic = Topic.query.join(Curriculum).filter(
        Topic.id == topic_id,
        Curriculum.user_id == user_id
    ).first()
    
    if not topic:
        return jsonify({
            'error': 'Not Found',
            'message': 'Topic not found'
        }), 404
    
    try:
        topic.mark_completed()
        db.session.commit()
        return jsonify({
            'message': 'Topic marked as completed',
            'topic': topic.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Update Failed',
            'message': str(e)
        }), 500


@curriculum_bp.route('/topic/<int:topic_id>/skills', methods=['PUT'])
@jwt_required()
def update_topic_skills(topic_id):
    """
    Update completed skills for a topic.
    """
    user_id = get_jwt_identity()
    
    topic = Topic.query.join(Curriculum).filter(
        Topic.id == topic_id,
        Curriculum.user_id == user_id
    ).first()
    
    if not topic:
        return jsonify({
            'error': 'Not Found',
            'message': 'Topic not found'
        }), 404
    
    data = request.get_json()
    completed_skills = data.get('completed_skills', [])
    
    try:
        topic.set_completed_skills(completed_skills)
        db.session.commit()
        return jsonify({
            'message': 'Skills updated',
            'topic': topic.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Update Failed',
            'message': str(e)
        }), 500
