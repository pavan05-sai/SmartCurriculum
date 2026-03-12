# SmartCurriculum - Seed Data
# Initialize database with sample data for testing

from datetime import datetime, timedelta
import random


def seed_database(app):
    """
    Seed the database with sample data for testing.
    
    Args:
        app: Flask application instance
    """
    from database import db
    from models.user import User
    from models.curriculum import Curriculum, Topic
    from models.progress import Progress
    from models.skill import Skill, get_skill_category
    
    with app.app_context():
        # Check if data already exists
        if User.query.count() > 0:
            print("Database already has data. Skipping seed.")
            return
        
        print("Seeding database with sample data...")
        
        # Create sample users
        users_data = [
            {
                'email': 'john.doe@example.com',
                'password': 'password123',
                'name': 'John Doe',
                'semester': 5,
                'skill_level': 'intermediate',
                'career_goal': 'placement',
                'branch': 'Computer Science',
                'weak_subjects': ['Data Structures', 'Algorithms'],
                'strong_subjects': ['Web Development', 'Python'],
                'interests': ['AI', 'Web Development']
            },
            {
                'email': 'jane.smith@example.com',
                'password': 'password123',
                'name': 'Jane Smith',
                'semester': 3,
                'skill_level': 'beginner',
                'career_goal': 'higher_studies',
                'branch': 'Computer Science',
                'weak_subjects': ['Mathematics'],
                'strong_subjects': ['Programming'],
                'interests': ['Machine Learning', 'Research']
            },
            {
                'email': 'alex.startup@example.com',
                'password': 'password123',
                'name': 'Alex Johnson',
                'semester': 7,
                'skill_level': 'advanced',
                'career_goal': 'startup',
                'branch': 'Information Technology',
                'weak_subjects': [],
                'strong_subjects': ['Full Stack', 'DevOps'],
                'interests': ['Entrepreneurship', 'Product Development']
            },
            {
                'email': 'demo@smartcurriculum.com',
                'password': 'demo123',
                'name': 'Demo User',
                'semester': 4,
                'skill_level': 'intermediate',
                'career_goal': 'placement',
                'branch': 'Computer Science',
                'weak_subjects': ['System Design'],
                'strong_subjects': ['Python', 'SQL'],
                'interests': ['Backend Development', 'Data Science']
            }
        ]
        
        created_users = []
        for user_data in users_data:
            user = User(
                email=user_data['email'],
                password=user_data['password'],
                name=user_data['name'],
                semester=user_data['semester'],
                skill_level=user_data['skill_level'],
                career_goal=user_data['career_goal'],
                branch=user_data['branch']
            )
            user.set_weak_subjects(user_data['weak_subjects'])
            user.set_strong_subjects(user_data['strong_subjects'])
            user.set_interests(user_data['interests'])
            
            db.session.add(user)
            created_users.append(user)
        
        db.session.flush()  # Get user IDs
        
        # Create sample curriculum for each user
        curriculum_templates = [
            {
                'title': 'Full Stack Developer Path',
                'description': 'Complete curriculum to become a full stack developer',
                'difficulty': 'intermediate',
                'duration_weeks': 12,
                'career_focus': 'placement',
                'topics': [
                    {'title': 'HTML Fundamentals', 'week': 1, 'hours': 4, 'difficulty': 'beginner',
                     'skills': ['HTML', 'Web Development']},
                    {'title': 'CSS Styling & Layout', 'week': 1, 'hours': 5, 'difficulty': 'beginner',
                     'skills': ['CSS', 'Responsive Design']},
                    {'title': 'JavaScript Basics', 'week': 2, 'hours': 6, 'difficulty': 'beginner',
                     'skills': ['JavaScript', 'Programming']},
                    {'title': 'JavaScript DOM Manipulation', 'week': 2, 'hours': 4, 'difficulty': 'intermediate',
                     'skills': ['JavaScript', 'DOM']},
                    {'title': 'React Fundamentals', 'week': 3, 'hours': 8, 'difficulty': 'intermediate',
                     'skills': ['React', 'Component Architecture']},
                    {'title': 'React State Management', 'week': 4, 'hours': 6, 'difficulty': 'intermediate',
                     'skills': ['React', 'State Management']},
                    {'title': 'Node.js Basics', 'week': 5, 'hours': 6, 'difficulty': 'intermediate',
                     'skills': ['Node.js', 'Backend']},
                    {'title': 'Express.js & REST APIs', 'week': 6, 'hours': 8, 'difficulty': 'intermediate',
                     'skills': ['Express', 'REST APIs']},
                    {'title': 'Database Design with SQL', 'week': 7, 'hours': 6, 'difficulty': 'intermediate',
                     'skills': ['SQL', 'Database Design']},
                    {'title': 'MongoDB & NoSQL', 'week': 8, 'hours': 5, 'difficulty': 'intermediate',
                     'skills': ['MongoDB', 'NoSQL']},
                    {'title': 'Authentication & Security', 'week': 9, 'hours': 6, 'difficulty': 'intermediate',
                     'skills': ['Security', 'Authentication']},
                    {'title': 'Full Stack Project', 'week': 10, 'hours': 15, 'difficulty': 'advanced',
                     'skills': ['Full Stack Development', 'Project Management']},
                    {'title': 'Deployment & DevOps', 'week': 11, 'hours': 6, 'difficulty': 'intermediate',
                     'skills': ['Docker', 'Deployment', 'CI/CD']},
                    {'title': 'Interview Preparation', 'week': 12, 'hours': 8, 'difficulty': 'intermediate',
                     'skills': ['Interview Skills', 'Problem Solving']},
                ]
            },
            {
                'title': 'Data Science Foundations',
                'description': 'Build strong foundations in data science and machine learning',
                'difficulty': 'intermediate',
                'duration_weeks': 10,
                'career_focus': 'higher_studies',
                'topics': [
                    {'title': 'Python for Data Science', 'week': 1, 'hours': 6, 'difficulty': 'beginner',
                     'skills': ['Python', 'Programming']},
                    {'title': 'NumPy Fundamentals', 'week': 2, 'hours': 5, 'difficulty': 'intermediate',
                     'skills': ['NumPy', 'Numerical Computing']},
                    {'title': 'Pandas for Data Analysis', 'week': 3, 'hours': 8, 'difficulty': 'intermediate',
                     'skills': ['Pandas', 'Data Analysis']},
                    {'title': 'Data Visualization', 'week': 4, 'hours': 6, 'difficulty': 'intermediate',
                     'skills': ['Matplotlib', 'Data Visualization']},
                    {'title': 'Statistics for Data Science', 'week': 5, 'hours': 8, 'difficulty': 'intermediate',
                     'skills': ['Statistics', 'Probability']},
                    {'title': 'Machine Learning Basics', 'week': 6, 'hours': 8, 'difficulty': 'intermediate',
                     'skills': ['Machine Learning', 'Scikit-learn']},
                    {'title': 'Supervised Learning', 'week': 7, 'hours': 10, 'difficulty': 'advanced',
                     'skills': ['Classification', 'Regression']},
                    {'title': 'Unsupervised Learning', 'week': 8, 'hours': 8, 'difficulty': 'advanced',
                     'skills': ['Clustering', 'Dimensionality Reduction']},
                    {'title': 'Deep Learning Introduction', 'week': 9, 'hours': 10, 'difficulty': 'advanced',
                     'skills': ['Deep Learning', 'Neural Networks']},
                    {'title': 'Data Science Project', 'week': 10, 'hours': 15, 'difficulty': 'advanced',
                     'skills': ['Data Science', 'Project Development']},
                ]
            }
        ]
        
        for i, user in enumerate(created_users):
            template = curriculum_templates[i % len(curriculum_templates)]
            
            curriculum = Curriculum(
                user_id=user.id,
                title=template['title'],
                description=template['description'],
                difficulty=template['difficulty'],
                duration_weeks=template['duration_weeks'],
                career_focus=template['career_focus'],
                total_hours=sum(t['hours'] for t in template['topics'])
            )
            db.session.add(curriculum)
            db.session.flush()
            
            # Create topics
            for idx, topic_data in enumerate(template['topics']):
                topic = Topic(
                    curriculum_id=curriculum.id,
                    title=topic_data['title'],
                    description=f"Learn {topic_data['title']} to build your skills.",
                    week=topic_data['week'],
                    order_index=idx,
                    difficulty=topic_data['difficulty'],
                    estimated_hours=topic_data['hours']
                )
                topic.set_skills_gained(topic_data['skills'])
                topic.set_resources([
                    {'type': 'video', 'title': f'{topic_data["title"]} Tutorial', 'url': 'https://example.com'},
                    {'type': 'article', 'title': f'{topic_data["title"]} Documentation', 'url': 'https://docs.example.com'}
                ])
                db.session.add(topic)
                
                # Create some progress for demo user
                if user.email == 'demo@smartcurriculum.com' and idx < 5:
                    db.session.flush()
                    progress = Progress(
                        user_id=user.id,
                        topic_id=topic.id,
                        status='completed' if idx < 3 else 'in_progress',
                        score=random.randint(70, 100) if idx < 3 else 0,
                        time_spent=random.randint(120, 300) if idx < 3 else 30,
                        completion_percentage=100 if idx < 3 else random.randint(20, 60)
                    )
                    if idx < 3:
                        progress.complete(progress.score)
                    else:
                        progress.start()
                    db.session.add(progress)
                    
                    # Add skills for completed topics
                    if idx < 3:
                        for skill_name in topic_data['skills']:
                            existing_skill = Skill.query.filter_by(
                                user_id=user.id,
                                name=skill_name
                            ).first()
                            if not existing_skill:
                                skill = Skill(
                                    user_id=user.id,
                                    name=skill_name,
                                    category=get_skill_category(skill_name),
                                    level='intermediate',
                                    proficiency_score=random.randint(50, 80),
                                    source='curriculum'
                                )
                                skill.generate_resume_bullet()
                                db.session.add(skill)
        
        # Commit all changes
        db.session.commit()
        print(f"Seeded {len(created_users)} users with curricula and progress data.")
        print("\nDemo account: demo@smartcurriculum.com / demo123")


def clear_database(app):
    """
    Clear all data from the database.
    
    Args:
        app: Flask application instance
    """
    from database import db
    from models import User, Curriculum, Topic, Progress, Skill
    
    with app.app_context():
        Progress.query.delete()
        Skill.query.delete()
        Topic.query.delete()
        Curriculum.query.delete()
        User.query.delete()
        db.session.commit()
        print("Database cleared.")


if __name__ == '__main__':
    # Run seeding from command line
    import sys
    sys.path.insert(0, '..')
    
    from app import app
    
    if len(sys.argv) > 1 and sys.argv[1] == '--clear':
        clear_database(app)
    else:
        seed_database(app)
