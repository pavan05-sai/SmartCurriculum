// SmartCurriculum - Profile Page
// User profile management and settings

import React, { useState, useEffect } from 'react';
import { useAuth } from '../App';
import { updateProfile, changePassword } from '../services/auth';
import LoadingSpinner from '../components/LoadingSpinner';
import {
    User, Mail, BookOpen, Target, Save, Lock, Check, AlertCircle
} from 'lucide-react';
import './Profile.css';

function Profile() {
    const { user, updateUser } = useAuth();
    const [loading, setLoading] = useState(false);
    const [saving, setSaving] = useState(false);
    const [message, setMessage] = useState({ type: '', text: '' });
    const [activeTab, setActiveTab] = useState('profile');

    const [formData, setFormData] = useState({
        name: '',
        branch: '',
        semester: '',
        skill_level: 'beginner',
        career_goal: 'placement',
        learning_pace: 'moderate',
        weak_subjects: [],
        strong_subjects: [],
        interests: []
    });

    const [passwordData, setPasswordData] = useState({
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
    });

    const [newItem, setNewItem] = useState({
        weak: '',
        strong: '',
        interest: ''
    });

    useEffect(() => {
        if (user) {
            setFormData({
                name: user.name || '',
                branch: user.branch || '',
                semester: user.semester || '',
                skill_level: user.skill_level || 'beginner',
                career_goal: user.career_goal || 'placement',
                learning_pace: user.learning_pace || 'moderate',
                weak_subjects: user.weak_subjects || [],
                strong_subjects: user.strong_subjects || [],
                interests: user.interests || []
            });
        }
    }, [user]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handlePasswordChange = (e) => {
        const { name, value } = e.target;
        setPasswordData(prev => ({ ...prev, [name]: value }));
    };

    const addListItem = (field, value) => {
        if (value.trim() && !formData[field].includes(value.trim())) {
            setFormData(prev => ({
                ...prev,
                [field]: [...prev[field], value.trim()]
            }));
        }
    };

    const removeListItem = (field, item) => {
        setFormData(prev => ({
            ...prev,
            [field]: prev[field].filter(i => i !== item)
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setSaving(true);
        setMessage({ type: '', text: '' });

        try {
            const submitData = {
                ...formData,
                semester: parseInt(formData.semester) || 1
            };
            const response = await updateProfile(submitData);
            updateUser(response.user);
            setMessage({ type: 'success', text: 'Profile updated successfully!' });
        } catch (error) {
            setMessage({
                type: 'error',
                text: error.response?.data?.message || 'Failed to update profile'
            });
        } finally {
            setSaving(false);
        }
    };

    const handlePasswordSubmit = async (e) => {
        e.preventDefault();

        if (passwordData.newPassword !== passwordData.confirmPassword) {
            setMessage({ type: 'error', text: 'Passwords do not match' });
            return;
        }

        if (passwordData.newPassword.length < 6) {
            setMessage({ type: 'error', text: 'Password must be at least 6 characters' });
            return;
        }

        setSaving(true);
        setMessage({ type: '', text: '' });

        try {
            await changePassword(passwordData.currentPassword, passwordData.newPassword);
            setMessage({ type: 'success', text: 'Password changed successfully!' });
            setPasswordData({ currentPassword: '', newPassword: '', confirmPassword: '' });
        } catch (error) {
            setMessage({
                type: 'error',
                text: error.response?.data?.message || 'Failed to change password'
            });
        } finally {
            setSaving(false);
        }
    };

    return (
        <div className="profile-page">
            <header className="page-header">
                <h1 className="page-title">Profile Settings</h1>
                <p className="page-subtitle">Manage your account and learning preferences</p>
            </header>

            {/* Message */}
            {message.text && (
                <div className={`alert alert-${message.type} mb-lg`}>
                    {message.type === 'success' ? <Check size={18} /> : <AlertCircle size={18} />}
                    {message.text}
                </div>
            )}

            <div className="profile-layout">
                {/* Sidebar */}
                <aside className="profile-sidebar">
                    <div className="profile-avatar-section">
                        <div className="avatar avatar-xl">
                            {user?.name?.charAt(0)?.toUpperCase() || 'U'}
                        </div>
                        <h3 className="profile-name">{user?.name}</h3>
                        <p className="profile-email">{user?.email}</p>
                    </div>

                    <nav className="profile-nav">
                        <button
                            className={`profile-nav-item ${activeTab === 'profile' ? 'active' : ''}`}
                            onClick={() => setActiveTab('profile')}
                        >
                            <User size={18} />
                            Profile
                        </button>
                        <button
                            className={`profile-nav-item ${activeTab === 'learning' ? 'active' : ''}`}
                            onClick={() => setActiveTab('learning')}
                        >
                            <BookOpen size={18} />
                            Learning Preferences
                        </button>
                        <button
                            className={`profile-nav-item ${activeTab === 'security' ? 'active' : ''}`}
                            onClick={() => setActiveTab('security')}
                        >
                            <Lock size={18} />
                            Security
                        </button>
                    </nav>
                </aside>

                {/* Main Content */}
                <main className="profile-content">
                    {/* Profile Tab */}
                    {activeTab === 'profile' && (
                        <div className="card animate-fade-in">
                            <div className="card-header">
                                <h2 className="card-title">Personal Information</h2>
                            </div>
                            <div className="card-body">
                                <form onSubmit={handleSubmit}>
                                    <div className="form-group">
                                        <label className="form-label">Full Name</label>
                                        <input
                                            type="text"
                                            name="name"
                                            value={formData.name}
                                            onChange={handleChange}
                                            className="form-input"
                                            required
                                        />
                                    </div>

                                    <div className="form-row">
                                        <div className="form-group">
                                            <label className="form-label">Degree & Branch</label>
                                            <select
                                                name="branch"
                                                value={formData.branch}
                                                onChange={handleChange}
                                                className="form-select"
                                            >
                                                <option value="">Select your Degree/Branch</option>
                                                <optgroup label="Engineering (B.Tech/B.E.)">
                                                    <option value="B.Tech Computer Science">B.Tech Computer Science</option>
                                                    <option value="B.Tech Electronics">B.Tech Electronics & Comm.</option>
                                                    <option value="B.Tech Mechanical">B.Tech Mechanical</option>
                                                    <option value="B.Tech Civil">B.Tech Civil</option>
                                                </optgroup>
                                                <optgroup label="Engineering (M.Tech/M.E.)">
                                                    <option value="M.Tech Computer Science">M.Tech Computer Science</option>
                                                    <option value="M.Tech Electronics">M.Tech Electronics</option>
                                                    <option value="M.Tech Thermal Engg">M.Tech Thermal Engineering</option>
                                                </optgroup>
                                                <optgroup label="Medical & Health">
                                                    <option value="MBBS">MBBS (Medicine)</option>
                                                    <option value="BDS">BDS (Dental)</option>
                                                    <option value="B.Pharma">B.Pharma</option>
                                                    <option value="B.Sc Nursing">B.Sc Nursing</option>
                                                </optgroup>
                                                <optgroup label="Science (B.Sc/M.Sc)">
                                                    <option value="B.Sc Physics">B.Sc Physics</option>
                                                    <option value="B.Sc Mathematics">B.Sc Mathematics</option>
                                                    <option value="B.Sc Chemistry">B.Sc Chemistry</option>
                                                    <option value="B.Sc Biology">B.Sc Biology</option>
                                                    <option value="M.Sc Physics">M.Sc Physics</option>
                                                    <option value="M.Sc Mathematics">M.Sc Mathematics</option>
                                                    <option value="M.Sc Chemistry">M.Sc Chemistry</option>
                                                </optgroup>
                                                <optgroup label="Arts & Humanities">
                                                    <option value="B.A. Economics">B.A. Economics</option>
                                                    <option value="B.A. English">B.A. English</option>
                                                    <option value="B.A. Psychology">B.A. Psychology</option>
                                                    <option value="B.A. Political Science">B.A. Political Science</option>
                                                    <option value="M.A. English Literature">M.A. English Literature</option>
                                                    <option value="M.A. Economics">M.A. Economics</option>
                                                </optgroup>
                                                <optgroup label="Commerce & Management">
                                                    <option value="B.Com">B.Com</option>
                                                    <option value="BBA">BBA</option>
                                                    <option value="MBA Finance">MBA Finance</option>
                                                    <option value="MBA Marketing">MBA Marketing</option>
                                                    <option value="MBA HR">MBA HR</option>
                                                </optgroup>
                                                <optgroup label="Law">
                                                    <option value="LLB">LLB</option>
                                                    <option value="B.A. LLB">B.A. LLB</option>
                                                    <option value="LLM">LLM</option>
                                                </optgroup>
                                                <option value="Other">Other</option>
                                            </select>
                                        </div>

                                        <div className="form-group">
                                            <label className="form-label">Current Semester</label>
                                            <select
                                                name="semester"
                                                value={formData.semester}
                                                onChange={handleChange}
                                                className="form-select"
                                            >
                                                {[1, 2, 3, 4, 5, 6, 7, 8].map(sem => (
                                                    <option key={sem} value={sem}>Semester {sem}</option>
                                                ))}
                                            </select>
                                        </div>
                                    </div>

                                    <button
                                        type="submit"
                                        className="btn btn-primary"
                                        disabled={saving}
                                    >
                                        {saving ? <span className="spinner spinner-sm" /> : <Save size={18} />}
                                        Save Changes
                                    </button>
                                </form>
                            </div>
                        </div>
                    )}

                    {/* Learning Preferences Tab */}
                    {activeTab === 'learning' && (
                        <div className="card animate-fade-in">
                            <div className="card-header">
                                <h2 className="card-title">Learning Preferences</h2>
                            </div>
                            <div className="card-body">
                                <form onSubmit={handleSubmit}>
                                    <div className="form-row">
                                        <div className="form-group">
                                            <label className="form-label">Skill Level</label>
                                            <select
                                                name="skill_level"
                                                value={formData.skill_level}
                                                onChange={handleChange}
                                                className="form-select"
                                            >
                                                <option value="beginner">Beginner</option>
                                                <option value="intermediate">Intermediate</option>
                                                <option value="advanced">Advanced</option>
                                            </select>
                                        </div>

                                        <div className="form-group">
                                            <label className="form-label">Career Goal</label>
                                            <select
                                                name="career_goal"
                                                value={formData.career_goal}
                                                onChange={handleChange}
                                                className="form-select"
                                            >
                                                <option value="placement">Job Placement</option>
                                                <option value="higher_studies">Higher Studies</option>
                                                <option value="startup">Startup</option>
                                                <option value="research">Research</option>
                                            </select>
                                        </div>
                                    </div>

                                    <div className="form-group">
                                        <label className="form-label">Learning Pace</label>
                                        <select
                                            name="learning_pace"
                                            value={formData.learning_pace}
                                            onChange={handleChange}
                                            className="form-select"
                                        >
                                            <option value="slow">Slow (More practice)</option>
                                            <option value="moderate">Moderate (Balanced)</option>
                                            <option value="fast">Fast (Quick learner)</option>
                                        </select>
                                    </div>

                                    {/* Weak Subjects */}
                                    <div className="form-group">
                                        <label className="form-label">Weak Subjects</label>
                                        <div className="tag-input-container">
                                            <div className="tags-list">
                                                {formData.weak_subjects.map((item, i) => (
                                                    <span key={i} className="tag tag-warning">
                                                        {item}
                                                        <button
                                                            type="button"
                                                            className="tag-remove"
                                                            onClick={() => removeListItem('weak_subjects', item)}
                                                        >×</button>
                                                    </span>
                                                ))}
                                            </div>
                                            <div className="tag-input-row">
                                                <input
                                                    type="text"
                                                    placeholder="Add subject"
                                                    value={newItem.weak}
                                                    onChange={(e) => setNewItem(prev => ({ ...prev, weak: e.target.value }))}
                                                    className="form-input"
                                                    onKeyPress={(e) => {
                                                        if (e.key === 'Enter') {
                                                            e.preventDefault();
                                                            addListItem('weak_subjects', newItem.weak);
                                                            setNewItem(prev => ({ ...prev, weak: '' }));
                                                        }
                                                    }}
                                                />
                                                <button
                                                    type="button"
                                                    className="btn btn-secondary"
                                                    onClick={() => {
                                                        addListItem('weak_subjects', newItem.weak);
                                                        setNewItem(prev => ({ ...prev, weak: '' }));
                                                    }}
                                                >
                                                    Add
                                                </button>
                                            </div>
                                        </div>
                                    </div>

                                    {/* Interests */}
                                    <div className="form-group">
                                        <label className="form-label">Interests</label>
                                        <div className="tag-input-container">
                                            <div className="tags-list">
                                                {formData.interests.map((item, i) => (
                                                    <span key={i} className="tag tag-primary">
                                                        {item}
                                                        <button
                                                            type="button"
                                                            className="tag-remove"
                                                            onClick={() => removeListItem('interests', item)}
                                                        >×</button>
                                                    </span>
                                                ))}
                                            </div>
                                            <div className="tag-input-row">
                                                <input
                                                    type="text"
                                                    placeholder="Add interest"
                                                    value={newItem.interest}
                                                    onChange={(e) => setNewItem(prev => ({ ...prev, interest: e.target.value }))}
                                                    className="form-input"
                                                    onKeyPress={(e) => {
                                                        if (e.key === 'Enter') {
                                                            e.preventDefault();
                                                            addListItem('interests', newItem.interest);
                                                            setNewItem(prev => ({ ...prev, interest: '' }));
                                                        }
                                                    }}
                                                />
                                                <button
                                                    type="button"
                                                    className="btn btn-secondary"
                                                    onClick={() => {
                                                        addListItem('interests', newItem.interest);
                                                        setNewItem(prev => ({ ...prev, interest: '' }));
                                                    }}
                                                >
                                                    Add
                                                </button>
                                            </div>
                                        </div>
                                    </div>

                                    <button
                                        type="submit"
                                        className="btn btn-primary"
                                        disabled={saving}
                                    >
                                        {saving ? <span className="spinner spinner-sm" /> : <Save size={18} />}
                                        Save Preferences
                                    </button>
                                </form>
                            </div>
                        </div>
                    )}

                    {/* Security Tab */}
                    {activeTab === 'security' && (
                        <div className="card animate-fade-in">
                            <div className="card-header">
                                <h2 className="card-title">Change Password</h2>
                            </div>
                            <div className="card-body">
                                <form onSubmit={handlePasswordSubmit}>
                                    <div className="form-group">
                                        <label className="form-label">Current Password</label>
                                        <input
                                            type="password"
                                            name="currentPassword"
                                            value={passwordData.currentPassword}
                                            onChange={handlePasswordChange}
                                            className="form-input"
                                            required
                                        />
                                    </div>

                                    <div className="form-group">
                                        <label className="form-label">New Password</label>
                                        <input
                                            type="password"
                                            name="newPassword"
                                            value={passwordData.newPassword}
                                            onChange={handlePasswordChange}
                                            className="form-input"
                                            required
                                        />
                                        <p className="form-hint">Must be at least 6 characters</p>
                                    </div>

                                    <div className="form-group">
                                        <label className="form-label">Confirm New Password</label>
                                        <input
                                            type="password"
                                            name="confirmPassword"
                                            value={passwordData.confirmPassword}
                                            onChange={handlePasswordChange}
                                            className="form-input"
                                            required
                                        />
                                    </div>

                                    <button
                                        type="submit"
                                        className="btn btn-primary"
                                        disabled={saving}
                                    >
                                        {saving ? <span className="spinner spinner-sm" /> : <Lock size={18} />}
                                        Update Password
                                    </button>
                                </form>
                            </div>
                        </div>
                    )}
                </main>
            </div>
        </div>
    );
}

export default Profile;
