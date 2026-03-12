// SmartCurriculum - Register Page
// User registration form

import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../App';
import { register as registerService } from '../services/auth';
import {
    Mail, Lock, Eye, EyeOff, ArrowRight, BookMarked,
    User, GraduationCap, Target
} from 'lucide-react';
import './Auth.css';

function Register() {
    const navigate = useNavigate();
    const { login } = useAuth();

    const [step, setStep] = useState(1);
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        password: '',
        confirmPassword: '',
        branch: '',
        semester: '',
        skill_level: 'beginner',
        career_goal: 'placement',
        weak_subjects: [],
        interests: []
    });
    const [showPassword, setShowPassword] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
        setError('');
    };

    const handleNext = () => {
        if (step === 1) {
            if (!formData.name || !formData.email || !formData.password) {
                setError('Please fill in all required fields');
                return;
            }
            if (formData.password !== formData.confirmPassword) {
                setError('Passwords do not match');
                return;
            }
            if (formData.password.length < 6) {
                setError('Password must be at least 6 characters');
                return;
            }
        }
        setError('');
        setStep(step + 1);
    };

    const handleBack = () => {
        setStep(step - 1);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            const { confirmPassword, ...submitData } = formData;
            submitData.semester = parseInt(submitData.semester) || 1;

            const response = await registerService(submitData);
            login(response.user, response.access_token, response.refresh_token);
            navigate('/dashboard');
        } catch (err) {
            setError(err.response?.data?.message || 'Registration failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-container">
            <div className="auth-card auth-card-wide">
                {/* Logo */}
                <div className="auth-logo">
                    <BookMarked size={32} className="logo-icon" />
                    <span className="logo-text">
                        Smart<span className="logo-highlight">Curriculum</span>
                    </span>
                </div>

                {/* Header */}
                <div className="auth-header">
                    <h1 className="auth-title">Create your account</h1>
                    <p className="auth-subtitle">Start your personalized learning journey today</p>
                </div>

                {/* Progress Indicator */}
                <div className="step-indicator">
                    <div className={`step ${step >= 1 ? 'active' : ''}`}>
                        <span className="step-number">1</span>
                        <span className="step-label">Account</span>
                    </div>
                    <div className="step-line"></div>
                    <div className={`step ${step >= 2 ? 'active' : ''}`}>
                        <span className="step-number">2</span>
                        <span className="step-label">Profile</span>
                    </div>
                    <div className="step-line"></div>
                    <div className={`step ${step >= 3 ? 'active' : ''}`}>
                        <span className="step-number">3</span>
                        <span className="step-label">Goals</span>
                    </div>
                </div>

                {/* Error Message */}
                {error && (
                    <div className="alert alert-error">
                        {error}
                    </div>
                )}

                {/* Form */}
                <form onSubmit={handleSubmit} className="auth-form">
                    {/* Step 1: Account */}
                    {step === 1 && (
                        <div className="form-step animate-fade-in">
                            <div className="form-group">
                                <label className="form-label">Full Name</label>
                                <div className="input-wrapper">
                                    <User size={18} className="input-icon" />
                                    <input
                                        type="text"
                                        name="name"
                                        value={formData.name}
                                        onChange={handleChange}
                                        placeholder="John Doe"
                                        className="form-input with-icon"
                                        required
                                    />
                                </div>
                            </div>

                            <div className="form-group">
                                <label className="form-label">Email</label>
                                <div className="input-wrapper">
                                    <Mail size={18} className="input-icon" />
                                    <input
                                        type="email"
                                        name="email"
                                        value={formData.email}
                                        onChange={handleChange}
                                        placeholder="you@example.com"
                                        className="form-input with-icon"
                                        required
                                    />
                                </div>
                            </div>

                            <div className="form-row">
                                <div className="form-group">
                                    <label className="form-label">Password</label>
                                    <div className="input-wrapper">
                                        <Lock size={18} className="input-icon" />
                                        <input
                                            type={showPassword ? 'text' : 'password'}
                                            name="password"
                                            value={formData.password}
                                            onChange={handleChange}
                                            placeholder="••••••••"
                                            className="form-input with-icon"
                                            required
                                        />
                                    </div>
                                </div>

                                <div className="form-group">
                                    <label className="form-label">Confirm Password</label>
                                    <div className="input-wrapper">
                                        <Lock size={18} className="input-icon" />
                                        <input
                                            type={showPassword ? 'text' : 'password'}
                                            name="confirmPassword"
                                            value={formData.confirmPassword}
                                            onChange={handleChange}
                                            placeholder="••••••••"
                                            className="form-input with-icon"
                                            required
                                        />
                                        <button
                                            type="button"
                                            className="input-toggle"
                                            onClick={() => setShowPassword(!showPassword)}
                                        >
                                            {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                                        </button>
                                    </div>
                                </div>
                            </div>

                            <button
                                type="button"
                                className="btn btn-primary btn-lg btn-full"
                                onClick={handleNext}
                            >
                                Continue
                                <ArrowRight size={18} />
                            </button>
                        </div>
                    )}

                    {/* Step 2: Profile */}
                    {step === 2 && (
                        <div className="form-step animate-fade-in">
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
                                        <option value="">Select Semester</option>
                                        {[1, 2, 3, 4, 5, 6, 7, 8].map(sem => (
                                            <option key={sem} value={sem}>Semester {sem}</option>
                                        ))}
                                    </select>
                                </div>
                            </div>

                            <div className="form-group">
                                <label className="form-label">Skill Level</label>
                                <div className="radio-group">
                                    {['beginner', 'intermediate', 'advanced'].map(level => (
                                        <label key={level} className="radio-card">
                                            <input
                                                type="radio"
                                                name="skill_level"
                                                value={level}
                                                checked={formData.skill_level === level}
                                                onChange={handleChange}
                                            />
                                            <span className="radio-content">
                                                <span className="radio-title">{level.charAt(0).toUpperCase() + level.slice(1)}</span>
                                            </span>
                                        </label>
                                    ))}
                                </div>
                            </div>

                            <div className="form-actions">
                                <button
                                    type="button"
                                    className="btn btn-secondary btn-lg"
                                    onClick={handleBack}
                                >
                                    Back
                                </button>
                                <button
                                    type="button"
                                    className="btn btn-primary btn-lg"
                                    onClick={handleNext}
                                >
                                    Continue
                                    <ArrowRight size={18} />
                                </button>
                            </div>
                        </div>
                    )}

                    {/* Step 3: Goals */}
                    {step === 3 && (
                        <div className="form-step animate-fade-in">
                            <div className="form-group">
                                <label className="form-label">Career Goal</label>
                                <div className="radio-group radio-group-large">
                                    {[
                                        { value: 'placement', label: 'Job Placement', desc: 'Prepare for industry roles' },
                                        { value: 'higher_studies', label: 'Higher Studies', desc: 'MS/PhD preparation' },
                                        { value: 'startup', label: 'Startup', desc: 'Build & launch products' },
                                        { value: 'research', label: 'Research', desc: 'AI/ML research focus' }
                                    ].map(goal => (
                                        <label key={goal.value} className="radio-card radio-card-large">
                                            <input
                                                type="radio"
                                                name="career_goal"
                                                value={goal.value}
                                                checked={formData.career_goal === goal.value}
                                                onChange={handleChange}
                                            />
                                            <span className="radio-content">
                                                <Target size={20} />
                                                <span className="radio-title">{goal.label}</span>
                                                <span className="radio-desc">{goal.desc}</span>
                                            </span>
                                        </label>
                                    ))}
                                </div>
                            </div>

                            <div className="form-actions">
                                <button
                                    type="button"
                                    className="btn btn-secondary btn-lg"
                                    onClick={handleBack}
                                >
                                    Back
                                </button>
                                <button
                                    type="submit"
                                    className="btn btn-primary btn-lg"
                                    disabled={loading}
                                >
                                    {loading ? (
                                        <span className="spinner spinner-sm"></span>
                                    ) : (
                                        <>
                                            Create Account
                                            <ArrowRight size={18} />
                                        </>
                                    )}
                                </button>
                            </div>
                        </div>
                    )}
                </form>

                {/* Footer */}
                <p className="auth-footer-text">
                    Already have an account?{' '}
                    <Link to="/login" className="auth-link">Sign in</Link>
                </p>
            </div>
        </div>
    );
}

export default Register;
