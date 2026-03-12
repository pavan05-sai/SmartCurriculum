# SmartCurriculum - Curriculum Recommender
# AI-powered recommendation system for personalized curriculum generation

import random
from typing import Dict, List, Optional


class CurriculumRecommender:
    """
    Recommendation system for generating personalized curricula.
    
    Uses content-based filtering and rule-based logic to create
    curricula tailored to the user's profile, goals, and skill level.
    """
    
    def __init__(self):
        """Initialize the recommender with topic database."""
        self.topic_database = self._load_topic_database()
        self.career_paths = self._load_career_paths()
    
    def _load_topic_database(self) -> Dict:
        """
        Load comprehensive topic database organized by skill area.
        In production, this would come from a database or external API.
        """
        return {
            'programming_fundamentals': [
                {
                    'title': 'Introduction to Programming Concepts',
                    'description': 'Learn basic programming concepts: variables, data types, operators',
                    'difficulty': 'beginner',
                    'estimated_hours': 4,
                    'skills_gained': ['Programming Basics', 'Logical Thinking'],
                    'resources': [
                        {'type': 'video', 'title': 'Programming Fundamentals', 'url': 'https://example.com/prog-basics'},
                        {'type': 'article', 'title': 'Getting Started with Programming', 'url': 'https://example.com/start-prog'}
                    ]
                },
                {
                    'title': 'Control Flow and Loops',
                    'description': 'Master conditional statements, loops, and flow control',
                    'difficulty': 'beginner',
                    'estimated_hours': 5,
                    'skills_gained': ['Control Flow', 'Loops', 'Algorithm Design'],
                    'resources': []
                },
                {
                    'title': 'Functions and Modularity',
                    'description': 'Learn to write reusable code with functions',
                    'difficulty': 'beginner',
                    'estimated_hours': 4,
                    'skills_gained': ['Functions', 'Code Organization'],
                    'resources': []
                },
                {
                    'title': 'Object-Oriented Programming',
                    'description': 'Master OOP concepts: classes, objects, inheritance',
                    'difficulty': 'intermediate',
                    'estimated_hours': 8,
                    'skills_gained': ['OOP', 'Classes', 'Inheritance'],
                    'resources': []
                }
            ],
            'python': [
                {
                    'title': 'Python Basics',
                    'description': 'Introduction to Python syntax and core features',
                    'difficulty': 'beginner',
                    'estimated_hours': 6,
                    'skills_gained': ['Python', 'Scripting'],
                    'resources': []
                },
                {
                    'title': 'Python Data Structures',
                    'description': 'Lists, dictionaries, sets, and tuples in Python',
                    'difficulty': 'beginner',
                    'estimated_hours': 5,
                    'skills_gained': ['Python Data Structures', 'Collections'],
                    'resources': []
                },
                {
                    'title': 'Python File Handling',
                    'description': 'Reading and writing files in Python',
                    'difficulty': 'intermediate',
                    'estimated_hours': 3,
                    'skills_gained': ['File I/O', 'Python'],
                    'resources': []
                },
                {
                    'title': 'Python Advanced Topics',
                    'description': 'Decorators, generators, context managers',
                    'difficulty': 'advanced',
                    'estimated_hours': 6,
                    'skills_gained': ['Advanced Python', 'Decorators'],
                    'resources': []
                }
            ],
            'web_development': [
                {
                    'title': 'HTML Fundamentals',
                    'description': 'Structure web pages with HTML5',
                    'difficulty': 'beginner',
                    'estimated_hours': 4,
                    'skills_gained': ['HTML', 'Web Development'],
                    'resources': []
                },
                {
                    'title': 'CSS Styling',
                    'description': 'Style web pages with modern CSS',
                    'difficulty': 'beginner',
                    'estimated_hours': 6,
                    'skills_gained': ['CSS', 'Responsive Design'],
                    'resources': []
                },
                {
                    'title': 'JavaScript Essentials',
                    'description': 'Add interactivity with JavaScript',
                    'difficulty': 'intermediate',
                    'estimated_hours': 8,
                    'skills_gained': ['JavaScript', 'DOM Manipulation'],
                    'resources': []
                },
                {
                    'title': 'React.js Fundamentals',
                    'description': 'Build modern UIs with React',
                    'difficulty': 'intermediate',
                    'estimated_hours': 10,
                    'skills_gained': ['React', 'Component Architecture'],
                    'resources': []
                },
                {
                    'title': 'Backend Development with Node.js',
                    'description': 'Create server-side applications',
                    'difficulty': 'intermediate',
                    'estimated_hours': 8,
                    'skills_gained': ['Node.js', 'Express', 'REST APIs'],
                    'resources': []
                },
                {
                    'title': 'Full Stack Project',
                    'description': 'Build a complete web application',
                    'difficulty': 'advanced',
                    'estimated_hours': 15,
                    'skills_gained': ['Full Stack Development', 'Project Management'],
                    'resources': []
                }
            ],
            'data_science': [
                {
                    'title': 'Introduction to Data Science',
                    'description': 'Overview of data science workflow and tools',
                    'difficulty': 'beginner',
                    'estimated_hours': 4,
                    'skills_gained': ['Data Science', 'Analytics'],
                    'resources': []
                },
                {
                    'title': 'NumPy for Numerical Computing',
                    'description': 'Master numerical operations with NumPy',
                    'difficulty': 'intermediate',
                    'estimated_hours': 5,
                    'skills_gained': ['NumPy', 'Numerical Computing'],
                    'resources': []
                },
                {
                    'title': 'Pandas for Data Analysis',
                    'description': 'Data manipulation and analysis with Pandas',
                    'difficulty': 'intermediate',
                    'estimated_hours': 8,
                    'skills_gained': ['Pandas', 'Data Analysis'],
                    'resources': []
                },
                {
                    'title': 'Data Visualization',
                    'description': 'Create compelling visualizations with Matplotlib and Seaborn',
                    'difficulty': 'intermediate',
                    'estimated_hours': 6,
                    'skills_gained': ['Data Visualization', 'Matplotlib'],
                    'resources': []
                },
                {
                    'title': 'Statistical Analysis',
                    'description': 'Apply statistical methods to data',
                    'difficulty': 'intermediate',
                    'estimated_hours': 8,
                    'skills_gained': ['Statistics', 'Hypothesis Testing'],
                    'resources': []
                }
            ],
            'machine_learning': [
                {
                    'title': 'Introduction to Machine Learning',
                    'description': 'Fundamentals of ML algorithms and concepts',
                    'difficulty': 'intermediate',
                    'estimated_hours': 6,
                    'skills_gained': ['Machine Learning', 'AI Fundamentals'],
                    'resources': []
                },
                {
                    'title': 'Supervised Learning',
                    'description': 'Classification and regression algorithms',
                    'difficulty': 'intermediate',
                    'estimated_hours': 10,
                    'skills_gained': ['Supervised Learning', 'Scikit-learn'],
                    'resources': []
                },
                {
                    'title': 'Unsupervised Learning',
                    'description': 'Clustering and dimensionality reduction',
                    'difficulty': 'intermediate',
                    'estimated_hours': 8,
                    'skills_gained': ['Unsupervised Learning', 'Clustering'],
                    'resources': []
                },
                {
                    'title': 'Deep Learning Fundamentals',
                    'description': 'Neural networks and deep learning basics',
                    'difficulty': 'advanced',
                    'estimated_hours': 12,
                    'skills_gained': ['Deep Learning', 'Neural Networks'],
                    'resources': []
                },
                {
                    'title': 'Natural Language Processing',
                    'description': 'Process and analyze text data',
                    'difficulty': 'advanced',
                    'estimated_hours': 10,
                    'skills_gained': ['NLP', 'Text Analysis'],
                    'resources': []
                }
            ],
            'databases': [
                {
                    'title': 'Database Fundamentals',
                    'description': 'Understanding relational databases',
                    'difficulty': 'beginner',
                    'estimated_hours': 4,
                    'skills_gained': ['Database Concepts', 'Data Modeling'],
                    'resources': []
                },
                {
                    'title': 'SQL Basics',
                    'description': 'Query databases with SQL',
                    'difficulty': 'beginner',
                    'estimated_hours': 6,
                    'skills_gained': ['SQL', 'Database Queries'],
                    'resources': []
                },
                {
                    'title': 'Advanced SQL',
                    'description': 'Complex queries, joins, and optimization',
                    'difficulty': 'intermediate',
                    'estimated_hours': 6,
                    'skills_gained': ['Advanced SQL', 'Query Optimization'],
                    'resources': []
                },
                {
                    'title': 'NoSQL Databases',
                    'description': 'Working with MongoDB and document databases',
                    'difficulty': 'intermediate',
                    'estimated_hours': 5,
                    'skills_gained': ['MongoDB', 'NoSQL'],
                    'resources': []
                }
            ],
            'devops': [
                {
                    'title': 'Version Control with Git',
                    'description': 'Master Git for code management',
                    'difficulty': 'beginner',
                    'estimated_hours': 4,
                    'skills_gained': ['Git', 'Version Control'],
                    'resources': []
                },
                {
                    'title': 'Linux Command Line',
                    'description': 'Essential Linux commands for developers',
                    'difficulty': 'beginner',
                    'estimated_hours': 5,
                    'skills_gained': ['Linux', 'Command Line'],
                    'resources': []
                },
                {
                    'title': 'Docker Fundamentals',
                    'description': 'Containerize applications with Docker',
                    'difficulty': 'intermediate',
                    'estimated_hours': 6,
                    'skills_gained': ['Docker', 'Containerization'],
                    'resources': []
                },
                {
                    'title': 'CI/CD Pipelines',
                    'description': 'Automate deployment with CI/CD',
                    'difficulty': 'intermediate',
                    'estimated_hours': 6,
                    'skills_gained': ['CI/CD', 'DevOps'],
                    'resources': []
                },
                {
                    'title': 'Cloud Services (AWS)',
                    'description': 'Deploy applications on AWS',
                    'difficulty': 'advanced',
                    'estimated_hours': 10,
                    'skills_gained': ['AWS', 'Cloud Computing'],
                    'resources': []
                }
            ],
            'soft_skills': [
                {
                    'title': 'Problem Solving Techniques',
                    'description': 'Systematic approaches to problem solving',
                    'difficulty': 'beginner',
                    'estimated_hours': 3,
                    'skills_gained': ['Problem Solving', 'Critical Thinking'],
                    'resources': []
                },
                {
                    'title': 'Technical Communication',
                    'description': 'Write effective technical documentation',
                    'difficulty': 'intermediate',
                    'estimated_hours': 4,
                    'skills_gained': ['Technical Writing', 'Communication'],
                    'resources': []
                },
                {
                    'title': 'Interview Preparation',
                    'description': 'Prepare for technical interviews',
                    'difficulty': 'intermediate',
                    'estimated_hours': 8,
                    'skills_gained': ['Interview Skills', 'Coding Interviews'],
                    'resources': []
                }
            ]
        }
    
    def _load_career_paths(self) -> Dict:
        """
        Define recommended learning paths for different career goals.
        """
        return {
            'placement': {
                'priority_areas': ['programming_fundamentals', 'python', 'databases', 'web_development', 'soft_skills'],
                'title': 'Placement-Ready Developer Path',
                'description': 'Comprehensive curriculum to prepare for software development roles'
            },
            'higher_studies': {
                'priority_areas': ['programming_fundamentals', 'python', 'data_science', 'machine_learning', 'databases'],
                'title': 'Research & Higher Studies Path',
                'description': 'Strong foundation for MS/PhD and research oriented career'
            },
            'startup': {
                'priority_areas': ['web_development', 'python', 'databases', 'devops', 'soft_skills'],
                'title': 'Startup Developer Path',
                'description': 'Full-stack skills for building and launching products quickly'
            },
            'research': {
                'priority_areas': ['python', 'data_science', 'machine_learning', 'programming_fundamentals'],
                'title': 'AI/ML Research Path',
                'description': 'Deep dive into machine learning and AI research'
            }
        }
    
    def generate_curriculum(
        self,
        user,
        focus_areas: Optional[List[str]] = None,
        duration_weeks: int = 12,
        hours_per_week: int = 10
    ) -> Dict:
        """
        Generate a personalized curriculum based on user profile.
        
        Args:
            user: User model instance with profile data
            focus_areas: Optional list of specific areas to focus on
            duration_weeks: Total duration in weeks
            hours_per_week: Estimated study hours per week
            
        Returns:
            Dictionary containing curriculum details and topics
        """
        # Get career path configuration
        career_goal = user.career_goal or 'placement'
        career_config = self.career_paths.get(career_goal, self.career_paths['placement'])
        
        # Determine priority areas
        if focus_areas:
            priority_areas = focus_areas
        else:
            priority_areas = career_config['priority_areas']
        
        # Adjust difficulty based on user's skill level
        skill_level = user.skill_level or 'beginner'
        difficulty_mapping = {
            'beginner': ['beginner', 'intermediate'],
            'intermediate': ['intermediate', 'advanced'],
            'advanced': ['advanced', 'intermediate']
        }
        allowed_difficulties = difficulty_mapping.get(skill_level, ['beginner', 'intermediate'])
        
        # Calculate total available hours
        total_hours = duration_weeks * hours_per_week
        
        # Collect topics from priority areas
        selected_topics = []
        hours_allocated = 0
        
        for area in priority_areas:
            if area in self.topic_database:
                area_topics = self.topic_database[area]
                
                for topic in area_topics:
                    # Filter by difficulty
                    if topic['difficulty'] in allowed_difficulties:
                        # Check if we have hours left
                        if hours_allocated + topic['estimated_hours'] <= total_hours:
                            selected_topics.append(topic.copy())
                            hours_allocated += topic['estimated_hours']
        
        # If user has weak subjects, add related topics
        weak_subjects = user.get_weak_subjects() if hasattr(user, 'get_weak_subjects') else []
        for weak in weak_subjects:
            weak_lower = weak.lower()
            for area, topics in self.topic_database.items():
                if weak_lower in area.lower():
                    for topic in topics[:2]:  # Add first 2 topics from weak areas
                        if topic not in selected_topics and hours_allocated + topic['estimated_hours'] <= total_hours:
                            selected_topics.append(topic.copy())
                            hours_allocated += topic['estimated_hours']
        
        # Organize topics into weeks
        weekly_topics = self._organize_by_week(selected_topics, duration_weeks)
        
        # Build curriculum data
        curriculum = {
            'title': f"{career_config['title']} ({duration_weeks} Weeks)",
            'description': career_config['description'],
            'difficulty': skill_level,
            'duration_weeks': duration_weeks,
            'total_hours': hours_allocated,
            'topics': weekly_topics
        }
        
        return curriculum
    
    def _organize_by_week(self, topics: List[Dict], duration_weeks: int) -> List[Dict]:
        """
        Organize topics into weekly schedule.
        """
        weekly_topics = []
        topics_per_week = max(1, len(topics) // duration_weeks)
        
        for i, topic in enumerate(topics):
            week = min((i // topics_per_week) + 1, duration_weeks)
            order_in_week = i % topics_per_week
            
            topic_with_schedule = {
                **topic,
                'week': week,
                'order_index': order_in_week
            }
            weekly_topics.append(topic_with_schedule)
        
        return weekly_topics
    
    def analyze_skill_gap(
        self,
        user,
        target_role: str,
        current_skills: List[str],
        job_description: Optional[str] = None
    ) -> Dict:
        """
        Analyze the gap between current skills and target role requirements.
        
        Args:
            user: User model instance
            target_role: Target job role
            current_skills: List of current skill names
            job_description: Optional job description for deeper analysis
            
        Returns:
            Skill gap analysis with recommendations
        """
        # Define required skills for common roles
        role_requirements = {
            'placement': {
                'required': ['Python', 'Data Structures', 'Algorithms', 'SQL', 'Git'],
                'preferred': ['JavaScript', 'React', 'System Design', 'CI/CD']
            },
            'Full Stack Developer': {
                'required': ['HTML', 'CSS', 'JavaScript', 'React', 'Node.js', 'SQL'],
                'preferred': ['TypeScript', 'MongoDB', 'Docker', 'AWS']
            },
            'Data Scientist': {
                'required': ['Python', 'Pandas', 'NumPy', 'Machine Learning', 'SQL'],
                'preferred': ['Deep Learning', 'TensorFlow', 'Statistics', 'Data Visualization']
            },
            'Backend Developer': {
                'required': ['Python', 'SQL', 'REST APIs', 'Git', 'Linux'],
                'preferred': ['Docker', 'Microservices', 'Redis', 'Message Queues']
            },
            'higher_studies': {
                'required': ['Research Skills', 'Statistics', 'Python', 'Machine Learning'],
                'preferred': ['Academic Writing', 'Deep Learning', 'Mathematics']
            },
            'startup': {
                'required': ['Full Stack Development', 'JavaScript', 'Python', 'Git'],
                'preferred': ['Product Thinking', 'DevOps', 'Agile', 'Leadership']
            }
        }
        
        # Get requirements for target role
        requirements = role_requirements.get(
            target_role, 
            role_requirements.get('placement', {'required': [], 'preferred': []})
        )
        
        # Normalize current skills for comparison
        current_skills_lower = {s.lower() for s in current_skills}
        
        # Find gaps
        missing_required = []
        missing_preferred = []
        matching_skills = []
        
        for skill in requirements['required']:
            if skill.lower() in current_skills_lower or any(skill.lower() in cs for cs in current_skills_lower):
                matching_skills.append(skill)
            else:
                missing_required.append(skill)
        
        for skill in requirements['preferred']:
            if skill.lower() not in current_skills_lower and not any(skill.lower() in cs for cs in current_skills_lower):
                missing_preferred.append(skill)
        
        # Calculate readiness score
        total_required = len(requirements['required'])
        matched_required = len(matching_skills)
        readiness_score = (matched_required / total_required * 100) if total_required > 0 else 0
        
        # Generate recommendations
        recommendations = []
        for skill in missing_required[:3]:  # Top 3 priority
            recommendations.append({
                'skill': skill,
                'priority': 'high',
                'reason': f'{skill} is required for {target_role}'
            })
        
        for skill in missing_preferred[:2]:  # Top 2 nice-to-haves
            recommendations.append({
                'skill': skill,
                'priority': 'medium',
                'reason': f'{skill} is preferred for {target_role}'
            })
        
        return {
            'target_role': target_role,
            'readiness_score': round(readiness_score, 1),
            'matching_skills': matching_skills,
            'missing_required': missing_required,
            'missing_preferred': missing_preferred,
            'recommendations': recommendations,
            'next_steps': self._generate_learning_path(missing_required[:3])
        }
    
    def _generate_learning_path(self, skills_to_learn: List[str]) -> List[Dict]:
        """Generate a learning path for missing skills."""
        path = []
        for skill in skills_to_learn:
            # Find topics that teach this skill
            for area, topics in self.topic_database.items():
                for topic in topics:
                    if skill.lower() in [s.lower() for s in topic.get('skills_gained', [])]:
                        path.append({
                            'skill': skill,
                            'topic': topic['title'],
                            'estimated_hours': topic['estimated_hours']
                        })
                        break
                else:
                    continue
                break
            else:
                # Generic recommendation if no specific topic found
                path.append({
                    'skill': skill,
                    'topic': f'Learn {skill}',
                    'estimated_hours': 10
                })
        return path
    
    def get_adaptive_recommendations(self, user, progress_records) -> Dict:
        """
        Get adaptive recommendations based on user's performance.
        
        Analyzes progress to suggest difficulty adjustments and additional topics.
        """
        if not progress_records:
            return {
                'adjustment': 'none',
                'message': 'Complete some topics to get personalized recommendations',
                'suggested_topics': []
            }
        
        # Calculate average performance
        completed = [p for p in progress_records if p.status == 'completed' and p.score]
        if not completed:
            return {
                'adjustment': 'none',
                'message': 'Complete some assessments to get personalized recommendations',
                'suggested_topics': []
            }
        
        avg_score = sum(p.score for p in completed) / len(completed)
        
        # Get difficulty feedback
        feedback_counts = {'too_easy': 0, 'just_right': 0, 'too_hard': 0}
        for p in progress_records:
            if p.difficulty_feedback:
                feedback_counts[p.difficulty_feedback] = feedback_counts.get(p.difficulty_feedback, 0) + 1
        
        # Determine adjustment
        adjustment = 'none'
        message = ''
        suggested_difficulty = user.skill_level
        
        if avg_score >= 85 and feedback_counts.get('too_easy', 0) > feedback_counts.get('too_hard', 0):
            adjustment = 'increase'
            message = 'Great performance! Recommending more challenging topics.'
            suggested_difficulty = 'advanced' if user.skill_level == 'intermediate' else 'intermediate'
        elif avg_score < 60 or feedback_counts.get('too_hard', 0) > 2:
            adjustment = 'decrease'
            message = 'Recommending additional practice and foundational topics.'
            suggested_difficulty = 'beginner' if user.skill_level == 'intermediate' else 'beginner'
        else:
            message = 'You\'re on track! Keep up the good work.'
        
        # Get suggested topics
        suggested_topics = []
        for area, topics in self.topic_database.items():
            for topic in topics:
                if topic['difficulty'] == suggested_difficulty:
                    suggested_topics.append({
                        'title': topic['title'],
                        'area': area,
                        'difficulty': topic['difficulty'],
                        'estimated_hours': topic['estimated_hours']
                    })
        
        return {
            'adjustment': adjustment,
            'message': message,
            'current_performance': {
                'average_score': round(avg_score, 1),
                'topics_completed': len(completed),
                'difficulty_feedback': feedback_counts
            },
            'suggested_difficulty': suggested_difficulty,
            'suggested_topics': suggested_topics[:5]
        }
