# SmartCurriculum - Main Application Entry Point
# Flask application with CORS, JWT authentication, and route registration

import os

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import get_config
from database import init_db, db

# Create Flask application
app = Flask(__name__)

# Load configuration
config = get_config()
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = config.JWT_ACCESS_TOKEN_EXPIRES

# Initialize CORS for frontend communication
CORS(app, origins=config.CORS_ORIGINS, supports_credentials=True)

# Initialize JWT for authentication
jwt = JWTManager(app)

# Initialize database (allow tests to skip auto-init)
if os.environ.get("SKIP_DB_INIT") != "1":
    init_db(app)




# ============================================================
# Register Blueprints (API Routes)
# ============================================================

from routes.auth import auth_bp
from routes.curriculum import curriculum_bp
from routes.ai import ai_bp
from routes.resume import resume_bp
from routes.admin import admin_bp

# Register all route blueprints with /api prefix
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(curriculum_bp, url_prefix='/api/curriculum')
app.register_blueprint(ai_bp, url_prefix='/api/ai')
app.register_blueprint(resume_bp, url_prefix='/api/resume')
app.register_blueprint(admin_bp, url_prefix='/api/admin')


# ============================================================
# Health Check and Root Endpoints
# ============================================================

@app.route('/')
def index():
    """Root endpoint with API information."""
    return jsonify({
        'name': 'SmartCurriculum API',
        'version': '1.0.0',
        'description': 'AI-Powered Personalized Educational Curriculum Design System',
        'endpoints': {
            'auth': '/api/auth',
            'curriculum': '/api/curriculum',
            'ai': '/api/ai',
            'resume': '/api/resume',
            'admin': '/api/admin'
        }
    })


@app.route('/api/health')
def health_check():
    """Health check endpoint for monitoring."""
    return jsonify({
        'status': 'healthy',
        'database': 'connected',
        'version': '1.0.0'
    })


# ============================================================
# Error Handlers
# ============================================================

@app.errorhandler(400)
def bad_request(error):
    """Handle 400 Bad Request errors."""
    return jsonify({
        'error': 'Bad Request',
        'message': str(error.description) if hasattr(error, 'description') else 'Invalid request'
    }), 400


@app.errorhandler(401)
def unauthorized(error):
    """Handle 401 Unauthorized errors."""
    return jsonify({
        'error': 'Unauthorized',
        'message': 'Authentication required'
    }), 401


@app.errorhandler(403)
def forbidden(error):
    """Handle 403 Forbidden errors."""
    return jsonify({
        'error': 'Forbidden',
        'message': 'Access denied'
    }), 403


@app.errorhandler(404)
def not_found(error):
    """Handle 404 Not Found errors."""
    return jsonify({
        'error': 'Not Found',
        'message': 'Resource not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 Internal Server errors."""
    db.session.rollback()  # Rollback any failed transactions
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred'
    }), 500


# ============================================================
# JWT Error Handlers
# ============================================================

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    """Handle expired JWT tokens."""
    print(f"JWT TOKEN EXPIRED: {jwt_payload}")
    return jsonify({
        'error': 'Token Expired',
        'message': 'Your session has expired. Please login again.'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    """Handle invalid JWT tokens."""
    print(f"JWT INVALID TOKEN: {error}")
    return jsonify({
        'error': 'Invalid Token',
        'message': 'Invalid authentication token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    """Handle missing JWT tokens."""
    print(f"JWT MISSING TOKEN: {error}")
    return jsonify({
        'error': 'Missing Token',
        'message': 'Authentication token is required'
    }), 401


# ============================================================
# Application Entry Point
# ============================================================

if __name__ == '__main__':
    # Run the development server
    print("\n" + "=" * 60)
    print("SmartCurriculum API Server")
    print("=" * 60)
    print(f"Environment: {'Development' if config.DEBUG else 'Production'}")
    print(f"Database: {config.DATABASE_TYPE}")
    print(f"Server: http://localhost:5000")
    print("=" * 60 + "\n")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=config.DEBUG
    )
