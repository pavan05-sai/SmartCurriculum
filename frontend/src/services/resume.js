// SmartCurriculum - Resume Service
// Resume and skills API functions

import api from './api';

/**
 * Get user's skills
 */
export async function getSkills() {
    const response = await api.get('/resume/skills');
    return response.data;
}

/**
 * Add a new skill
 * @param {object} skillData - Skill data
 */
export async function addSkill(skillData) {
    const response = await api.post('/resume/skills', skillData);
    return response.data;
}

/**
 * Update a skill
 * @param {number} skillId - Skill ID
 * @param {object} skillData - Updated skill data
 */
export async function updateSkill(skillId, skillData) {
    const response = await api.put(`/resume/skills/${skillId}`, skillData);
    return response.data;
}

/**
 * Delete a skill
 * @param {number} skillId - Skill ID
 */
export async function deleteSkill(skillId) {
    const response = await api.delete(`/resume/skills/${skillId}`);
    return response.data;
}

/**
 * Generate resume bullet point for a skill
 * @param {number} skillId - Skill ID
 */
export async function generateBullet(skillId) {
    const response = await api.post(`/resume/skills/${skillId}/generate-bullet`);
    return response.data;
}

/**
 * Export skills for resume
 * @param {string} format - Export format (text/markdown)
 */
export async function exportSkills(format = 'text') {
    const response = await api.get(`/resume/export?format=${format}`);
    return response.data;
}

/**
 * Match skills against a job description
 * @param {string} jobDescription - Job description text
 */
export async function matchJobSkills(jobDescription) {
    const response = await api.post('/resume/match', {
        job_description: jobDescription
    });
    return response.data;
}
