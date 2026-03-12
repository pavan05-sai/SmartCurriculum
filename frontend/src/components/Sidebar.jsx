// SmartCurriculum - Sidebar Component
// Side navigation with menu items

import React from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import {
    LayoutDashboard, BookOpen,
    FileText, User, BookMarked, X, LogOut
} from 'lucide-react';
import { useAuth } from '../App';
import './Sidebar.css';

const menuItems = [
    { path: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { path: '/curriculum', label: 'My Curriculum', icon: BookOpen },
    { path: '/resume', label: 'Resume Skills', icon: FileText },
    { path: '/profile', label: 'Profile', icon: User },
];

function Sidebar({ isOpen, onToggle }) {
    const location = useLocation();
    const { logout } = useAuth();

    return (
        <>
            {/* Mobile Overlay */}
            {isOpen && (
                <div className="sidebar-overlay hide-desktop" onClick={onToggle} />
            )}

            <aside className={`sidebar ${isOpen ? 'open' : 'closed'}`}>
                {/* Logo */}
                <div className="sidebar-header">
                    <div className="logo">
                        <BookMarked className="logo-icon" size={28} />
                        <span className="logo-text">
                            Smart<span className="logo-highlight">Curriculum</span>
                        </span>
                    </div>
                    <button className="sidebar-close hide-desktop" onClick={onToggle}>
                        <X size={20} />
                    </button>
                </div>

                {/* Navigation */}
                <nav className="sidebar-nav">
                    <ul className="nav-list">
                        {menuItems.map((item) => (
                            <li key={item.path} className="nav-item">
                                <NavLink
                                    to={item.path}
                                    className={({ isActive }) =>
                                        `nav-link ${isActive ? 'active' : ''}`
                                    }
                                    onClick={() => window.innerWidth <= 768 && onToggle()}
                                >
                                    <item.icon size={20} className="nav-icon" />
                                    <span className="nav-label">{item.label}</span>
                                </NavLink>
                            </li>
                        ))}
                    </ul>
                </nav>

                <div className="sidebar-footer-actions">
                    <button onClick={logout} className="sidebar-logout-btn">
                        <LogOut size={20} />
                        <span>Logout</span>
                    </button>
                </div>


            </aside >
        </>
    );
}

export default Sidebar;
