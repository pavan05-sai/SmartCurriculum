# SmartCurriculum - User Model (MongoDB)
# Handles user registration, authentication, and profile data

from datetime import datetime
from bson import ObjectId
import bcrypt
import logging

logger = logging.getLogger(__name__)


class User:
    """
    User model for MongoDB.

    Stores user credentials, profile information, and learning preferences.
    The profile data is used by the AI engine to personalize curricula.
    """

    COLLECTION = 'users'

    def __init__(self, db, data: dict):
        """Initialize User from a MongoDB document dict."""
        self._db = db
        self._data = data

    # ─── Properties ───────────────────────────────────────────────────────────

    @property
    def id(self):
        return str(self._data.get('_id', ''))

    @property
    def email(self):
        return self._data.get('email', '')

    @property
    def name(self):
        return self._data.get('name', '')

    @property
    def semester(self):
        return self._data.get('semester', 1)

    @property
    def skill_level(self):
        return self._data.get('skill_level', 'beginner')

    @property
    def weak_subjects(self):
        return self._data.get('weak_subjects', [])

    @property
    def strong_subjects(self):
        return self._data.get('strong_subjects', [])

    @property
    def career_goal(self):
        return self._data.get('career_goal', 'placement')

    @property
    def learning_pace(self):
        return self._data.get('learning_pace', 'moderate')

    @property
    def branch(self):
        return self._data.get('branch', 'Computer Science')

    @property
    def interests(self):
        return self._data.get('interests', [])

    @property
    def created_at(self):
        return self._data.get('created_at')

    @property
    def password_hash(self):
        return self._data.get('password_hash', '')

    # ─── Password Helpers ─────────────────────────────────────────────────────

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a plain-text password using bcrypt."""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password: str) -> bool:
        """Verify a password against the stored bcrypt hash."""
        try:
            return bcrypt.checkpw(
                password.encode('utf-8'),
                self.password_hash.encode('utf-8')
            )
        except Exception as e:
            logger.error(f"Password check error for {self.email}: {e}")
            return False

    # ─── CRUD Class Methods ───────────────────────────────────────────────────

    @classmethod
    def create(cls, db, email: str, password: str, name: str, **kwargs) -> 'User':
        """
        Insert a new user document into MongoDB.

        Args:
            db: PyMongo database instance
            email: User email (stored lowercase)
            password: Plain-text password (hashed before storage)
            name: Display name
            **kwargs: Additional profile fields

        Returns:
            User instance
        """
        doc = {
            'email': email.lower().strip(),
            'password_hash': cls.hash_password(password),
            'name': name,
            'semester': kwargs.get('semester', 1),
            'skill_level': kwargs.get('skill_level', 'beginner'),
            'weak_subjects': kwargs.get('weak_subjects', []),
            'strong_subjects': kwargs.get('strong_subjects', []),
            'career_goal': kwargs.get('career_goal', 'placement'),
            'learning_pace': kwargs.get('learning_pace', 'moderate'),
            'branch': kwargs.get('branch', 'Computer Science'),
            'interests': kwargs.get('interests', []),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
        }
        result = db[cls.COLLECTION].insert_one(doc)
        doc['_id'] = result.inserted_id
        return cls(db, doc)

    @classmethod
    def find_by_email(cls, db, email: str) -> 'User | None':
        """Find a user by email address."""
        doc = db[cls.COLLECTION].find_one({'email': email.lower().strip()})
        return cls(db, doc) if doc else None

    @classmethod
    def find_by_id(cls, db, user_id: str) -> 'User | None':
        """Find a user by string ObjectId."""
        try:
            doc = db[cls.COLLECTION].find_one({'_id': ObjectId(user_id)})
            return cls(db, doc) if doc else None
        except Exception:
            return None

    def update(self, fields: dict) -> bool:
        """
        Update user fields in MongoDB.

        Args:
            fields: Dictionary of fields to update

        Returns:
            True if successful
        """
        fields['updated_at'] = datetime.utcnow()
        result = self._db[self.COLLECTION].update_one(
            {'_id': self._data['_id']},
            {'$set': fields}
        )
        if result.modified_count > 0:
            self._data.update(fields)
        return result.acknowledged

    def set_password(self, new_password: str):
        """Hash and update the password."""
        new_hash = self.hash_password(new_password)
        self.update({'password_hash': new_hash})

    # ─── Serialization ────────────────────────────────────────────────────────

    def to_dict(self, include_sensitive: bool = False) -> dict:
        """
        Convert user to dictionary for API responses.

        Args:
            include_sensitive: If True, includes email.
        """
        data = {
            'id': self.id,
            'name': self.name,
            'semester': self.semester,
            'skill_level': self.skill_level,
            'weak_subjects': self.weak_subjects,
            'strong_subjects': self.strong_subjects,
            'career_goal': self.career_goal,
            'learning_pace': self.learning_pace,
            'branch': self.branch,
            'interests': self.interests,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

        if include_sensitive:
            data['email'] = self.email

        return data

    def __repr__(self):
        return f'<User {self.email}>'
