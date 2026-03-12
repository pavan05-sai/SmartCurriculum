# SmartCurriculum - Curriculum and Topic Models
# Handles personalized curriculum and learning topics

from datetime import datetime
from database import db
import json


class Curriculum(db.Model):
    """
    Curriculum model representing a personalized learning plan.
    
    Each user can have multiple curricula (e.g., for different semesters or goals).
    A curriculum contains multiple topics organized by week.
    """
    
    __tablename__ = 'curricula'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign key to user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Curriculum details
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    
    # Curriculum metadata
    difficulty = db.Column(db.String(50), default='intermediate')  # beginner, intermediate, advanced
    duration_weeks = db.Column(db.Integer, default=12)  # Total duration in weeks
    career_focus = db.Column(db.String(100))  # The career goal this curriculum targets
    
    # Total estimated hours for the entire curriculum
    total_hours = db.Column(db.Integer, default=0)
    
    # Status: 'draft', 'active', 'completed', 'archived'
    status = db.Column(db.String(50), default='active')
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    topics = db.relationship('Topic', backref='curriculum', lazy=True, 
                           cascade='all, delete-orphan', order_by='Topic.week, Topic.order_index')
    
    def __init__(self, user_id, title, **kwargs):
        """
        Create a new curriculum.
        
        Args:
            user_id: ID of the user this curriculum belongs to
            title: Title of the curriculum
            **kwargs: Additional fields
        """
        self.user_id = user_id
        self.title = title
        
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def get_topics_by_week(self):
        """
        Get topics organized by week number.
        
        Returns:
            Dictionary with week numbers as keys and lists of topics as values
        """
        topics_by_week = {}
        for topic in self.topics:
            week = topic.week or 1
            if week not in topics_by_week:
                topics_by_week[week] = []
            topics_by_week[week].append(topic.to_dict())
        return topics_by_week
    
    def calculate_progress(self):
        """
        Calculate overall progress percentage for this curriculum.
        
        Returns:
            Float between 0 and 100 representing completion percentage
        """
        if not self.topics:
            return 0.0
        
        completed = sum(1 for t in self.topics if t.status == 'completed')
        return round((completed / len(self.topics)) * 100, 1)
    
    def to_dict(self, include_topics=False):
        """
        Convert curriculum to dictionary for API responses.
        
        Args:
            include_topics: If True, includes all topics in the response
        """
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
            'topic_count': len(self.topics),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_topics:
            data['topics'] = [t.to_dict() for t in self.topics]
            data['topics_by_week'] = self.get_topics_by_week()
        
        return data
    
    def __repr__(self):
        return f'<Curriculum {self.title}>'


class Topic(db.Model):
    """
    Topic model representing a single learning topic within a curriculum.
    
    Topics are the individual learning units that students work through.
    They contain resources, estimated time, and track completion status.
    """
    
    __tablename__ = 'topics'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign key to curriculum
    curriculum_id = db.Column(db.Integer, db.ForeignKey('curricula.id'), nullable=False, index=True)
    
    # Topic details
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    
    # Organization
    week = db.Column(db.Integer, default=1)  # Which week this topic is in
    semester = db.Column(db.Integer, default=1)  # Explicit semester number
    order_index = db.Column(db.Integer, default=0)  # Order within the week
    phase = db.Column(db.String(100))  # Phase name (e.g., Foundation, Core)
    
    # Academic details
    credits = db.Column(db.Integer, default=3)
    course_code = db.Column(db.String(20))
    
    # Learning metadata
    difficulty = db.Column(db.String(50), default='intermediate')
    estimated_hours = db.Column(db.Float, default=2.0)  # Estimated time to complete
    
    # Resources stored as JSON
    # Format: [{"type": "video", "title": "...", "url": "..."}, ...]
    resources = db.Column(db.Text, default='[]')
    
    # Prerequisites stored as JSON array of topic IDs
    prerequisites = db.Column(db.Text, default='[]')
    
    # Skills that will be gained from this topic (JSON array)
    skills_gained = db.Column(db.Text, default='[]')
    
    # Skills that have been completed (JSON array)
    completed_skills = db.Column(db.Text, default='[]')
    
    # Status: 'not_started', 'in_progress', 'completed'
    status = db.Column(db.String(50), default='not_started')
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def __init__(self, curriculum_id, title, **kwargs):
        """
        Create a new topic.
        
        Args:
            curriculum_id: ID of the parent curriculum
            title: Title of the topic
            **kwargs: Additional fields
        """
        self.curriculum_id = curriculum_id
        self.title = title
        
        # Set defaults if not provided in kwargs
        if 'credits' not in kwargs:
            self.credits = 3
        if 'semester' not in kwargs:
            self.semester = kwargs.get('week', 1)
        
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def get_resources(self):
        """Return resources as a Python list."""
        try:
            return json.loads(self.resources) if self.resources else []
        except json.JSONDecodeError:
            return []
    
    def set_resources(self, resources_list):
        """Store resources as JSON."""
        self.resources = json.dumps(resources_list)
    
    def get_prerequisites(self):
        """Return prerequisites as a Python list."""
        try:
            return json.loads(self.prerequisites) if self.prerequisites else []
        except json.JSONDecodeError:
            return []
    
    def set_prerequisites(self, prereq_list):
        """Store prerequisites as JSON."""
        self.prerequisites = json.dumps(prereq_list)
    
    def get_skills_gained(self):
        """Return skills gained as a Python list."""
        try:
            return json.loads(self.skills_gained) if self.skills_gained else []
        except json.JSONDecodeError:
            return []
    
    def set_skills_gained(self, skills_list):
        """Store skills gained as JSON."""
        self.skills_gained = json.dumps(skills_list)
    
    def mark_completed(self):
        """Mark this topic as completed."""
        self.status = 'completed'
        self.completed_at = datetime.utcnow()
    
    def to_dict(self):
        """Convert topic to dictionary for API responses."""
        return {
            'id': self.id,
            'curriculum_id': self.curriculum_id,
            'title': self.title,
            'description': self.description,
            'week': self.week,
            'semester': self.semester or self.week,
            'phase': self.phase,
            'credits': self.credits,
            'course_code': self.course_code,
            'order_index': self.order_index,
            'difficulty': self.difficulty,
            'estimated_hours': self.estimated_hours,
            'resources': self.get_resources(),
            'prerequisites': self.get_prerequisites(),
            'skills_gained': self.get_skills_gained(),
            'completed_skills': self.get_completed_skills(),
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

    def get_completed_skills(self):
        """Return completed skills as a Python list."""
        try:
            return json.loads(self.completed_skills) if self.completed_skills else []
        except json.JSONDecodeError:
            return []

    def set_completed_skills(self, skills_list):
        """Store completed skills as JSON."""
        self.completed_skills = json.dumps(skills_list)

    
    def __repr__(self):
        return f'<Topic {self.title}>'
