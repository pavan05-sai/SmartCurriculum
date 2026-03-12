// SmartCurriculum - Curriculum Page
// Clear roadmap display with phases and real-time duration

import React, { useState, useEffect } from 'react';
import { getCurricula, getCurriculum, generateCurriculum, downloadPDF } from '../services/curriculum';
import LoadingSpinner from '../components/LoadingSpinner';
import {
    BookOpen, Plus, Download, Clock, Target, Layers,
    ChevronRight, Sparkles, RefreshCw, GraduationCap,
    Code, Database, Layout, Server, Smartphone, Brain,
    CheckCircle2, Circle, ArrowRight, Calendar, Check
} from 'lucide-react';
import './Curriculum.css';

// Domain categories for Indian universities
const DOMAIN_CATEGORIES = {
    'Engineering': [
        { id: 'engineering-cs', name: 'B.Tech Computer Science', icon: Code, color: '#3B82F6' },
        { id: 'engineering-ece', name: 'B.Tech Electronics', icon: Smartphone, color: '#10B981' },
        { id: 'engineering-mech', name: 'B.Tech Mechanical', icon: Server, color: '#6366F1' },
        { id: 'engineering-civil', name: 'B.Tech Civil', icon: Layers, color: '#F59E0B' },
        { id: 'bca', name: 'BCA', icon: Code, color: '#8B5CF6' },
        { id: 'mca', name: 'MCA', icon: Database, color: '#EC4899' }
    ],
    'Science': [
        { id: 'science-physics', name: 'B.Sc Physics', icon: Brain, color: '#3B82F6' },
        { id: 'science-chemistry', name: 'B.Sc Chemistry', icon: Database, color: '#10B981' },
        { id: 'science-math', name: 'B.Sc Mathematics', icon: Target, color: '#F59E0B' },
        { id: 'science-biology', name: 'B.Sc Biology', icon: Layout, color: '#8B5CF6' }
    ],
    'Commerce': [
        { id: 'commerce-bcom', name: 'B.Com', icon: Target, color: '#3B82F6' },
        { id: 'commerce-bba', name: 'BBA', icon: Layers, color: '#10B981' },
        { id: 'commerce-mba', name: 'MBA', icon: GraduationCap, color: '#F59E0B' }
    ],
    'Medical': [
        { id: 'medical-mbbs', name: 'MBBS', icon: Brain, color: '#EF4444' },
        { id: 'medical-pharma', name: 'B.Pharma', icon: Database, color: '#EC4899' }
    ],
    'Law': [
        { id: 'law-llb', name: 'LLB', icon: BookOpen, color: '#6366F1' },
        { id: 'law-ballb', name: 'BA LLB (Integrated)', icon: GraduationCap, color: '#8B5CF6' }
    ],
    'Arts & Humanities': [
        { id: 'arts-economics', name: 'BA Economics', icon: Target, color: '#3B82F6' },
        { id: 'arts-psychology', name: 'BA Psychology', icon: Brain, color: '#EC4899' },
        { id: 'arts-english', name: 'BA English', icon: BookOpen, color: '#10B981' }
    ]
};

// Flatten for backward compatibility
const DOMAIN_OPTIONS = Object.values(DOMAIN_CATEGORIES).flat();

// Intensity options
const INTENSITY_OPTIONS = [
    { id: 'casual', name: 'Casual', desc: '1-2 hours/day', multiplier: 1 },
    { id: 'regular', name: 'Regular', desc: '3-4 hours/day', multiplier: 0.6 },
    { id: 'intensive', name: 'Intensive', desc: '6+ hours/day', multiplier: 0.3 }
];

function Curriculum() {
    const [updatingTopic, setUpdatingTopic] = useState(null);
    const [curricula, setCurricula] = useState([]);
    const [selectedCurriculum, setSelectedCurriculum] = useState(null);
    const [loading, setLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);
    const [generating, setGenerating] = useState(false);
    const [selectedCategory, setSelectedCategory] = useState('Engineering');
    const [genOptions, setGenOptions] = useState({
        domain: '',
        intensity: 'regular'
    });

    useEffect(() => {
        fetchCurricula();
    }, []);

    const fetchCurricula = async () => {
        try {
            const response = await getCurricula();
            setCurricula(response.curricula || []);
            // Auto-select first curriculum if available
            if (response.curricula?.length > 0 && !selectedCurriculum) {
                // Fetch full details including topics
                const fullCurriculum = await getCurriculum(response.curricula[0].id);
                setSelectedCurriculum(fullCurriculum.curriculum);
            }
        } catch (error) {
            console.error('Failed to fetch curricula:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleGenerate = async () => {
        setGenerating(true);
        try {
            await generateCurriculum(genOptions);
            await fetchCurricula();
            setShowModal(false);
        } catch (error) {
            console.error('Failed to generate curriculum:', error);
        } finally {
            setGenerating(false);
        }
    };

    const handleDownload = async (curriculumId) => {
        try {
            await downloadPDF(curriculumId);
        } catch (error) {
            console.error('Failed to download PDF:', error);
        }
    };

    const handleSkillToggle = async (topic, skill) => {
        // Optimistic update
        const currentCompleted = topic.completed_skills || [];
        const isCompleted = currentCompleted.includes(skill);
        let newCompleted;

        if (isCompleted) {
            newCompleted = currentCompleted.filter(s => s !== skill);
        } else {
            newCompleted = [...currentCompleted, skill];
        }

        // Update local state temporarily
        const updatedTopic = { ...topic, completed_skills: newCompleted };
        if (topic.skills_gained && newCompleted.length >= topic.skills_gained.length) {
            updatedTopic.status = 'completed';
        } else if (newCompleted.length > 0) {
            updatedTopic.status = 'in_progress';
        }

        // Update selectedCurriculum state
        setSelectedCurriculum(prev => ({
            ...prev,
            topics: prev.topics.map(t => t.id === topic.id ? updatedTopic : t)
        }));

        // Send to backend
        try {
            setUpdatingTopic(topic.id);
            // Use locally imported function instead of calling from potentially unimported service
            // Dynamic import to avoid dependency issues if not updated yet
            const { updateTopicSkills } = await import('../services/curriculum');
            await updateTopicSkills(topic.id, newCompleted);
        } catch (error) {
            console.error('Failed to update skills:', error);
            // Revert on error could be implemented here
        } finally {
            setUpdatingTopic(null);
        }
    };

    if (loading) {
        return (
            <div className="loading-overlay">
                <LoadingSpinner size="lg" message="Loading your learning paths..." />
            </div>
        );
    }

    return (
        <div className="curriculum-page">
            {curricula.length === 0 ? (
                <div className="empty-state-container">
                    <div className="empty-state-card">
                        <div className="empty-icon">
                            <GraduationCap size={48} />
                        </div>
                        <h2>Start Your Learning Journey</h2>
                        <p>Generate a personalized learning roadmap tailored to your goals</p>

                        <div className="domain-preview">
                            {DOMAIN_OPTIONS.slice(0, 4).map(domain => (
                                <div key={domain.id} className="domain-chip" style={{ '--domain-color': domain.color }}>
                                    <domain.icon size={16} />
                                    {domain.name}
                                </div>
                            ))}
                        </div>

                        <button className="btn btn-primary btn-lg" onClick={() => setShowModal(true)}>
                            <Sparkles size={20} />
                            Generate My Roadmap
                        </button>
                    </div>
                </div>
            ) : (
                <div className="curriculum-layout full-width">
                    {/* Header with Actions */}
                    <header className="curriculum-header">
                        <div className="curriculum-title-section">
                            <h1 className="page-title">My Learning Paths</h1>
                            <p className="page-subtitle">Track your curriculum progress and unlock new modules</p>
                        </div>
                        <div className="curriculum-actions">
                            <button className="btn btn-primary" onClick={() => setShowModal(true)}>
                                <Plus size={18} />
                                New Curriculum
                            </button>
                        </div>
                    </header>

                    {/* Progress Stats */}
                    {selectedCurriculum && (
                        <div className="curriculum-stats">
                            <div className="stat-card">
                                <div className="stat-icon">
                                    <BookOpen size={24} />
                                </div>
                                <div className="stat-details">
                                    <span className="stat-value">{selectedCurriculum.topics?.length || 0}</span>
                                    <span className="stat-label">Total Modules</span>
                                </div>
                            </div>
                            <div className="stat-card">
                                <div className="stat-icon completed">
                                    <CheckCircle2 size={24} />
                                </div>
                                <div className="stat-details">
                                    <span className="stat-value">
                                        {selectedCurriculum.topics?.filter(t => t.status === 'completed').length || 0}
                                    </span>
                                    <span className="stat-label">Completed</span>
                                </div>
                            </div>
                            <div className="stat-card">
                                <div className="stat-icon hours">
                                    <Clock size={24} />
                                </div>
                                <div className="stat-details">
                                    <span className="stat-value">{selectedCurriculum.total_hours || 0}h</span>
                                    <span className="stat-label">Total Hours</span>
                                </div>
                            </div>
                            <div className="stat-card">
                                <div className="stat-icon progress">
                                    <Target size={24} />
                                </div>
                                <div className="stat-details">
                                    <span className="stat-value">{Math.round(selectedCurriculum.progress || 0)}%</span>
                                    <span className="stat-label">Progress</span>
                                </div>
                            </div>
                        </div>
                    )}

                    {selectedCurriculum && (
                        <main className="roadmap-main">
                            {/* Curriculum Title */}
                            <div className="roadmap-header">
                                <div className="roadmap-title-section">
                                    <h2 className="roadmap-title">{selectedCurriculum.title}</h2>
                                    <p className="roadmap-description">{selectedCurriculum.description}</p>
                                </div>
                                <div className="roadmap-actions">
                                    <button
                                        className="btn btn-secondary"
                                        onClick={() => handleDownload(selectedCurriculum.id)}
                                    >
                                        <Download size={18} />
                                        Download PDF
                                    </button>
                                </div>
                            </div>

                            {/* Modules List */}
                            <div className="modules-list">
                                {selectedCurriculum.topics?.map((topic, index) => (
                                    <div key={topic.id} className={`module-card ${topic.status === 'completed' ? 'completed' : ''} ${topic.status === 'in_progress' ? 'in-progress' : ''}`}>
                                        <div className="module-header">
                                            <div className="module-icon-status">
                                                {topic.status === 'completed' ? (
                                                    <div className="status-icon success">
                                                        <CheckCircle2 size={24} />
                                                    </div>
                                                ) : (
                                                    <div className="status-icon number">
                                                        {index + 1}
                                                    </div>
                                                )}
                                            </div>
                                            <div className="module-info">
                                                <h3 className="module-title">{topic.title}</h3>
                                                <div className="module-meta">
                                                    <span className="meta-item">
                                                        <Clock size={14} />
                                                        {topic.estimated_hours} Hours
                                                    </span>
                                                    <span className="meta-item">
                                                        <Calendar size={14} />
                                                        Semester {topic.semester || topic.week}
                                                    </span>
                                                    {topic.difficulty && (
                                                        <span className={`badge badge-${topic.difficulty.toLowerCase()}`}>
                                                            {topic.difficulty}
                                                        </span>
                                                    )}
                                                </div>
                                            </div>
                                        </div>

                                        {topic.description && (
                                            <p className="module-description">{topic.description}</p>
                                        )}

                                        <div className="module-content">
                                            <div className="key-concepts-section">
                                                <h4 className="section-label">KEY CONCEPTS</h4>
                                                <div className="concepts-list">
                                                    {(topic.skills_gained || []).map((skill, i) => {
                                                        const isChecked = (topic.completed_skills || []).includes(skill);
                                                        return (
                                                            <label key={i} className={`concept-item ${isChecked ? 'checked' : ''}`}>
                                                                <input
                                                                    type="checkbox"
                                                                    checked={isChecked}
                                                                    onChange={() => handleSkillToggle(topic, skill)}
                                                                />
                                                                <span className="checkmark">
                                                                    {isChecked && <Check size={12} />}
                                                                </span>
                                                                <span className="concept-text">{skill}</span>
                                                            </label>
                                                        );
                                                    })}
                                                    {(!topic.skills_gained || topic.skills_gained.length === 0) && (
                                                        <p className="no-concepts">No specific key concepts listed.</p>
                                                    )}
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </main>
                    )}
                </div>
            )}

            {/* Generate Modal */}
            {showModal && (
                <div className="modal-overlay" onClick={() => setShowModal(false)}>
                    <div className="modal modal-lg" onClick={(e) => e.stopPropagation()}>
                        <div className="modal-header">
                            <h2 className="modal-title">Create Learning Roadmap</h2>
                            <button className="modal-close" onClick={() => setShowModal(false)}>×</button>
                        </div>
                        <div className="modal-body">
                            {/* Domain Selection with Categories */}
                            <div className="form-group">
                                <label className="form-label">Choose Your Program</label>

                                {/* Category Tabs */}
                                <div className="category-tabs">
                                    {Object.keys(DOMAIN_CATEGORIES).map(category => (
                                        <button
                                            key={category}
                                            className={`category-tab ${selectedCategory === category ? 'active' : ''}`}
                                            onClick={() => setSelectedCategory(category)}
                                        >
                                            {category}
                                        </button>
                                    ))}
                                </div>

                                {/* Programs in Selected Category */}
                                <div className="domain-grid">
                                    {DOMAIN_CATEGORIES[selectedCategory]?.map(domain => (
                                        <div
                                            key={domain.id}
                                            className={`domain-option ${genOptions.domain === domain.id ? 'selected' : ''}`}
                                            onClick={() => setGenOptions(prev => ({ ...prev, domain: domain.id }))}
                                            style={{ '--domain-color': domain.color }}
                                        >
                                            <domain.icon size={24} />
                                            <span>{domain.name}</span>
                                        </div>
                                    ))}
                                </div>
                            </div>

                            {/* Intensity Selection */}
                            <div className="form-group">
                                <label className="form-label">Learning Intensity</label>
                                <div className="intensity-options">
                                    {INTENSITY_OPTIONS.map(intensity => (
                                        <div
                                            key={intensity.id}
                                            className={`intensity-option ${genOptions.intensity === intensity.id ? 'selected' : ''}`}
                                            onClick={() => setGenOptions(prev => ({ ...prev, intensity: intensity.id }))}
                                        >
                                            <span className="intensity-name">{intensity.name}</span>
                                            <span className="intensity-desc">{intensity.desc}</span>
                                        </div>
                                    ))}
                                </div>
                            </div>

                            <p className="form-hint">
                                Your roadmap will be customized based on your profile, current skills, and career goals.
                            </p>
                        </div>
                        <div className="modal-footer">
                            <button className="btn btn-secondary" onClick={() => setShowModal(false)}>
                                Cancel
                            </button>
                            <button
                                className="btn btn-primary"
                                onClick={handleGenerate}
                                disabled={generating}
                            >
                                {generating ? (
                                    <>
                                        <RefreshCw size={18} className="animate-spin" />
                                        Generating...
                                    </>
                                ) : (
                                    <>
                                        <Sparkles size={18} />
                                        Generate Roadmap
                                    </>
                                )}
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default Curriculum;
