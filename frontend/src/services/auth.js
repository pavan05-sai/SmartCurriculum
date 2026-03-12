// SmartCurriculum - Auth Service
// Authentication API functions

import api from './api';

/**
 * Register a new user
 * @param {object} userData - User registration data
 */
export async function register(userData) {
    const response = await api.post('/auth/register', userData);
    return response.data;
}

/**
 * Login user
 * @param {string} email - User email
 * @param {string} password - User password
 */
export async function login(email, password) {
    const response = await api.post('/auth/login', { email, password });
    return response.data;
}

/**
 * Get current user profile
 */
export async function getProfile() {
    const response = await api.get('/auth/profile');
    return response.data;
}

/**
 * Update user profile
 * @param {object} profileData - Profile update data
 */
export async function updateProfile(profileData) {
    const response = await api.put('/auth/profile', profileData);
    return response.data;
}

/**
 * Change user password
 * @param {string} currentPassword - Current password
 * @param {string} newPassword - New password
 */
export async function changePassword(currentPassword, newPassword) {
    const response = await api.put('/auth/password', {
        current_password: currentPassword,
        new_password: newPassword
    });
    return response.data;
}

/**
 * Logout user (client-side only)
 */
export function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
}
