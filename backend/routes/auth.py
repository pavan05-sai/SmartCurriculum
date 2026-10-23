# SmartCurriculum - Authentication Routes (MongoDB)
# Handles user registration, login, and profile management

import logging
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from database import get_db
from models.user import User

logger = logging.getLogger(__name__)

# Create blueprint for auth routes
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user.

    Expected JSON body:
    {
        "email": "user@example.com",
        "password": "password123",
        "name": "John Doe",
        "semester": 3,
        "skill_level": "beginner",
        "career_goal": "placement",
        "branch": "Computer Science"
    }
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Validation Error', 'message': 'Request body is required'}), 400

    # Validate required fields
    required_fields = ['email', 'password', 'name']
    for field in required_fields:
        if not data.get(field):
            return jsonify({
                'error': 'Validation Error',
                'message': f'{field} is required'
            }), 400

    # Validate email format (basic)
    email = data['email'].strip().lower()
    if '@' not in email or '.' not in email:
        return jsonify({'error': 'Validation Error', 'message': 'Invalid email format'}), 400

    # Validate password length
    if len(data['password']) < 6:
        return jsonify({
            'error': 'Validation Error',
            'message': 'Password must be at least 6 characters'
        }), 400

    db = get_db()

    # Check if email already exists
    existing_user = User.find_by_email(db, email)
    if existing_user:
        return jsonify({
            'error': 'Registration Failed',
            'message': 'Email already registered'
        }), 409

    try:
        # Create new user
        user = User.create(
            db=db,
            email=email,
            password=data['password'],
            name=data['name'],
            semester=data.get('semester', 1),
            skill_level=data.get('skill_level', 'beginner'),
            career_goal=data.get('career_goal', 'placement'),
            learning_pace=data.get('learning_pace', 'moderate'),
            branch=data.get('branch', 'Computer Science'),
            weak_subjects=data.get('weak_subjects', []),
            strong_subjects=data.get('strong_subjects', []),
            interests=data.get('interests', [])
        )

        # Generate tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        logger.info(f"New user registered: {email}")

        return jsonify({
            'message': 'Registration successful',
            'user': user.to_dict(include_sensitive=True),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 201

    except Exception as e:
        logger.error(f"Registration error for {email}: {e}")
        return jsonify({
            'error': 'Registration Failed',
            'message': 'An error occurred during registration. Please try again.'
        }), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login an existing user.

    Expected JSON body:
    {
        "email": "user@example.com",
        "password": "password123"
    }
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Validation Error', 'message': 'Request body is required'}), 400

    # Validate required fields
    if not data.get('email') or not data.get('password'):
        return jsonify({
            'error': 'Validation Error',
            'message': 'Email and password are required'
        }), 400

    db = get_db()

    # Find user by email
    user = User.find_by_email(db, data['email'])

    # Verify user exists and password is correct
    if not user or not user.check_password(data['password']):
        return jsonify({
            'error': 'Login Failed',
            'message': 'Invalid email or password'
        }), 401

    # Generate tokens
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    logger.info(f"User logged in: {user.email}")

    return jsonify({
        'message': 'Login successful',
        'user': user.to_dict(include_sensitive=True),
        'access_token': access_token,
        'refresh_token': refresh_token
    }), 200


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """
    Get the current user's profile.
    Requires JWT authentication.
    """
    user_id = get_jwt_identity()
    db = get_db()
    user = User.find_by_id(db, user_id)

    if not user:
        return jsonify({
            'error': 'Not Found',
            'message': 'User not found'
        }), 404

    return jsonify({
        'user': user.to_dict(include_sensitive=True)
    }), 200


@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """
    Update the current user's profile.

    Expected JSON body (all fields optional):
    {
        "name": "New Name",
        "semester": 4,
        "skill_level": "intermediate",
        "career_goal": "startup",
        "weak_subjects": ["Math", "Physics"],
        "strong_subjects": ["Programming"],
        "interests": ["AI", "Web Development"],
        "learning_pace": "fast",
        "branch": "Computer Science"
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

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Validation Error', 'message': 'Request body is required'}), 400

    # Build update document with allowed fields only
    allowed_simple = ['name', 'semester', 'skill_level', 'career_goal', 'learning_pace', 'branch']
    allowed_list = ['weak_subjects', 'strong_subjects', 'interests']
    updates = {}

    for field in allowed_simple:
        if field in data:
            updates[field] = data[field]

    for field in allowed_list:
        if field in data:
            if not isinstance(data[field], list):
                return jsonify({
                    'error': 'Validation Error',
                    'message': f'{field} must be a list'
                }), 400
            updates[field] = data[field]

    if not updates:
        return jsonify({'error': 'Validation Error', 'message': 'No valid fields to update'}), 400

    try:
        user.update(updates)
        # Re-fetch updated user
        user = User.find_by_id(db, user_id)
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict(include_sensitive=True)
        }), 200
    except Exception as e:
        logger.error(f"Profile update error for user {user_id}: {e}")
        return jsonify({
            'error': 'Update Failed',
            'message': 'An error occurred while updating your profile.'
        }), 500


@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """
    Change the current user's password.

    Expected JSON body:
    {
        "current_password": "oldpassword",
        "new_password": "newpassword"
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

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Validation Error', 'message': 'Request body is required'}), 400

    # Validate current password
    if not user.check_password(data.get('current_password', '')):
        return jsonify({
            'error': 'Validation Error',
            'message': 'Current password is incorrect'
        }), 400

    # Validate new password
    new_password = data.get('new_password', '')
    if len(new_password) < 6:
        return jsonify({
            'error': 'Validation Error',
            'message': 'New password must be at least 6 characters'
        }), 400

    try:
        user.set_password(new_password)
        return jsonify({'message': 'Password changed successfully'}), 200
    except Exception as e:
        logger.error(f"Password change error for user {user_id}: {e}")
        return jsonify({
            'error': 'Update Failed',
            'message': 'An error occurred while changing your password.'
        }), 500


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    """Refresh the access token using a refresh token."""
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)
    return jsonify({'access_token': access_token}), 200
