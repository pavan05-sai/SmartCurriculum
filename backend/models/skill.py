# SmartCurriculum - Skill Model (MongoDB)
# Tracks skills acquired by users for resume mapping

from datetime import datetime
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)


class Skill:
    """
    Skill model for MongoDB.

    Skills are gained by completing topics or self-declared, used for:
    1. Resume skill mapping - generating resume bullet points
    2. Skill gap analysis - comparing with job requirements
    3. Proficiency tracking - monitoring skill development
    """

    COLLECTION = 'skills'

    def __init__(self, db, data: dict):
        self._db = db
        self._data = data

    # ─── Properties ───────────────────────────────────────────────────────────

    @property
    def id(self):
        return str(self._data.get('_id', ''))

    @property
    def user_id(self):
        return str(self._data.get('user_id', ''))

    @property
    def name(self):
        return self._data.get('name', '')

    @property
    def category(self):
        return self._data.get('category', 'other')

    @property
    def level(self):
        return self._data.get('level', 'beginner')

    @property
    def proficiency_score(self):
        return self._data.get('proficiency_score', 0)

    @property
    def source(self):
        return self._data.get('source', 'curriculum')

    @property
    def source_topic_id(self):
        return self._data.get('source_topic_id')

    @property
    def resume_bullet(self):
        return self._data.get('resume_bullet', '')

    @property
    def is_verified(self):
        return self._data.get('is_verified', False)

    @property
    def show_on_resume(self):
        return self._data.get('show_on_resume', True)

    @property
    def acquired_at(self):
        return self._data.get('acquired_at')

    # ─── CRUD Class Methods ───────────────────────────────────────────────────

    @classmethod
    def create(cls, db, user_id: str, name: str, **kwargs) -> 'Skill':
        """Insert a new skill document."""
        doc = {
            'user_id': str(user_id),
            'name': name.strip(),
            'category': kwargs.get('category', get_skill_category(name)),
            'level': kwargs.get('level', 'beginner'),
            'proficiency_score': kwargs.get('proficiency_score', 25),
            'source': kwargs.get('source', 'curriculum'),
            'source_topic_id': kwargs.get('source_topic_id'),
            'resume_bullet': kwargs.get('resume_bullet', ''),
            'is_verified': kwargs.get('is_verified', False),
            'show_on_resume': kwargs.get('show_on_resume', True),
            'acquired_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
        }
        result = db[cls.COLLECTION].insert_one(doc)
        doc['_id'] = result.inserted_id
        return cls(db, doc)

    @classmethod
    def find_by_user(cls, db, user_id: str, category: str = None, show_on_resume: bool = None) -> list:
        """Find skills for a user with optional category and visibility filters."""
        query = {'user_id': str(user_id)}
        if category:
            query['category'] = category
        if show_on_resume is not None:
            query['show_on_resume'] = show_on_resume

        docs = db[cls.COLLECTION].find(query).sort('proficiency_score', -1)
        return [cls(db, doc) for doc in docs]

    @classmethod
    def find_by_id(cls, db, skill_id: str) -> 'Skill | None':
        try:
            doc = db[cls.COLLECTION].find_one({'_id': ObjectId(str(skill_id))})
            return cls(db, doc) if doc else None
        except Exception:
            return None

    @classmethod
    def find_by_user_and_id(cls, db, user_id: str, skill_id: str) -> 'Skill | None':
        """Find a specific skill belonging to a user."""
        try:
            doc = db[cls.COLLECTION].find_one({
                '_id': ObjectId(str(skill_id)),
                'user_id': str(user_id)
            })
            return cls(db, doc) if doc else None
        except Exception:
            return None

    @classmethod
    def find_by_user_and_name(cls, db, user_id: str, name: str) -> 'Skill | None':
        """Find a skill by name (case-insensitive) for a user."""
        import re
        doc = db[cls.COLLECTION].find_one({
            'user_id': str(user_id),
            'name': {'$regex': f'^{re.escape(name.strip())}$', '$options': 'i'}
        })
        return cls(db, doc) if doc else None

    @classmethod
    def find_by_ids_and_user(cls, db, user_id: str, skill_ids: list) -> list:
        """Find multiple skills by list of ID strings for a user."""
        obj_ids = []
        for sid in skill_ids:
            try:
                obj_ids.append(ObjectId(str(sid)))
            except Exception:
                pass
        docs = db[cls.COLLECTION].find({
            '_id': {'$in': obj_ids},
            'user_id': str(user_id)
        })
        return [cls(db, doc) for doc in docs]

    def update(self, fields: dict) -> bool:
        """Update skill fields."""
        fields['updated_at'] = datetime.utcnow()
        result = self._db[self.COLLECTION].update_one(
            {'_id': self._data['_id']},
            {'$set': fields}
        )
        if result.modified_count > 0:
            self._data.update(fields)
        return result.acknowledged

    def update_proficiency(self, score: int) -> bool:
        """Update proficiency score and adjust level."""
        score = max(0, min(100, score))
        if score >= 90:
            level = 'expert'
        elif score >= 70:
            level = 'advanced'
        elif score >= 40:
            level = 'intermediate'
        else:
            level = 'beginner'

        return self.update({
            'proficiency_score': score,
            'level': level
        })

    def delete(self) -> bool:
        """Delete this skill document."""
        result = self._db[self.COLLECTION].delete_one({'_id': self._data['_id']})
        return result.deleted_count > 0

    # ─── Business Logic ───────────────────────────────────────────────────────

    def generate_resume_bullet(self) -> str:
        """Generate a default resume bullet point for this skill."""
        level_descriptions = {
            'beginner': 'Familiar with',
            'intermediate': 'Proficient in',
            'advanced': 'Experienced with',
            'expert': 'Expert-level proficiency in'
        }
        description = level_descriptions.get(self.level, 'Knowledge of')
        return f"{description} {self.name} for technical problem-solving and implementation"

    # ─── Serialization ────────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        """Convert skill to dictionary for API responses."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'category': self.category,
            'level': self.level,
            'proficiency_score': self.proficiency_score,
            'source': self.source,
            'source_topic_id': self.source_topic_id,
            'resume_bullet': self.resume_bullet or self.generate_resume_bullet(),
            'is_verified': self.is_verified,
            'show_on_resume': self.show_on_resume,
            'acquired_at': self.acquired_at.isoformat() if self.acquired_at else None,
        }

    def __repr__(self):
        return f'<Skill {self.name} ({self.level})>'


# ─── Predefined Skill Categories ──────────────────────────────────────────────

SKILL_CATEGORIES = {
    'programming': [
        'Python', 'JavaScript', 'Java', 'C++', 'C', 'Go', 'Rust', 'TypeScript',
        'SQL', 'PHP', 'Ruby', 'Swift', 'Kotlin', 'R', 'MATLAB'
    ],
    'web_development': [
        'HTML', 'CSS', 'React', 'Angular', 'Vue.js', 'Node.js', 'Express.js',
        'Django', 'Flask', 'FastAPI', 'Next.js', 'Bootstrap', 'Tailwind CSS'
    ],
    'data_science': [
        'Machine Learning', 'Deep Learning', 'Data Analysis', 'Data Visualization',
        'Pandas', 'NumPy', 'Scikit-learn', 'TensorFlow', 'PyTorch', 'Keras',
        'Statistical Analysis', 'Data Mining', 'NLP', 'Computer Vision'
    ],
    'databases': [
        'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'SQLite', 'Oracle',
        'Cassandra', 'Firebase', 'Supabase', 'Elasticsearch'
    ],
    'devops': [
        'Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP', 'CI/CD', 'Jenkins',
        'Git', 'Linux', 'Terraform', 'Ansible'
    ],
    'soft_skills': [
        'Problem Solving', 'Critical Thinking', 'Communication', 'Teamwork',
        'Project Management', 'Time Management', 'Leadership', 'Agile'
    ]
}


def get_skill_category(skill_name: str) -> str:
    """
    Get the category for a given skill name.

    Args:
        skill_name: Name of the skill

    Returns:
        Category name or 'other' if not found
    """
    skill_lower = skill_name.lower()
    for category, skills in SKILL_CATEGORIES.items():
        if any(s.lower() in skill_lower or skill_lower in s.lower() for s in skills):
            return category
    return 'other'
