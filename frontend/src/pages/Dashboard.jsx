// SmartCurriculum - Dashboard Page
// Main dashboard with overview and quick actions

import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../App';
import { getCurricula } from '../services/curriculum';
import LoadingSpinner from '../components/LoadingSpinner';
import {
    BookOpen, Clock, Plus, ChevronRight, Target, User
} from 'lucide-react';
import './Dashboard.css';

function Dashboard() {
    const { user } = useAuth();
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
    const [curricula, setCurricula] = useState([]);

    useEffect(() => {
        fetchDashboardData();
    }, []);

    const fetchDashboardData = async () => {
        try {
            const curriculaRes = await getCurricula();
            setCurricula(curriculaRes.curricula || []);
        } catch (error) {
            console.error('Failed to fetch dashboard data:', error);
        } finally {
            setLoading(false);
        }
    };

    const getGreeting = () => {
        const hour = new Date().getHours();
        if (hour < 12) return 'Good morning';
        if (hour < 17) return 'Good afternoon';
        return 'Good evening';
    };

    if (loading) {
        return (
            <div className="loading-overlay">
                <LoadingSpinner size="lg" message="Loading dashboard..." />
            </div>
        );
    }

    const hasActiveCurriculum = curricula.length > 0;
    const activeCurriculum = hasActiveCurriculum ? curricula[0] : null;

    return (
        <div className="dashboard">
            {/* Welcome Header */}
            <header className="dashboard-header">
                <div className="welcome-section">
                    <h1 className="welcome-title">
                        {getGreeting()}, <span className="user-name-highlight">{user?.name?.split(' ')[0] || 'Learner'}!</span>
                    </h1>
                    <p className="welcome-subtitle">
                        {hasActiveCurriculum
                            ? "Your personalized curriculum is ready"
                            : "Start your personalized learning journey today"}
                    </p>
                </div>

                {!hasActiveCurriculum && (
                    <button
                        className="btn btn-primary btn-lg"
                        onClick={() => navigate('/curriculum')}
                    >
                        <Plus size={20} />
                        Generate Curriculum
                    </button>
                )}
            </header>

            {/* Stats Grid */}
            <section className="stats-grid">
                <div className="card stat-card">
                    <div className="stat-icon" style={{ background: 'var(--primary-100)', color: 'var(--primary-600)' }}>
                        <BookOpen size={24} />
                    </div>
                    <div className="stat-value">{curricula.length}</div>
                    <div className="stat-label">Curricula Created</div>
                </div>

                {activeCurriculum && (
                    <>
                        <div className="card stat-card">
                            <div className="stat-icon" style={{ background: 'var(--accent-success-light)', color: 'var(--accent-success)' }}>
                                <Clock size={24} />
                            </div>
                            <div className="stat-value">{activeCurriculum.duration_weeks}</div>
                            <div className="stat-label">Weeks Duration</div>
                        </div>

                        <div className="card stat-card">
                            <div className="stat-icon" style={{ background: 'var(--accent-warning-light)', color: 'var(--accent-warning)' }}>
                                <Target size={24} />
                            </div>
                            <div className="stat-value">{activeCurriculum.total_hours || 0}h</div>
                            <div className="stat-label">Total Hours</div>
                        </div>
                    </>
                )}
            </section>

            {/* Main Content Grid */}
            <div className="dashboard-grid">
                {/* Current Curriculum Card */}
                <section className="card progress-overview-card">
                    <div className="card-header">
                        <h2 className="card-title">Current Curriculum</h2>
                        {hasActiveCurriculum && (
                            <Link to="/curriculum" className="card-link">
                                View All <ChevronRight size={16} />
                            </Link>
                        )}
                    </div>
                    <div className="card-body">
                        {hasActiveCurriculum ? (
                            <>
                                <div className="curriculum-info">
                                    <h3 className="curriculum-title">{activeCurriculum.title}</h3>
                                    <p className="curriculum-meta">
                                        {activeCurriculum.duration_weeks} weeks • {activeCurriculum.difficulty} • {activeCurriculum.total_hours || 0} hours total
                                    </p>
                                </div>

                                <p className="curriculum-description" style={{ marginTop: '1rem', color: 'var(--text-secondary)' }}>
                                    {activeCurriculum.description?.substring(0, 150)}
                                    {activeCurriculum.description?.length > 150 ? '...' : ''}
                                </p>

                                <button
                                    className="btn btn-primary btn-full mt-lg"
                                    onClick={() => navigate('/curriculum')}
                                >
                                    View Curriculum Details
                                    <ChevronRight size={18} />
                                </button>
                            </>
                        ) : (
                            <div className="empty-state">
                                <div className="empty-state-icon">
                                    <BookOpen size={32} />
                                </div>
                                <h3 className="empty-state-title">No Curriculum Yet</h3>
                                <p className="empty-state-description">
                                    Generate your personalized curriculum to start learning
                                </p>
                                <button
                                    className="btn btn-primary"
                                    onClick={() => navigate('/curriculum')}
                                >
                                    Get Started
                                </button>
                            </div>
                        )}
                    </div>
                </section>

                {/* Quick Actions Card */}
                <section className="card quick-actions-card">
                    <div className="card-header">
                        <h2 className="card-title">Quick Actions</h2>
                    </div>
                    <div className="card-body">
                        <div className="actions-list">
                            <button
                                className="action-item"
                                onClick={() => navigate('/curriculum')}
                            >
                                <div className="action-icon" style={{ background: 'var(--primary-100)' }}>
                                    <BookOpen size={20} className="text-primary-600" />
                                </div>
                                <div className="action-content">
                                    <span className="action-title">My Curriculum</span>
                                    <span className="action-desc">View and generate curricula</span>
                                </div>
                                <ChevronRight size={20} className="action-arrow" />
                            </button>

                            <button
                                className="action-item"
                                onClick={() => navigate('/resume')}
                            >
                                <div className="action-icon" style={{ background: 'var(--accent-success-light)' }}>
                                    <Target size={20} style={{ color: 'var(--accent-success)' }} />
                                </div>
                                <div className="action-content">
                                    <span className="action-title">Resume Skills</span>
                                    <span className="action-desc">Export skills for your resume</span>
                                </div>
                                <ChevronRight size={20} className="action-arrow" />
                            </button>

                            <button
                                className="action-item"
                                onClick={() => navigate('/profile')}
                            >
                                <div className="action-icon" style={{ background: 'var(--accent-warning-light)' }}>
                                    <User size={20} style={{ color: 'var(--accent-warning)' }} />
                                </div>
                                <div className="action-content">
                                    <span className="action-title">Update Profile</span>
                                    <span className="action-desc">Customize learning preferences</span>
                                </div>
                                <ChevronRight size={20} className="action-arrow" />
                            </button>
                        </div>
                    </div>
                </section>
            </div>
        </div>
    );
}

export default Dashboard;
