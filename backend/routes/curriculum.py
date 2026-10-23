# SmartCurriculum - Curriculum Routes (MongoDB)
# Handles curriculum generation, retrieval, progress tracking, and PDF export

import logging
from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import get_db
from models.user import User
from models.curriculum import Curriculum, Topic

logger = logging.getLogger(__name__)

# Create blueprint for curriculum routes
curriculum_bp = Blueprint('curriculum', __name__)


@curriculum_bp.route('', methods=['GET'], strict_slashes=False)
@curriculum_bp.route('/', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_curricula():
    """
    Get all curricula for the current user.

    Query params:
    - status: Filter by status (active, completed, archived)
    """
    user_id = get_jwt_identity()
    db = get_db()

    status = request.args.get('status')
    curricula = Curriculum.find_by_user(db, user_id, status=status)

    return jsonify({
        'curricula': [c.to_dict() for c in curricula],
        'total': len(curricula)
    }), 200


@curriculum_bp.route('/<string:curriculum_id>', methods=['GET'])
@jwt_required()
def get_curriculum(curriculum_id):
    """Get a specific curriculum with all its topics."""
    user_id = get_jwt_identity()
    db = get_db()

    curriculum = Curriculum.find_one_by_user_and_id(db, curriculum_id, user_id)
    if not curriculum:
        return jsonify({'error': 'Not Found', 'message': 'Curriculum not found'}), 404

    return jsonify({'curriculum': curriculum.to_dict(include_topics=True)}), 200


@curriculum_bp.route('/generate', methods=['POST'])
@jwt_required()
def generate_curriculum():
    """
    Generate a personalized curriculum based on user profile and selected program.

    Expected JSON body:
    {
        "domain": "engineering-cs",   // Domain ID
        "intensity": "regular",       // casual, regular, intensive
        "hours_per_week": 20
    }
    """
    user_id = get_jwt_identity()
    db = get_db()
    user = User.find_by_id(db, user_id)

    if not user:
        return jsonify({'error': 'Not Found', 'message': 'User not found'}), 404

    data = request.get_json() or {}

    try:
        from data.curriculum_datasets import get_curriculum_for_domain

        domain_id = data.get('domain', 'engineering-cs')
        domain_curriculum = get_curriculum_for_domain(domain_id)

        # Calculate intensity multiplier for duration
        intensity = data.get('intensity', 'regular')
        intensity_multipliers = {
            'casual': 1.5,
            'regular': 1.0,
            'intensive': 0.6
        }
        multiplier = intensity_multipliers.get(intensity, 1.0)

        # Build topic list from semesters
        total_hours = 0
        topics_data = []
        order_index = 0

        for semester in domain_curriculum['semesters']:
            semester_num = semester['semester']
            for subject in semester['subjects']:
                base_hours = subject.get('credits', 3) * 15
                adjusted_hours = int(base_hours * multiplier)
                total_hours += adjusted_hours

                topics_data.append({
                    'title': subject['title'],
                    'description': subject.get('description', ''),
                    'week': semester_num,
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

        total_semesters = domain_curriculum.get('total_semesters', 8)
        calculated_weeks = total_semesters * 16

        # Create curriculum document
        curriculum = Curriculum.create(
            db=db,
            user_id=user_id,
            title=domain_curriculum['title'],
            description=domain_curriculum['description'],
            difficulty=domain_curriculum['difficulty'],
            duration_weeks=calculated_weeks,
            career_focus=user.career_goal,
            total_hours=total_hours
        )

        # Create topic documents
        for td in topics_data:
            Topic.create(
                db=db,
                curriculum_id=curriculum.id,
                title=td['title'],
                description=td['description'],
                week=td['week'],
                semester=td['semester'],
                order_index=td['order_index'],
                phase=td['phase'],
                difficulty=td['difficulty'],
                estimated_hours=td['estimated_hours'],
                credits=td['credits'],
                course_code=td['course_code'],
                resources=td['resources'],
                skills_gained=td['skills_gained']
            )

        logger.info(f"Curriculum generated for user {user_id}: {curriculum.title}")

        return jsonify({
            'message': 'Curriculum generated successfully',
            'curriculum': curriculum.to_dict(include_topics=True)
        }), 201

    except ValueError as e:
        return jsonify({'error': 'Invalid Domain', 'message': str(e)}), 400
    except Exception as e:
        logger.error(f"Curriculum generation error: {e}")
        return jsonify({
            'error': 'Generation Failed',
            'message': str(e)
        }), 500


@curriculum_bp.route('/roadmap', methods=['GET'])
@jwt_required()
def get_roadmap():
    """Get the weekly/semester roadmap for the user's active curriculum."""
    user_id = get_jwt_identity()
    db = get_db()

    # Get the most recent active curriculum
    curricula = Curriculum.find_by_user(db, user_id, status='active')
    if not curricula:
        return jsonify({
            'error': 'Not Found',
            'message': 'No active curriculum found. Generate one first.'
        }), 404

    curriculum = curricula[0]

    roadmap = {
        'curriculum_id': curriculum.id,
        'title': curriculum.title,
        'duration_weeks': curriculum.duration_weeks,
        'progress': curriculum.calculate_progress(),
        'weeks': curriculum.get_topics_by_week()
    }

    return jsonify({'roadmap': roadmap}), 200


@curriculum_bp.route('/<string:curriculum_id>/pdf', methods=['GET'])
@jwt_required()
def download_curriculum_pdf(curriculum_id):
    """Download the curriculum as a PDF roadmap."""
    user_id = get_jwt_identity()
    db = get_db()

    user = User.find_by_id(db, user_id)
    curriculum = Curriculum.find_one_by_user_and_id(db, curriculum_id, user_id)

    if not curriculum:
        return jsonify({'error': 'Not Found', 'message': 'Curriculum not found'}), 404

    try:
        from utils.pdf_generator import generate_curriculum_pdf
        pdf_buffer = generate_curriculum_pdf(curriculum, user)

        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'curriculum_{curriculum_id}_roadmap.pdf'
        )
    except Exception as e:
        logger.error(f"PDF generation error for curriculum {curriculum_id}: {e}")
        return jsonify({'error': 'PDF Generation Failed', 'message': str(e)}), 500


@curriculum_bp.route('/<string:curriculum_id>', methods=['PUT'])
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
    db = get_db()

    curriculum = Curriculum.find_one_by_user_and_id(db, curriculum_id, user_id)
    if not curriculum:
        return jsonify({'error': 'Not Found', 'message': 'Curriculum not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Validation Error', 'message': 'Request body is required'}), 400

    updates = {}
    for field in ['title', 'description', 'status']:
        if field in data:
            updates[field] = data[field]

    if not updates:
        return jsonify({'error': 'Validation Error', 'message': 'No valid fields to update'}), 400

    try:
        curriculum.update(updates)
        return jsonify({
            'message': 'Curriculum updated',
            'curriculum': curriculum.to_dict()
        }), 200
    except Exception as e:
        logger.error(f"Curriculum update error: {e}")
        return jsonify({'error': 'Update Failed', 'message': str(e)}), 500


@curriculum_bp.route('/<string:curriculum_id>', methods=['DELETE'])
@jwt_required()
def delete_curriculum(curriculum_id):
    """Delete a curriculum and all its topics."""
    user_id = get_jwt_identity()
    db = get_db()

    curriculum = Curriculum.find_one_by_user_and_id(db, curriculum_id, user_id)
    if not curriculum:
        return jsonify({'error': 'Not Found', 'message': 'Curriculum not found'}), 404

    try:
        curriculum.delete()
        return jsonify({'message': 'Curriculum deleted successfully'}), 200
    except Exception as e:
        logger.error(f"Curriculum delete error: {e}")
        return jsonify({'error': 'Delete Failed', 'message': str(e)}), 500


@curriculum_bp.route('/topic/<string:topic_id>', methods=['GET'])
@jwt_required()
def get_topic(topic_id):
    """Get details of a specific topic."""
    user_id = get_jwt_identity()
    db = get_db()

    topic = Topic.find_by_id(db, topic_id)
    if not topic:
        return jsonify({'error': 'Not Found', 'message': 'Topic not found'}), 404

    # Verify ownership via curriculum
    curriculum = Curriculum.find_one_by_user_and_id(db, topic.curriculum_id, user_id)
    if not curriculum:
        return jsonify({'error': 'Forbidden', 'message': 'Access denied'}), 403

    return jsonify({'topic': topic.to_dict()}), 200


@curriculum_bp.route('/topic/<string:topic_id>/complete', methods=['POST', 'PUT'])
@curriculum_bp.route('/<string:curriculum_id>/topics/<string:topic_id>/complete', methods=['POST', 'PUT'])
@jwt_required()
def complete_topic(topic_id, curriculum_id=None):
    """Mark a topic as completed."""
    user_id = get_jwt_identity()
    db = get_db()

    topic = Topic.find_by_id(db, topic_id)
    if not topic:
        return jsonify({'error': 'Not Found', 'message': 'Topic not found'}), 404

    # Verify ownership
    curriculum = Curriculum.find_one_by_user_and_id(db, topic.curriculum_id, user_id)
    if not curriculum:
        return jsonify({'error': 'Forbidden', 'message': 'Access denied'}), 403

    try:
        topic.mark_completed()
        return jsonify({
            'message': 'Topic marked as completed',
            'topic': topic.to_dict()
        }), 200
    except Exception as e:
        logger.error(f"Topic complete error: {e}")
        return jsonify({'error': 'Update Failed', 'message': str(e)}), 500


@curriculum_bp.route('/topic/<string:topic_id>/skills', methods=['PUT'])
@jwt_required()
def update_topic_skills(topic_id):
    """Update completed skills for a topic."""
    user_id = get_jwt_identity()
    db = get_db()

    topic = Topic.find_by_id(db, topic_id)
    if not topic:
        return jsonify({'error': 'Not Found', 'message': 'Topic not found'}), 404

    # Verify ownership
    curriculum = Curriculum.find_one_by_user_and_id(db, topic.curriculum_id, user_id)
    if not curriculum:
        return jsonify({'error': 'Forbidden', 'message': 'Access denied'}), 403

    data = request.get_json()
    completed_skills = data.get('completed_skills', [])

    if not isinstance(completed_skills, list):
        return jsonify({'error': 'Validation Error', 'message': 'completed_skills must be a list'}), 400

    try:
        topic.set_completed_skills(completed_skills)
        return jsonify({
            'message': 'Skills updated',
            'topic': topic.to_dict()
        }), 200
    except Exception as e:
        logger.error(f"Topic skills update error: {e}")
        return jsonify({'error': 'Update Failed', 'message': str(e)}), 500
