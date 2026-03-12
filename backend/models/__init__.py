# SmartCurriculum - Database Models Package
# This module exports all database models for easy importing

from models.user import User
from models.curriculum import Curriculum, Topic
from models.skill import Skill

# Export all models
__all__ = ['User', 'Curriculum', 'Topic', 'Skill']
