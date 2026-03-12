// SmartCurriculum - API Service
// Axios instance with auth interceptors

import axios from 'axios';

// Create axios instance
const api = axios.create({
    baseURL: '/api',
    headers: {
        'Content-Type': 'application/json'
    },
    timeout: 30000
});

// Request interceptor - add auth token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor - handle token refresh
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        // If 401 and not already retried
        // Also don't retry if the request itself was an auth request to avoid loops
        const isAuthRequest = originalRequest.url.includes('/auth/login') ||
            originalRequest.url.includes('/auth/register') ||
            originalRequest.url.includes('/auth/refresh');

        if (error.response?.status === 401 && !originalRequest._retry && !isAuthRequest) {
            originalRequest._retry = true;

            try {
                const refreshToken = localStorage.getItem('refresh_token');
                if (refreshToken) {
                    // Use standard axios for refresh to avoid infinite interceptor loop
                    // Send refresh token in Authorization header as expected by Flask-JWT-Extended
                    const response = await axios.post('/api/auth/refresh', {}, {
                        headers: {
                            Authorization: `Bearer ${refreshToken}`
                        }
                    });

                    const { access_token } = response.data;
                    localStorage.setItem('access_token', access_token);

                    // Update existing request header and retry
                    originalRequest.headers.Authorization = `Bearer ${access_token}`;
                    return axios(originalRequest);
                }
            } catch (refreshError) {
                // Refresh failed or no refresh token, logout and redirect
                console.error('Session expired or refresh failed:', refreshError);
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');

                // Only redirect if we are not already on the login or register page
                if (!window.location.pathname.includes('/login') &&
                    !window.location.pathname.includes('/register')) {
                    window.location.href = '/login';
                }
            }
        }

        return Promise.reject(error);
    }
);

export default api;
