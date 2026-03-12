# SmartCurriculum - User Model
# Handles user registration, authentication, and profile data

from datetime import datetime
from database import db
import bcrypt
import json


class User(db.Model):
    """
    User model representing students in the system.
    
    Stores user credentials, profile information, and learning preferences.
    The profile data is used by the AI engine to personalize curricula.
    """
    
    __tablename__ = 'users'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Authentication fields
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Profile fields
    name = db.Column(db.String(255), nullable=False)
    semester = db.Column(db.Integer, default=1)  # 1-8 for typical engineering
    skill_level = db.Column(db.String(50), default='beginner')  # beginner, intermediate, advanced
    
    # Learning preferences (stored as JSON string for flexibility)
    weak_subjects = db.Column(db.Text, default='[]')  # JSON array of subject names
    strong_subjects = db.Column(db.Text, default='[]')  # JSON array of subject names
    
    # Career goal: 'placement', 'higher_studies', 'startup', 'research'
    career_goal = db.Column(db.String(100), default='placement')
    
    # Learning pace: 'slow', 'moderate', 'fast'
    learning_pace = db.Column(db.String(50), default='moderate')
    
    # Additional profile data
    branch = db.Column(db.String(100), default='Computer Science')  # Engineering branch
    interests = db.Column(db.Text, default='[]')  # JSON array of interests
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    curricula = db.relationship('Curriculum', backref='user', lazy=True, cascade='all, delete-orphan')
    skills = db.relationship('Skill', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, email, password, name, **kwargs):
        """
        Create a new user with hashed password.
        
        Args:
            email: User's email address
            password: Plain text password (will be hashed)
            name: User's display name
            **kwargs: Additional profile fields
        """
        self.email = email.lower().strip()
        self.set_password(password)
        self.name = name
        
        # Set optional fields from kwargs
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def set_password(self, password):
        """Hash and store the password securely using bcrypt."""
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, password):
        """Verify a password against the stored hash."""
        with open('debug_log.txt', 'a') as f:
            f.write(f">>> DEBUG: check_password called for user: {self.email}\n")
            f.flush()
            try:
                result = bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
                f.write(f">>> DEBUG: bcrypt.checkpw result: {result}\n")
                f.flush()
                return result
            except Exception as e:
                f.write(f">>> DEBUG: ERROR in check_password: {str(e)}\n")
                f.flush()
                raise e
    
    def get_weak_subjects(self):
        """Return weak subjects as a Python list."""
        try:
            return json.loads(self.weak_subjects) if self.weak_subjects else []
        except json.JSONDecodeError:
            return []
    
    def set_weak_subjects(self, subjects):
        """Store weak subjects as JSON."""
        self.weak_subjects = json.dumps(subjects)
    
    def get_strong_subjects(self):
        """Return strong subjects as a Python list."""
        try:
            return json.loads(self.strong_subjects) if self.strong_subjects else []
        except json.JSONDecodeError:
            return []
    
    def set_strong_subjects(self, subjects):
        """Store strong subjects as JSON."""
        self.strong_subjects = json.dumps(subjects)
    
    def get_interests(self):
        """Return interests as a Python list."""
        try:
            return json.loads(self.interests) if self.interests else []
        except json.JSONDecodeError:
            return []
    
    def set_interests(self, interests_list):
        """Store interests as JSON."""
        self.interests = json.dumps(interests_list)
    
    def to_dict(self, include_sensitive=False):
        """
        Convert user to dictionary for API responses.
        
        Args:
            include_sensitive: If True, includes email (for profile page)
        """
        data = {
            'id': self.id,
            'name': self.name,
            'semester': self.semester,
            'skill_level': self.skill_level,
            'weak_subjects': self.get_weak_subjects(),
            'strong_subjects': self.get_strong_subjects(),
            'career_goal': self.career_goal,
            'learning_pace': self.learning_pace,
            'branch': self.branch,
            'interests': self.get_interests(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_sensitive:
            data['email'] = self.email
        
        return data
    
    def __repr__(self):
        return f'<User {self.email}>'
