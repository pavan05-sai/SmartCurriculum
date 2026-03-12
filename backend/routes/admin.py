# SmartCurriculum - Admin Routes
# Handles system analytics and admin dashboard

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from models.user import User
from models.curriculum import Curriculum, Topic
from models.skill import Skill
from datetime import datetime, timedelta
from sqlalchemy import func

# Create blueprint for admin routes
admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/analytics', methods=['GET'])
@jwt_required()
def get_system_analytics():
    """
    Get comprehensive system analytics.
    Shows overall platform statistics.
    """
    try:
        # User statistics
        total_users = User.query.count()
        new_users_week = User.query.filter(
            User.created_at >= datetime.utcnow() - timedelta(days=7)
        ).count()
        
        # Career goal distribution
        career_distribution = db.session.query(
            User.career_goal,
            func.count(User.id)
        ).group_by(User.career_goal).all()
        
        # Skill level distribution
        skill_distribution = db.session.query(
            User.skill_level,
            func.count(User.id)
        ).group_by(User.skill_level).all()
        
        # Curriculum statistics
        total_curricula = Curriculum.query.count()
        active_curricula = Curriculum.query.filter_by(status='active').count()
        completed_curricula = Curriculum.query.filter_by(status='completed').count()
        
        # Topic statistics
        total_topics = Topic.query.count()
        completed_topics = Topic.query.filter_by(status='completed').count()
        
        # Skill statistics
        total_skills = Skill.query.count()
        verified_skills = Skill.query.filter_by(is_verified=True).count()
        
        # Popular skills
        popular_skills = db.session.query(
            Skill.name,
            func.count(Skill.id).label('count')
        ).group_by(Skill.name).order_by(func.count(Skill.id).desc()).limit(10).all()
        
        return jsonify({
            'analytics': {
                'users': {
                    'total': total_users,
                    'new_this_week': new_users_week,
                    'career_distribution': {
                        goal: count for goal, count in career_distribution
                    },
                    'skill_distribution': {
                        level: count for level, count in skill_distribution
                    }
                },
                'curricula': {
                    'total': total_curricula,
                    'active': active_curricula,
                    'completed': completed_curricula
                },
                'topics': {
                    'total': total_topics,
                    'completed': completed_topics,
                    'completion_rate': round((completed_topics / total_topics * 100) if total_topics > 0 else 0, 1)
                },
                'skills': {
                    'total': total_skills,
                    'verified': verified_skills,
                    'popular': [
                        {'name': name, 'count': count}
                        for name, count in popular_skills
                    ]
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Analytics Failed',
            'message': str(e)
        }), 500


@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def get_user_metrics():
    """
    Get user performance metrics.
    
    Query params:
    - limit: Number of users to return (default 20)
    - sort_by: Field to sort by (curricula, skills, created_at)
    """
    try:
        limit = request.args.get('limit', 20, type=int)
        sort_by = request.args.get('sort_by', 'created_at')
        
        # Get users with their statistics
        users = User.query.limit(limit).all()
        
        user_metrics = []
        for user in users:
            # Get user's curricula
            curricula = Curriculum.query.filter_by(user_id=user.id).all()
            
            # Get skill count
            skill_count = Skill.query.filter_by(user_id=user.id).count()
            
            user_metrics.append({
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'semester': user.semester,
                'skill_level': user.skill_level,
                'career_goal': user.career_goal,
                'curricula_count': len(curricula),
                'skills_acquired': skill_count,
                'created_at': user.created_at.isoformat() if user.created_at else None
            })
        
        # Sort based on parameter
        if sort_by == 'curricula':
            user_metrics.sort(key=lambda x: x['curricula_count'], reverse=True)
        elif sort_by == 'skills':
            user_metrics.sort(key=lambda x: x['skills_acquired'], reverse=True)
        
        return jsonify({
            'users': user_metrics,
            'total': len(user_metrics)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Query Failed',
            'message': str(e)
        }), 500


@admin_bp.route('/topics', methods=['GET'])
@jwt_required()
def get_topic_statistics():
    """
    Get topic completion statistics.
    Shows which topics are most/least completed.
    """
    try:
        # Get all unique topic titles with completion counts
        topic_stats = db.session.query(
            Topic.title,
            Topic.difficulty,
            func.count(Topic.id).label('total'),
            func.sum(
                db.case((Topic.status == 'completed', 1), else_=0)
            ).label('completed')
        ).group_by(Topic.title, Topic.difficulty).all()
        
        topics_data = []
        for title, difficulty, total, completed in topic_stats:
            completion_rate = (completed / total * 100) if total > 0 else 0
            topics_data.append({
                'title': title,
                'difficulty': difficulty,
                'total_assigned': total,
                'total_completed': completed or 0,
                'completion_rate': round(completion_rate, 1)
            })
        
        # Sort by completion rate
        topics_data.sort(key=lambda x: x['completion_rate'], reverse=True)
        
        # Get topics needing attention (low completion rate)
        struggling_topics = [t for t in topics_data if t['completion_rate'] < 50]
        
        # Get most successful topics
        successful_topics = [t for t in topics_data if t['completion_rate'] >= 80]
        
        return jsonify({
            'topics': topics_data,
            'insights': {
                'total_unique_topics': len(topics_data),
                'struggling_topics': struggling_topics[:5],
                'successful_topics': successful_topics[:5],
                'average_completion_rate': round(
                    sum(t['completion_rate'] for t in topics_data) / len(topics_data) if topics_data else 0, 1
                )
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Query Failed',
            'message': str(e)
        }), 500


@admin_bp.route('/activity', methods=['GET'])
@jwt_required()
def get_recent_activity():
    """
    Get recent platform activity.
    """
    try:
        # Recent curriculum generations
        recent_curricula = Curriculum.query.filter(
            Curriculum.created_at >= datetime.utcnow() - timedelta(days=7)
        ).order_by(Curriculum.created_at.desc()).limit(10).all()
        
        # Recent registrations
        recent_users = User.query.filter(
            User.created_at >= datetime.utcnow() - timedelta(days=7)
        ).order_by(User.created_at.desc()).limit(10).all()
        
        return jsonify({
            'activity': {
                'recent_curricula': [
                    {
                        'id': c.id,
                        'title': c.title,
                        'user_id': c.user_id,
                        'created_at': c.created_at.isoformat() if c.created_at else None
                    }
                    for c in recent_curricula
                ],
                'recent_registrations': [
                    {
                        'id': u.id,
                        'name': u.name,
                        'career_goal': u.career_goal,
                        'created_at': u.created_at.isoformat() if u.created_at else None
                    }
                    for u in recent_users
                ]
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Query Failed',
            'message': str(e)
        }), 500
