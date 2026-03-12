// SmartCurriculum - Resume Page
// Skill management and resume export

import React, { useState, useEffect } from 'react';
import { getSkills, addSkill, deleteSkill, generateBullet, exportSkills, matchJobSkills } from '../services/resume';
import LoadingSpinner from '../components/LoadingSpinner';
import {
    FileText, Plus, Trash2, Sparkles, Download,
    Copy, Check, Search, Award
} from 'lucide-react';
import './Resume.css';

function Resume() {
    const [loading, setLoading] = useState(true);
    const [skills, setSkills] = useState([]);
    const [showAddModal, setShowAddModal] = useState(false);
    const [showMatchModal, setShowMatchModal] = useState(false);
    const [newSkill, setNewSkill] = useState({ name: '', proficiency_level: 50, category: 'technical' });
    const [jobDescription, setJobDescription] = useState('');
    const [matchResults, setMatchResults] = useState(null);
    const [exportedText, setExportedText] = useState('');
    const [copied, setCopied] = useState(false);

    useEffect(() => {
        fetchSkills();
    }, []);

    const fetchSkills = async () => {
        try {
            const response = await getSkills();
            setSkills(response.skills || []);
        } catch (error) {
            console.error('Failed to fetch skills:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleAddSkill = async (e) => {
        e.preventDefault();
        try {
            await addSkill(newSkill);
            await fetchSkills();
            setShowAddModal(false);
            setNewSkill({ name: '', proficiency_level: 50, category: 'technical' });
        } catch (error) {
            console.error('Failed to add skill:', error);
        }
    };

    const handleDeleteSkill = async (skillId) => {
        if (!confirm('Are you sure you want to delete this skill?')) return;
        try {
            await deleteSkill(skillId);
            await fetchSkills();
        } catch (error) {
            console.error('Failed to delete skill:', error);
        }
    };

    const handleGenerateBullet = async (skillId) => {
        try {
            const response = await generateBullet(skillId);
            const updatedSkills = skills.map(s =>
                s.id === skillId ? { ...s, resume_bullet: response.bullet_point } : s
            );
            setSkills(updatedSkills);
        } catch (error) {
            console.error('Failed to generate bullet:', error);
        }
    };

    const handleExport = async () => {
        try {
            const response = await exportSkills('markdown');
            setExportedText(response.content || response);
        } catch (error) {
            console.error('Failed to export skills:', error);
        }
    };

    const handleMatchJob = async () => {
        try {
            const response = await matchJobSkills(jobDescription);
            setMatchResults(response);
        } catch (error) {
            console.error('Failed to match skills:', error);
        }
    };

    const handleCopy = () => {
        navigator.clipboard.writeText(exportedText);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    if (loading) {
        return (
            <div className="loading-overlay">
                <LoadingSpinner size="lg" message="Loading skills..." />
            </div>
        );
    }

    const technicalSkills = skills.filter(s => s.category === 'technical');
    const softSkills = skills.filter(s => s.category === 'soft');
    const toolSkills = skills.filter(s => s.category === 'tool');

    return (
        <div className="resume-page">
            <header className="page-header">
                <div>
                    <h1 className="page-title">Resume Skills</h1>
                    <p className="page-subtitle">Manage your skills and export for your resume</p>
                </div>
                <div className="header-actions">
                    <button
                        className="btn btn-secondary"
                        onClick={() => setShowMatchModal(true)}
                    >
                        <Search size={18} />
                        Match to Job
                    </button>
                    <button className="btn btn-primary" onClick={() => setShowAddModal(true)}>
                        <Plus size={18} />
                        Add Skill
                    </button>
                </div>
            </header>

            {/* Skills Grid */}
            <div className="skills-sections">
                {/* Technical Skills */}
                <section className="card skills-section">
                    <div className="section-header">
                        <h2 className="section-title">Technical Skills</h2>
                        <span className="skill-count">{technicalSkills.length}</span>
                    </div>
                    <div className="skills-list">
                        {technicalSkills.length === 0 ? (
                            <p className="no-skills">No technical skills added yet.</p>
                        ) : (
                            technicalSkills.map((skill) => (
                                <SkillCard
                                    key={skill.id}
                                    skill={skill}
                                    onDelete={handleDeleteSkill}
                                    onGenerateBullet={handleGenerateBullet}
                                />
                            ))
                        )}
                    </div>
                </section>

                {/* Soft Skills */}
                <section className="card skills-section">
                    <div className="section-header">
                        <h2 className="section-title">Soft Skills</h2>
                        <span className="skill-count">{softSkills.length}</span>
                    </div>
                    <div className="skills-list">
                        {softSkills.length === 0 ? (
                            <p className="no-skills">No soft skills added yet.</p>
                        ) : (
                            softSkills.map((skill) => (
                                <SkillCard
                                    key={skill.id}
                                    skill={skill}
                                    onDelete={handleDeleteSkill}
                                    onGenerateBullet={handleGenerateBullet}
                                />
                            ))
                        )}
                    </div>
                </section>

                {/* Tools & Technologies */}
                <section className="card skills-section">
                    <div className="section-header">
                        <h2 className="section-title">Tools & Technologies</h2>
                        <span className="skill-count">{toolSkills.length}</span>
                    </div>
                    <div className="skills-list">
                        {toolSkills.length === 0 ? (
                            <p className="no-skills">No tools added yet.</p>
                        ) : (
                            toolSkills.map((skill) => (
                                <SkillCard
                                    key={skill.id}
                                    skill={skill}
                                    onDelete={handleDeleteSkill}
                                    onGenerateBullet={handleGenerateBullet}
                                />
                            ))
                        )}
                    </div>
                </section>
            </div>

            {/* Export Section */}
            <section className="card export-section">
                <div className="card-header">
                    <h2 className="card-title">Export Skills</h2>
                    <button className="btn btn-primary" onClick={handleExport}>
                        <Download size={18} />
                        Export for Resume
                    </button>
                </div>
                {exportedText && (
                    <div className="card-body">
                        <div className="export-preview">
                            <pre>{exportedText}</pre>
                        </div>
                        <button className="btn btn-secondary" onClick={handleCopy}>
                            {copied ? <Check size={16} /> : <Copy size={16} />}
                            {copied ? 'Copied!' : 'Copy to Clipboard'}
                        </button>
                    </div>
                )}
            </section>

            {/* Add Skill Modal */}
            {showAddModal && (
                <div className="modal-overlay" onClick={() => setShowAddModal(false)}>
                    <div className="modal" onClick={(e) => e.stopPropagation()}>
                        <div className="modal-header">
                            <h2 className="modal-title">Add Skill</h2>
                            <button className="modal-close" onClick={() => setShowAddModal(false)}>×</button>
                        </div>
                        <form onSubmit={handleAddSkill}>
                            <div className="modal-body">
                                <div className="form-group">
                                    <label className="form-label">Skill Name</label>
                                    <input
                                        type="text"
                                        value={newSkill.name}
                                        onChange={(e) => setNewSkill(prev => ({ ...prev, name: e.target.value }))}
                                        className="form-input"
                                        placeholder="e.g., Python, React, Communication"
                                        required
                                    />
                                </div>

                                <div className="form-group">
                                    <label className="form-label">Category</label>
                                    <select
                                        value={newSkill.category}
                                        onChange={(e) => setNewSkill(prev => ({ ...prev, category: e.target.value }))}
                                        className="form-select"
                                    >
                                        <option value="technical">Technical</option>
                                        <option value="soft">Soft Skill</option>
                                        <option value="tool">Tool/Technology</option>
                                    </select>
                                </div>

                                <div className="form-group">
                                    <label className="form-label">Proficiency: {newSkill.proficiency_level}%</label>
                                    <input
                                        type="range"
                                        min="10"
                                        max="100"
                                        value={newSkill.proficiency_level}
                                        onChange={(e) => setNewSkill(prev => ({ ...prev, proficiency_level: parseInt(e.target.value) }))}
                                        className="form-range"
                                    />
                                </div>
                            </div>
                            <div className="modal-footer">
                                <button type="button" className="btn btn-secondary" onClick={() => setShowAddModal(false)}>Cancel</button>
                                <button type="submit" className="btn btn-primary">Add Skill</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            {/* Job Match Modal */}
            {showMatchModal && (
                <div className="modal-overlay" onClick={() => setShowMatchModal(false)}>
                    <div className="modal modal-wide" onClick={(e) => e.stopPropagation()}>
                        <div className="modal-header">
                            <h2 className="modal-title">Match Skills to Job</h2>
                            <button className="modal-close" onClick={() => setShowMatchModal(false)}>×</button>
                        </div>
                        <div className="modal-body">
                            <div className="form-group">
                                <label className="form-label">Paste Job Description</label>
                                <textarea
                                    value={jobDescription}
                                    onChange={(e) => setJobDescription(e.target.value)}
                                    className="form-textarea"
                                    rows={6}
                                    placeholder="Paste the job description here..."
                                />
                            </div>

                            {matchResults && (
                                <div className="match-results">
                                    <h3>Match Results</h3>
                                    <div className="match-score">
                                        <Award size={24} />
                                        <span>Match Score: {matchResults.match_percentage || 0}%</span>
                                    </div>

                                    {matchResults.matching_skills?.length > 0 && (
                                        <div className="match-group">
                                            <h4>Matching Skills ✓</h4>
                                            <div className="match-tags">
                                                {matchResults.matching_skills.map((skill, i) => (
                                                    <span key={i} className="tag tag-success">{skill}</span>
                                                ))}
                                            </div>
                                        </div>
                                    )}

                                    {matchResults.missing_skills?.length > 0 && (
                                        <div className="match-group">
                                            <h4>Skills to Develop</h4>
                                            <div className="match-tags">
                                                {matchResults.missing_skills.map((skill, i) => (
                                                    <span key={i} className="tag tag-warning">{skill}</span>
                                                ))}
                                            </div>
                                        </div>
                                    )}
                                </div>
                            )}
                        </div>
                        <div className="modal-footer">
                            <button className="btn btn-secondary" onClick={() => setShowMatchModal(false)}>Close</button>
                            <button className="btn btn-primary" onClick={handleMatchJob}>
                                <Search size={16} />
                                Analyze Job
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

// Skill Card Component
function SkillCard({ skill, onDelete, onGenerateBullet }) {
    const [generating, setGenerating] = useState(false);

    const handleGenerate = async () => {
        setGenerating(true);
        await onGenerateBullet(skill.id);
        setGenerating(false);
    };

    return (
        <div className="skill-card">
            <div className="skill-header">
                <span className="skill-name">{skill.name}</span>
                <div className="skill-actions">
                    <button
                        className="btn btn-icon btn-ghost"
                        onClick={handleGenerate}
                        disabled={generating}
                        title="Generate resume bullet"
                    >
                        <Sparkles size={16} />
                    </button>
                    <button
                        className="btn btn-icon btn-ghost text-error"
                        onClick={() => onDelete(skill.id)}
                        title="Delete skill"
                    >
                        <Trash2 size={16} />
                    </button>
                </div>
            </div>

            <div className="skill-proficiency">
                <div className="proficiency-bar">
                    <div
                        className="proficiency-fill"
                        style={{ width: `${skill.proficiency_level}%` }}
                    />
                </div>
                <span className="proficiency-value">{skill.proficiency_level}%</span>
            </div>

            {skill.resume_bullet && (
                <p className="skill-bullet">"{skill.resume_bullet}"</p>
            )}
        </div>
    );
}

export default Resume;
