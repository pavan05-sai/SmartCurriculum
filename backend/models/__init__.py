# SmartCurriculum Models Package
# MongoDB-based models for all application entities

from models.user import User
from models.curriculum import Curriculum, Topic
from models.skill import Skill, get_skill_category

__all__ = ['User', 'Curriculum', 'Topic', 'Skill', 'get_skill_category']
