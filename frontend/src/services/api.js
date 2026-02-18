import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE || '/api';

const api = axios.create({
    baseURL: API_BASE,
    timeout: 120000, // 2 min for AI operations
});

// ============================================
// Documents
// ============================================

export const uploadDocument = async (file, onProgress) => {
    const formData = new FormData();
    formData.append('file', file);
    const { data } = await api.post('/documents/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: onProgress,
    });
    return data;
};

export const getDocuments = async () => {
    const { data } = await api.get('/documents');
    return data;
};

export const getDocument = async (id) => {
    const { data } = await api.get(`/documents/${id}`);
    return data;
};

export const getDocumentStatus = async (id) => {
    const { data } = await api.get(`/documents/${id}/status`);
    return data;
};

export const deleteDocument = async (id) => {
    await api.delete(`/documents/${id}`);
};

export const getDocumentText = async (id) => {
    const { data } = await api.get(`/documents/${id}/text`);
    return data;
};

// ============================================
// Insights
// ============================================

export const summarizeDocument = async (id) => {
    const { data } = await api.post(`/documents/${id}/summarize`);
    return data;
};

export const extractDocument = async (id, docType = 'general') => {
    const { data } = await api.post(`/documents/${id}/extract`, { document_type: docType });
    return data;
};

export const detectRisks = async (id) => {
    const { data } = await api.post(`/documents/${id}/risks`);
    return data;
};

export const getInsights = async (id) => {
    const { data } = await api.get(`/documents/${id}/insights`);
    return data;
};

// ============================================
// Search
// ============================================

export const semanticSearch = async (query, topK = 5, documentId = null) => {
    const { data } = await api.post('/search', {
        query,
        top_k: topK,
        document_id: documentId,
    });
    return data;
};

// ============================================
// Chat
// ============================================

export const chatWithDocument = async (id, question) => {
    const { data } = await api.post(`/documents/${id}/chat`, { question });
    return data;
};

export const getChatHistory = async (id) => {
    const { data } = await api.get(`/documents/${id}/chat/history`);
    return data;
};

// ============================================
// Compare
// ============================================

export const compareDocuments = async (documentIds, comparisonType = 'general') => {
    const { data } = await api.post('/compare', {
        document_ids: documentIds,
        comparison_type: comparisonType,
    });
    return data;
};

// ============================================
// Dashboard
// ============================================

export const getDashboardStats = async () => {
    const { data } = await api.get('/dashboard/stats');
    return data;
};

export const getRiskOverview = async () => {
    const { data } = await api.get('/dashboard/risks');
    return data;
};

export const getTimeline = async () => {
    const { data } = await api.get('/dashboard/timeline');
    return data;
};

export default api;
