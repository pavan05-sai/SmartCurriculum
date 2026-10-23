# SmartCurriculum - Admin Routes (MongoDB)
# Handles system analytics and admin dashboard using PyMongo aggregations

import logging
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import get_db

logger = logging.getLogger(__name__)

# Create blueprint for admin routes
admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/analytics', methods=['GET'])
@jwt_required()
def get_system_analytics():
    """
    Get comprehensive system analytics using MongoDB aggregation pipelines.
    Shows overall platform statistics.
    """
    try:
        db = get_db()
        week_ago = datetime.utcnow() - timedelta(days=7)

        # User statistics
        total_users = db.users.count_documents({})
        new_users_week = db.users.count_documents({'created_at': {'$gte': week_ago}})

        # Career goal distribution aggregation
        career_agg = list(db.users.aggregate([
            {'$group': {'_id': '$career_goal', 'count': {'$sum': 1}}}
        ]))
        career_distribution = {
            item['_id'] or 'Unknown': item['count']
            for item in career_agg
        }

        # Skill level distribution aggregation
        skill_agg = list(db.users.aggregate([
            {'$group': {'_id': '$skill_level', 'count': {'$sum': 1}}}
        ]))
        skill_distribution = {
            item['_id'] or 'Unknown': item['count']
            for item in skill_agg
        }

        # Curriculum statistics
        total_curricula = db.curricula.count_documents({})
        active_curricula = db.curricula.count_documents({'status': 'active'})
        completed_curricula = db.curricula.count_documents({'status': 'completed'})

        # Topic statistics
        total_topics = db.topics.count_documents({})
        completed_topics = db.topics.count_documents({'status': 'completed'})

        # Skill statistics
        total_skills = db.skills.count_documents({})
        verified_skills = db.skills.count_documents({'is_verified': True})

        # Popular skills aggregation
        popular_skills_agg = list(db.skills.aggregate([
            {'$group': {'_id': '$name', 'count': {'$sum': 1}}},
            {'$sort': {'count': -1}},
            {'$limit': 10}
        ]))
        popular_skills = [
            {'name': item['_id'], 'count': item['count']}
            for item in popular_skills_agg
        ]

        return jsonify({
            'analytics': {
                'users': {
                    'total': total_users,
                    'new_this_week': new_users_week,
                    'career_distribution': career_distribution,
                    'skill_distribution': skill_distribution
                },
                'curricula': {
                    'total': total_curricula,
                    'active': active_curricula,
                    'completed': completed_curricula
                },
                'topics': {
                    'total': total_topics,
                    'completed': completed_topics,
                    'completion_rate': round(
                        (completed_topics / total_topics * 100) if total_topics > 0 else 0, 1
                    )
                },
                'skills': {
                    'total': total_skills,
                    'verified': verified_skills,
                    'popular': popular_skills
                }
            }
        }), 200

    except Exception as e:
        logger.error(f"Error getting analytics: {e}")
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
        db = get_db()
        limit = min(request.args.get('limit', 20, type=int), 100)
        sort_by = request.args.get('sort_by', 'created_at')

        users_cursor = db.users.find({}, {
            'password_hash': 0
        }).sort('created_at', -1).limit(limit)

        user_metrics = []
        for doc in users_cursor:
            uid = str(doc['_id'])
            curricula_count = db.curricula.count_documents({'user_id': uid})
            skills_count = db.skills.count_documents({'user_id': uid})

            user_metrics.append({
                'id': uid,
                'name': doc.get('name', ''),
                'email': doc.get('email', ''),
                'semester': doc.get('semester', 1),
                'skill_level': doc.get('skill_level', 'beginner'),
                'career_goal': doc.get('career_goal', ''),
                'curricula_count': curricula_count,
                'skills_acquired': skills_count,
                'created_at': doc.get('created_at').isoformat() if doc.get('created_at') else None
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
        logger.error(f"Error querying user metrics: {e}")
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
        db = get_db()

        # Aggregate unique topic titles with completion stats
        topic_stats = list(db.topics.aggregate([
            {
                '$group': {
                    '_id': {
                        'title': '$title',
                        'difficulty': '$difficulty'
                    },
                    'total': {'$sum': 1},
                    'completed': {
                        '$sum': {
                            '$cond': [{'$eq': ['$status', 'completed']}, 1, 0]
                        }
                    }
                }
            }
        ]))

        topics_data = []
        for item in topic_stats:
            title = item['_id'].get('title', 'Unknown')
            difficulty = item['_id'].get('difficulty', 'intermediate')
            total = item.get('total', 0)
            completed = item.get('completed', 0)
            completion_rate = (completed / total * 100) if total > 0 else 0

            topics_data.append({
                'title': title,
                'difficulty': difficulty,
                'total_assigned': total,
                'total_completed': completed,
                'completion_rate': round(completion_rate, 1)
            })

        # Sort by completion rate
        topics_data.sort(key=lambda x: x['completion_rate'], reverse=True)

        struggling_topics = [t for t in topics_data if t['completion_rate'] < 50]
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
        logger.error(f"Error getting topic statistics: {e}")
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
        db = get_db()
        week_ago = datetime.utcnow() - timedelta(days=7)

        # Recent curriculum generations
        recent_curricula_cursor = db.curricula.find(
            {'created_at': {'$gte': week_ago}}
        ).sort('created_at', -1).limit(10)

        # Recent registrations
        recent_users_cursor = db.users.find(
            {'created_at': {'$gte': week_ago}},
            {'password_hash': 0}
        ).sort('created_at', -1).limit(10)

        return jsonify({
            'activity': {
                'recent_curricula': [
                    {
                        'id': str(c['_id']),
                        'title': c.get('title', ''),
                        'user_id': str(c.get('user_id', '')),
                        'created_at': c.get('created_at').isoformat() if c.get('created_at') else None
                    }
                    for c in recent_curricula_cursor
                ],
                'recent_registrations': [
                    {
                        'id': str(u['_id']),
                        'name': u.get('name', ''),
                        'career_goal': u.get('career_goal', ''),
                        'created_at': u.get('created_at').isoformat() if u.get('created_at') else None
                    }
                    for u in recent_users_cursor
                ]
            }
        }), 200

    except Exception as e:
        logger.error(f"Error getting recent activity: {e}")
        return jsonify({
            'error': 'Query Failed',
            'message': str(e)
        }), 500
