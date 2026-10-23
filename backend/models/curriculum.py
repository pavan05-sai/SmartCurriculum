# SmartCurriculum - Curriculum and Topic Models (MongoDB)
# Handles personalized curriculum and learning topics

from datetime import datetime
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)


class Curriculum:
    """
    Curriculum model for MongoDB.

    Each user can have multiple curricula (e.g., for different domains or goals).
    A curriculum contains multiple topics organized by semester/week.
    """

    COLLECTION = 'curricula'

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
    def title(self):
        return self._data.get('title', '')

    @property
    def description(self):
        return self._data.get('description', '')

    @property
    def difficulty(self):
        return self._data.get('difficulty', 'intermediate')

    @property
    def duration_weeks(self):
        return self._data.get('duration_weeks', 0)

    @property
    def career_focus(self):
        return self._data.get('career_focus', '')

    @property
    def total_hours(self):
        return self._data.get('total_hours', 0)

    @property
    def status(self):
        return self._data.get('status', 'active')

    @property
    def created_at(self):
        return self._data.get('created_at')

    @property
    def updated_at(self):
        return self._data.get('updated_at')

    # ─── CRUD Class Methods ───────────────────────────────────────────────────

    @classmethod
    def create(cls, db, user_id: str, title: str, **kwargs) -> 'Curriculum':
        """Insert a new curriculum document."""
        doc = {
            'user_id': user_id,
            'title': title,
            'description': kwargs.get('description', ''),
            'difficulty': kwargs.get('difficulty', 'intermediate'),
            'duration_weeks': kwargs.get('duration_weeks', 0),
            'career_focus': kwargs.get('career_focus', ''),
            'total_hours': kwargs.get('total_hours', 0),
            'status': kwargs.get('status', 'active'),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
        }
        result = db[cls.COLLECTION].insert_one(doc)
        doc['_id'] = result.inserted_id
        return cls(db, doc)

    @classmethod
    def find_by_id(cls, db, curriculum_id: str) -> 'Curriculum | None':
        """Find a curriculum by its ObjectId string."""
        try:
            doc = db[cls.COLLECTION].find_one({'_id': ObjectId(curriculum_id)})
            return cls(db, doc) if doc else None
        except Exception:
            return None

    @classmethod
    def find_by_user(cls, db, user_id: str, status: str = None) -> list:
        """Find all curricula for a user, optionally filtered by status."""
        query = {'user_id': user_id}
        if status:
            query['status'] = status
        docs = db[cls.COLLECTION].find(query).sort('created_at', -1)
        return [cls(db, doc) for doc in docs]

    @classmethod
    def find_one_by_user_and_id(cls, db, curriculum_id: str, user_id: str) -> 'Curriculum | None':
        """Find a curriculum that belongs to a specific user."""
        try:
            doc = db[cls.COLLECTION].find_one({
                '_id': ObjectId(curriculum_id),
                'user_id': user_id
            })
            return cls(db, doc) if doc else None
        except Exception:
            return None

    def update(self, fields: dict) -> bool:
        """Update curriculum fields."""
        fields['updated_at'] = datetime.utcnow()
        result = self._db[self.COLLECTION].update_one(
            {'_id': self._data['_id']},
            {'$set': fields}
        )
        if result.modified_count > 0:
            self._data.update(fields)
        return result.acknowledged

    def delete(self) -> bool:
        """Delete this curriculum and all its topics."""
        # Delete all topics first
        self._db[Topic.COLLECTION].delete_many({'curriculum_id': self.id})
        # Delete curriculum
        result = self._db[self.COLLECTION].delete_one({'_id': self._data['_id']})
        return result.deleted_count > 0

    # ─── Business Logic ───────────────────────────────────────────────────────

    @property
    def topics(self) -> list:
        """Property to access topics list directly."""
        return self.get_topics()

    def get_topics(self) -> list:
        """Get all topics for this curriculum, sorted by week and order."""
        docs = self._db[Topic.COLLECTION].find(
            {'curriculum_id': self.id}
        ).sort([('week', 1), ('order_index', 1)])
        return [Topic(self._db, doc) for doc in docs]

    def get_topics_by_week(self) -> dict:
        """Get topics organized by week number."""
        topics = self.get_topics()
        by_week = {}
        for topic in topics:
            week = topic.week or 1
            if week not in by_week:
                by_week[week] = []
            by_week[week].append(topic.to_dict())
        return by_week

    def calculate_progress(self) -> float:
        """Calculate overall progress percentage."""
        topics = self.get_topics()
        if not topics:
            return 0.0
        completed = sum(1 for t in topics if t.status == 'completed')
        return round((completed / len(topics)) * 100, 1)

    def to_dict(self, include_topics: bool = False) -> dict:
        """Convert curriculum to dictionary for API responses."""
        topics = self.get_topics() if include_topics else []
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'difficulty': self.difficulty,
            'duration_weeks': self.duration_weeks,
            'career_focus': self.career_focus,
            'total_hours': self.total_hours,
            'status': self.status,
            'progress': self.calculate_progress(),
            'topic_count': self._db[Topic.COLLECTION].count_documents({'curriculum_id': self.id}),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

        if include_topics:
            data['topics'] = [t.to_dict() for t in topics]
            data['topics_by_week'] = self.get_topics_by_week()

        return data

    def __repr__(self):
        return f'<Curriculum {self.title}>'


class Topic:
    """
    Topic model for MongoDB.

    Topics are individual learning units within a curriculum.
    They contain resources, estimated time, and completion tracking.
    """

    COLLECTION = 'topics'

    def __init__(self, db, data: dict):
        self._db = db
        self._data = data

    # ─── Properties ───────────────────────────────────────────────────────────

    @property
    def id(self):
        return str(self._data.get('_id', ''))

    @property
    def curriculum_id(self):
        return self._data.get('curriculum_id', '')

    @property
    def title(self):
        return self._data.get('title', '')

    @property
    def description(self):
        return self._data.get('description', '')

    @property
    def week(self):
        return self._data.get('week', 1)

    @property
    def semester(self):
        return self._data.get('semester', self.week)

    @property
    def order_index(self):
        return self._data.get('order_index', 0)

    @property
    def phase(self):
        return self._data.get('phase', '')

    @property
    def credits(self):
        return self._data.get('credits', 3)

    @property
    def course_code(self):
        return self._data.get('course_code', '')

    @property
    def difficulty(self):
        return self._data.get('difficulty', 'intermediate')

    @property
    def estimated_hours(self):
        return self._data.get('estimated_hours', 2.0)

    @property
    def resources(self):
        return self._data.get('resources', [])

    @property
    def prerequisites(self):
        return self._data.get('prerequisites', [])

    @property
    def skills_gained(self):
        return self._data.get('skills_gained', [])

    @property
    def completed_skills(self):
        return self._data.get('completed_skills', [])

    @property
    def status(self):
        return self._data.get('status', 'not_started')

    @property
    def created_at(self):
        return self._data.get('created_at')

    @property
    def completed_at(self):
        return self._data.get('completed_at')

    # ─── CRUD Class Methods ───────────────────────────────────────────────────

    @classmethod
    def create(cls, db, curriculum_id: str, title: str, **kwargs) -> 'Topic':
        """Insert a new topic document."""
        doc = {
            'curriculum_id': curriculum_id,
            'title': title,
            'description': kwargs.get('description', ''),
            'week': kwargs.get('week', 1),
            'semester': kwargs.get('semester', kwargs.get('week', 1)),
            'order_index': kwargs.get('order_index', 0),
            'phase': kwargs.get('phase', ''),
            'credits': kwargs.get('credits', 3),
            'course_code': kwargs.get('course_code', ''),
            'difficulty': kwargs.get('difficulty', 'intermediate'),
            'estimated_hours': kwargs.get('estimated_hours', 2.0),
            'resources': kwargs.get('resources', []),
            'prerequisites': kwargs.get('prerequisites', []),
            'skills_gained': kwargs.get('skills_gained', []),
            'completed_skills': [],
            'status': 'not_started',
            'created_at': datetime.utcnow(),
            'completed_at': None,
        }
        result = db[cls.COLLECTION].insert_one(doc)
        doc['_id'] = result.inserted_id
        return cls(db, doc)

    @classmethod
    def find_by_id(cls, db, topic_id: str) -> 'Topic | None':
        """Find a topic by its ObjectId string."""
        try:
            doc = db[cls.COLLECTION].find_one({'_id': ObjectId(topic_id)})
            return cls(db, doc) if doc else None
        except Exception:
            return None

    @classmethod
    def find_by_curriculum(cls, db, curriculum_id: str) -> list:
        """Find all topics for a curriculum."""
        docs = db[cls.COLLECTION].find(
            {'curriculum_id': curriculum_id}
        ).sort([('week', 1), ('order_index', 1)])
        return [cls(db, doc) for doc in docs]

    def update(self, fields: dict) -> bool:
        """Update topic fields."""
        result = self._db[self.COLLECTION].update_one(
            {'_id': self._data['_id']},
            {'$set': fields}
        )
        if result.modified_count > 0:
            self._data.update(fields)
        return result.acknowledged

    def mark_completed(self) -> bool:
        """Mark this topic as completed."""
        return self.update({
            'status': 'completed',
            'completed_at': datetime.utcnow()
        })

    def set_completed_skills(self, skills: list) -> bool:
        """Update the list of completed skills for this topic."""
        return self.update({'completed_skills': skills})

    # ─── Serialization ────────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        """Convert topic to dictionary for API responses."""
        return {
            'id': self.id,
            'curriculum_id': self.curriculum_id,
            'title': self.title,
            'description': self.description,
            'week': self.week,
            'semester': self.semester,
            'phase': self.phase,
            'credits': self.credits,
            'course_code': self.course_code,
            'order_index': self.order_index,
            'difficulty': self.difficulty,
            'estimated_hours': self.estimated_hours,
            'resources': self.resources,
            'prerequisites': self.prerequisites,
            'skills_gained': self.skills_gained,
            'completed_skills': self.completed_skills,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
        }

    def __repr__(self):
        return f'<Topic {self.title}>'
