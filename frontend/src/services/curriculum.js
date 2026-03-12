// SmartCurriculum - Curriculum Service
// Curriculum and topic API functions

import api from './api';

/**
 * Generate a new curriculum for the user
 * @param {object} options - Generation options
 */
export async function generateCurriculum(options = {}) {
    const response = await api.post('/curriculum/generate', options);
    return response.data;
}

/**
 * Get user's curricula
 */
export async function getCurricula() {
    const response = await api.get('/curriculum');
    return response.data;
}

/**
 * Get a specific curriculum by ID
 * @param {number} curriculumId - Curriculum ID
 */
export async function getCurriculum(curriculumId) {
    const response = await api.get(`/curriculum/${curriculumId}`);
    return response.data;
}

/**
 * Get curriculum roadmap (topics organized by week)
 * @param {number} curriculumId - Curriculum ID
 */
export async function getRoadmap(curriculumId) {
    const response = await api.get(`/curriculum/${curriculumId}/roadmap`);
    return response.data;
}

/**
 * Mark a topic as completed
 * @param {number} curriculumId - Curriculum ID
 * @param {number} topicId - Topic ID
 * @param {number} score - Completion score
 */
export async function completeTopic(curriculumId, topicId, score = 100) {
    const response = await api.post(`/curriculum/${curriculumId}/topics/${topicId}/complete`, {
        score
    });
    return response.data;
}

/**
 * Download curriculum as PDF
 * @param {number} curriculumId - Curriculum ID
 */
export async function downloadPDF(curriculumId) {
    const response = await api.get(`/curriculum/${curriculumId}/pdf`, {
        responseType: 'blob'
    });

    // Create download link
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `curriculum_${curriculumId}.pdf`);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
}
/**
 * Update completed skills for a topic
 * @param {number} topicId - Topic ID
 * @param {string[]} completedSkills - List of completed skill strings
 */
export async function updateTopicSkills(topicId, completedSkills) {
    const response = await api.put(`/curriculum/topic/${topicId}/skills`, {
        completed_skills: completedSkills
    });
    return response.data;
}
