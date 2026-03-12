// SmartCurriculum - AI Service
// AI features API functions

import api from './api';

/**
 * Get skill gap analysis
 */
export async function getSkillGap() {
    const response = await api.get('/ai/skill-gap');
    return response.data;
}

/**
 * Generate learning notes for a topic
 * @param {string} topic - Topic name
 * @param {string} detailLevel - Detail level (basic/intermediate/comprehensive)
 */
export async function generateNotes(topic, detailLevel = 'intermediate') {
    const response = await api.post('/ai/generate-notes', {
        topic,
        detail_level: detailLevel
    });
    return response.data;
}

/**
 * Generate MCQs for a topic
 * @param {string} topic - Topic name
 * @param {number} count - Number of questions
 * @param {string} difficulty - Difficulty level
 */
export async function generateMCQs(topic, count = 5, difficulty = 'intermediate') {
    const response = await api.post('/ai/generate-mcqs', {
        topic,
        count,
        difficulty
    });
    return response.data;
}

/**
 * Generate project ideas
 * @param {string} topic - Topic/skill area
 * @param {number} count - Number of projects
 */
export async function generateProjects(topic, count = 3) {
    const response = await api.post('/ai/generate-projects', {
        topic,
        count
    });
    return response.data;
}

/**
 * Generate coding problems
 * @param {string} topic - Topic
 * @param {number} count - Number of problems
 * @param {string} difficulty - Difficulty level
 */
export async function generateCodingProblems(topic, count = 3, difficulty = 'intermediate') {
    const response = await api.post('/ai/generate-coding-problems', {
        topic,
        count,
        difficulty
    });
    return response.data;
}

/**
 * Analyze syllabus
 * @param {string} syllabusText - Syllabus text
 */
export async function analyzeSyllabus(syllabusText) {
    const response = await api.post('/ai/analyze-syllabus', {
        syllabus: syllabusText
    });
    return response.data;
}

/**
 * Analyze job description
 * @param {string} jobDescription - Job description text
 */
export async function analyzeJob(jobDescription) {
    const response = await api.post('/ai/analyze-job', {
        job_description: jobDescription
    });
    return response.data;
}

/**
 * Get adaptive curriculum recommendations
 */
export async function getAdaptiveRecommendations() {
    const response = await api.get('/ai/adaptive-update');
    return response.data;
}
