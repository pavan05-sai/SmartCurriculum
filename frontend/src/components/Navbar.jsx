// SmartCurriculum - Navbar Component
// Top navigation bar with user menu

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../App';
import {
    Menu, Bell, Search, ChevronDown, User, Settings, LogOut
} from 'lucide-react';
import './Navbar.css';

function Navbar({ onMenuClick }) {
    const { user, logout } = useAuth();
    const navigate = useNavigate();
    const [dropdownOpen, setDropdownOpen] = useState(false);

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    const getInitials = (name) => {
        if (!name) return 'U';
        return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
    };

    return (
        <nav className="navbar">
            <div className="navbar-left">
                <button className="navbar-menu-btn hide-desktop" onClick={onMenuClick}>
                    <Menu size={24} />
                </button>

                <div className="navbar-search">
                    <Search size={18} className="search-icon" />
                    <input
                        type="text"
                        placeholder="Search topics, skills..."
                        className="search-input"
                    />
                </div>
            </div>

            <div className="navbar-right">
                <button className="navbar-icon-btn">
                    <Bell size={20} />
                    <span className="notification-dot"></span>
                </button>

                <div className="navbar-user">
                    <button
                        className="user-menu-btn"
                        onClick={() => setDropdownOpen(!dropdownOpen)}
                    >
                        <div className="avatar avatar-sm">
                            {getInitials(user?.name)}
                        </div>
                        <span className="user-name hide-mobile">
                            {user?.name || 'User'}
                        </span>
                        <ChevronDown size={16} className={`dropdown-arrow ${dropdownOpen ? 'rotate' : ''}`} />
                    </button>

                    {dropdownOpen && (
                        <>
                            <div className="dropdown-backdrop" onClick={() => setDropdownOpen(false)} />
                            <div className="dropdown-menu">
                                <div className="dropdown-header">
                                    <div className="avatar">{getInitials(user?.name)}</div>
                                    <div className="user-info">
                                        <span className="user-name">{user?.name}</span>
                                        <span className="user-email">{user?.email}</span>
                                    </div>
                                </div>
                                <div className="dropdown-divider" />
                                <button
                                    className="dropdown-item"
                                    onClick={() => { setDropdownOpen(false); navigate('/profile'); }}
                                >
                                    <User size={16} />
                                    My Profile
                                </button>
                                <button
                                    className="dropdown-item"
                                    onClick={() => { setDropdownOpen(false); navigate('/profile'); }}
                                >
                                    <Settings size={16} />
                                    Settings
                                </button>
                                <div className="dropdown-divider" />
                                <button
                                    className="dropdown-item text-error"
                                    onClick={handleLogout}
                                >
                                    <LogOut size={16} />
                                    Logout
                                </button>
                            </div>
                        </>
                    )}
                </div>
            </div>
        </nav>
    );
}

export default Navbar;
