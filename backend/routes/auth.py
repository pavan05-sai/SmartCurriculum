# SmartCurriculum - Authentication Routes
# Handles user registration, login, and profile management

from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token,
    jwt_required, 
    get_jwt_identity
)
from database import db
from models.user import User

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
    
    # Validate required fields
    required_fields = ['email', 'password', 'name']
    for field in required_fields:
        if not data.get(field):
            return jsonify({
                'error': 'Validation Error',
                'message': f'{field} is required'
            }), 400
    
    # Check if email already exists
    existing_user = User.query.filter_by(email=data['email'].lower()).first()
    if existing_user:
        return jsonify({
            'error': 'Registration Failed',
            'message': 'Email already registered'
        }), 409
    
    # Validate password length
    if len(data['password']) < 6:
        return jsonify({
            'error': 'Validation Error',
            'message': 'Password must be at least 6 characters'
        }), 400
    
    try:
        # Create new user
        user = User(
            email=data['email'],
            password=data['password'],
            name=data['name'],
            semester=data.get('semester', 1),
            skill_level=data.get('skill_level', 'beginner'),
            career_goal=data.get('career_goal', 'placement'),
            learning_pace=data.get('learning_pace', 'moderate'),
            branch=data.get('branch', 'Computer Science')
        )
        
        # Set optional list fields
        if data.get('weak_subjects'):
            user.set_weak_subjects(data['weak_subjects'])
        if data.get('strong_subjects'):
            user.set_strong_subjects(data['strong_subjects'])
        if data.get('interests'):
            user.set_interests(data['interests'])
        
        # Save to database
        db.session.add(user)
        db.session.commit()
        
        # Generate tokens
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        
        return jsonify({
            'message': 'Registration successful',
            'user': user.to_dict(include_sensitive=True),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Registration Failed',
            'message': str(e)
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
    with open('debug_log.txt', 'a') as f:
        f.write("\n>>> DEBUG: Login request received\n")
        data = request.get_json()
        f.write(f">>> DEBUG: Login attempt for email: {data.get('email')}\n")
        
        # Validate required fields
        if not data.get('email') or not data.get('password'):
            f.write(">>> DEBUG: Missing email or password\n")
            return jsonify({
                'error': 'Validation Error',
                'message': 'Email and password are required'
            }), 400
        
        # Find user by email
        f.write(">>> DEBUG: Querying database for user...\n")
        user = User.query.filter_by(email=data['email'].lower()).first()
        f.write(f">>> DEBUG: User found: {user is not None}\n")
        
        # Verify user exists and password is correct
        if not user:
            f.write(">>> DEBUG: Login failed - User not found\n")
            return jsonify({
                'error': 'Login Failed',
                'message': 'Invalid email or password'
            }), 401
            
        f.write(">>> DEBUG: Verifying password...\n")
        f.flush() # Ensure logs are written before bcrypt call
        
        try:
            password_correct = user.check_password(data['password'])
            f.write(f">>> DEBUG: Password correct: {password_correct}\n")
        except Exception as e:
            f.write(f">>> DEBUG: FATAL ERROR during check_password: {str(e)}\n")
            f.flush()
            raise e
        
        if not password_correct:
            f.write(">>> DEBUG: Login failed - Incorrect password\n")
            return jsonify({
                'error': 'Login Failed',
                'message': 'Invalid email or password'
            }), 401
        
        # Generate tokens
        f.write(">>> DEBUG: Generating JWT tokens...\n")
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        f.write(">>> DEBUG: Tokens generated successfully\n")
        
        f.write(">>> DEBUG: Login successful, returning response\n\n")
        f.flush()
    
    return jsonify({
        'message': 'Login successful',
        'user': user.to_dict(include_sensitive=True),
        'access_token': access_token,
        'refresh_token': refresh_token
    }), 200
    
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
    with open('debug_log.txt', 'a') as f:
        f.write("\n>>> DEBUG: get_profile request received\n")
        user_id = get_jwt_identity()
        f.write(f">>> DEBUG: User ID from token: {user_id}\n")
        user = User.query.get(user_id)
        f.write(f">>> DEBUG: User found: {user is not None}\n")
        
        if not user:
            f.write(">>> DEBUG: User not found in database\n")
            return jsonify({
                'error': 'Not Found',
                'message': 'User not found'
            }), 404
        
        f.write(">>> DEBUG: Returning profile data\n\n")
        f.flush()
    
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
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({
            'error': 'Not Found',
            'message': 'User not found'
        }), 404
    
    data = request.get_json()
    
    # Update simple fields
    simple_fields = ['name', 'semester', 'skill_level', 'career_goal', 'learning_pace', 'branch']
    for field in simple_fields:
        if field in data:
            setattr(user, field, data[field])
    
    # Update list fields
    if 'weak_subjects' in data:
        user.set_weak_subjects(data['weak_subjects'])
    if 'strong_subjects' in data:
        user.set_strong_subjects(data['strong_subjects'])
    if 'interests' in data:
        user.set_interests(data['interests'])
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict(include_sensitive=True)
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Update Failed',
            'message': str(e)
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
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({
            'error': 'Not Found',
            'message': 'User not found'
        }), 404
    
    data = request.get_json()
    
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
        db.session.commit()
        return jsonify({
            'message': 'Password changed successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Update Failed',
            'message': str(e)
        }), 500


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    """
    Refresh the access token using a refresh token.
    """
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=str(user_id))
    
    return jsonify({
        'access_token': access_token
    }), 200
