/**
 * API Communication Layer for ChurnScope Dashboard.
 * Handles all fetch requests to the Flask backend.
 */

const API_BASE = window.location.origin + '/api';

const ChurnAPI = {
    /**
     * Generic GET request.
     */
    async get(endpoint) {
        try {
            const response = await fetch(`${API_BASE}${endpoint}`);
            if (!response.ok) throw new Error(`API Error: ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error(`GET ${endpoint} failed:`, error);
            throw error;
        }
    },

    /**
     * Generic POST request.
     */
    async post(endpoint, data) {
        try {
            const response = await fetch(`${API_BASE}${endpoint}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            if (!response.ok) throw new Error(`API Error: ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error(`POST ${endpoint} failed:`, error);
            throw error;
        }
    },

    // --- Analytics Endpoints ---
    getOverview: ()          => ChurnAPI.get('/overview'),
    getChurnDist: ()         => ChurnAPI.get('/churn-distribution'),
    getDemographics: ()      => ChurnAPI.get('/demographics'),
    getServices: ()          => ChurnAPI.get('/services'),
    getContracts: ()         => ChurnAPI.get('/contracts'),
    getTenure: ()            => ChurnAPI.get('/tenure'),
    getCharges: ()           => ChurnAPI.get('/charges'),
    getCorrelation: ()       => ChurnAPI.get('/correlation'),

    // --- Model Endpoints ---
    getModelPerformance: ()  => ChurnAPI.get('/model-performance'),
    getFeatureImportance: () => ChurnAPI.get('/feature-importance'),
    getRiskSegments: ()      => ChurnAPI.get('/risk-segments'),

    // --- Prediction ---
    predict: (data)          => ChurnAPI.post('/predict', data),

    // --- Health ---
    healthCheck: ()          => ChurnAPI.get('/health'),
};
