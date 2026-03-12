# SmartCurriculum - Routes Package
# Exports all API route blueprints

from routes.auth import auth_bp
from routes.curriculum import curriculum_bp
from routes.ai import ai_bp
from routes.resume import resume_bp
from routes.admin import admin_bp

__all__ = [
    'auth_bp',
    'curriculum_bp', 
    'ai_bp',
    'resume_bp',
    'admin_bp'
]
