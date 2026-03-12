# SmartCurriculum - Skill Model
# Tracks skills acquired by users for resume mapping

from datetime import datetime
from database import db


class Skill(db.Model):
    """
    Skill model for tracking user-acquired skills.
    
    Skills are gained by completing topics and are used for:
    1. Resume skill mapping - generating resume bullet points
    2. Skill gap analysis - comparing with job requirements
    3. Proficiency tracking - monitoring skill development
    """
    
    __tablename__ = 'skills'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign key to user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Skill details
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100))  # e.g., 'programming', 'data_science', 'web_dev'
    
    # Proficiency level: 'beginner', 'intermediate', 'advanced', 'expert'
    level = db.Column(db.String(50), default='beginner')
    
    # Proficiency score (0-100) for more granular tracking
    proficiency_score = db.Column(db.Integer, default=0)
    
    # Source of the skill (how it was acquired)
    # e.g., 'curriculum', 'project', 'certification', 'self_declared'
    source = db.Column(db.String(100), default='curriculum')
    
    # The topic ID that granted this skill (if from curriculum)
    source_topic_id = db.Column(db.Integer)
    
    # Resume bullet point - auto-generated or user-edited
    resume_bullet = db.Column(db.Text)
    
    # Whether this skill is verified (e.g., through assessment)
    is_verified = db.Column(db.Boolean, default=False)
    
    # Whether to show this skill on resume
    show_on_resume = db.Column(db.Boolean, default=True)
    
    # Timestamps
    acquired_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, user_id, name, **kwargs):
        """
        Create a new skill record.
        
        Args:
            user_id: ID of the user
            name: Name of the skill
            **kwargs: Additional fields
        """
        self.user_id = user_id
        self.name = name
        
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def update_proficiency(self, score):
        """
        Update proficiency score and adjust level accordingly.
        
        Args:
            score: New proficiency score (0-100)
        """
        self.proficiency_score = max(0, min(100, score))
        
        # Auto-update level based on score
        if self.proficiency_score >= 90:
            self.level = 'expert'
        elif self.proficiency_score >= 70:
            self.level = 'advanced'
        elif self.proficiency_score >= 40:
            self.level = 'intermediate'
        else:
            self.level = 'beginner'
    
    def generate_resume_bullet(self):
        """
        Generate a default resume bullet point for this skill.
        Can be overridden by user or LLM-generated content.
        """
        level_descriptions = {
            'beginner': 'Familiar with',
            'intermediate': 'Proficient in',
            'advanced': 'Experienced with',
            'expert': 'Expert-level proficiency in'
        }
        
        description = level_descriptions.get(self.level, 'Knowledge of')
        self.resume_bullet = f"{description} {self.name}"
        return self.resume_bullet
    
    def verify(self):
        """Mark this skill as verified."""
        self.is_verified = True
    
    def to_dict(self):
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
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Skill {self.name} ({self.level})>'


# Predefined skill categories for organization
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


def get_skill_category(skill_name):
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
