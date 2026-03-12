// SmartCurriculum - Main App Component
// React Router setup and authentication provider

import React, { useState, useEffect, createContext, useContext } from 'react';
import { BrowserRouter, Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import { getProfile, logout as logoutService } from './services/auth';

// Pages
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Profile from './pages/Profile';
import Curriculum from './pages/Curriculum';
import Resume from './pages/Resume';

// Components
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import LoadingSpinner from './components/LoadingSpinner';
import Chatbot from './components/Chatbot';

// Create Auth Context
const AuthContext = createContext(null);

// Auth Provider Component
function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    // Check authentication on mount
    useEffect(() => {
        checkAuth();
    }, []);

    const checkAuth = async () => {
        const token = localStorage.getItem('access_token');
        if (!token) {
            setLoading(false);
            return;
        }

        try {
            const response = await getProfile();
            setUser(response.user);
            setIsAuthenticated(true);
        } catch (error) {
            console.error('Auth check failed:', error);
            // Only clear tokens if the error is 401 (meaning refresh failed too)
            if (error.response?.status === 401) {
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                setIsAuthenticated(false);
            }
        } finally {
            setLoading(false);
        }
    };

    const login = (userData, accessToken, refreshToken) => {
        localStorage.setItem('access_token', accessToken);
        localStorage.setItem('refresh_token', refreshToken);
        setUser(userData);
        setIsAuthenticated(true);
    };

    const logout = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        setUser(null);
        setIsAuthenticated(false);
    };

    const updateUser = (userData) => {
        setUser(userData);
    };

    return (
        <AuthContext.Provider value={{ user, isAuthenticated, loading, login, logout, updateUser }}>
            {children}
        </AuthContext.Provider>
    );
}

// Custom hook to use auth context
export function useAuth() {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
}

// Protected Route Component
function ProtectedRoute({ children }) {
    const { isAuthenticated, loading } = useAuth();

    if (loading) {
        return (
            <div className="loading-overlay">
                <LoadingSpinner size="lg" />
            </div>
        );
    }

    if (!isAuthenticated) {
        return <Navigate to="/login" replace />;
    }

    return children;
}

// Auth Layout (for login/register pages)
function AuthLayout({ children }) {
    return (
        <div className="auth-layout">
            <div className="main-content">
                {children}
            </div>
        </div>
    );
}

// Dashboard Layout (for authenticated pages)
function DashboardLayout({ children }) {
    const [sidebarOpen, setSidebarOpen] = useState(true);

    const toggleSidebar = () => {
        setSidebarOpen(!sidebarOpen);
    };

    return (
        <div className="app-container">
            <Sidebar isOpen={sidebarOpen} onToggle={toggleSidebar} />
            <div className={`main-content ${!sidebarOpen ? 'sidebar-collapsed' : ''}`}>
                <Navbar onMenuClick={toggleSidebar} />
                <div className="page-container animate-fade-in">
                    {children}
                </div>
            </div>
            <Chatbot />
        </div>
    );
}

// Main App Component
function App() {
    return (
        <BrowserRouter>
            <AuthProvider>
                <AppRoutes />
            </AuthProvider>
        </BrowserRouter>
    );
}

// App Routes Component
function AppRoutes() {
    const { isAuthenticated, loading } = useAuth();

    if (loading) {
        return (
            <div className="loading-overlay">
                <LoadingSpinner size="lg" />
            </div>
        );
    }

    return (
        <Routes>
            {/* Auth Routes */}
            <Route
                path="/login"
                element={
                    isAuthenticated ? (
                        <Navigate to="/dashboard" replace />
                    ) : (
                        <AuthLayout>
                            <Login />
                        </AuthLayout>
                    )
                }
            />
            <Route
                path="/register"
                element={
                    isAuthenticated ? (
                        <Navigate to="/dashboard" replace />
                    ) : (
                        <AuthLayout>
                            <Register />
                        </AuthLayout>
                    )
                }
            />

            {/* Protected Routes */}
            <Route
                path="/dashboard"
                element={
                    <ProtectedRoute>
                        <DashboardLayout>
                            <Dashboard />
                        </DashboardLayout>
                    </ProtectedRoute>
                }
            />
            <Route
                path="/profile"
                element={
                    <ProtectedRoute>
                        <DashboardLayout>
                            <Profile />
                        </DashboardLayout>
                    </ProtectedRoute>
                }
            />
            <Route
                path="/curriculum"
                element={
                    <ProtectedRoute>
                        <DashboardLayout>
                            <Curriculum />
                        </DashboardLayout>
                    </ProtectedRoute>
                }
            />
            <Route
                path="/resume"
                element={
                    <ProtectedRoute>
                        <DashboardLayout>
                            <Resume />
                        </DashboardLayout>
                    </ProtectedRoute>
                }
            />

            {/* Default Routes */}
            <Route path="/" element={<Navigate to={isAuthenticated ? "/dashboard" : "/login"} replace />} />
            <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
    );
}

export default App;
