// src/services/api.js
/**
 * API service for communicating with the backend
 */

// API base URL - will use relative path for same-origin requests
const API_BASE_URL = "/api";

/**
 * Generic fetch wrapper with error handling
 * @param {string} endpoint - API endpoint
 * @param {Object} options - Fetch options
 * @returns {Promise<any>} Response data
 */
const fetchApi = async (endpoint, options = {}) => {
  try {
    // Set default headers
    const headers = {
      "Content-Type": "application/json",
      ...options.headers,
    };

    // Build request
    const url = `${API_BASE_URL}/${endpoint.replace(/^\//, "")}`;
    const response = await fetch(url, {
      ...options,
      headers,
    });

    // Check if response is JSON
    const contentType = response.headers.get("content-type");
    const isJson = contentType && contentType.includes("application/json");
    const data = isJson ? await response.json() : await response.text();

    // Handle error responses
    if (!response.ok) {
      throw new Error(
        isJson && data.message ? data.message : `API error: ${response.status}`
      );
    }

    return data;
  } catch (error) {
    console.error("API request failed:", error);
    throw error;
  }
};

/**
 * API service object with methods for different endpoints
 */
const apiService = {
  /**
   * Generate a floor plan based on a text prompt
   * @param {string} prompt - Text description of the floor plan
   * @param {Object} options - Additional generation options
   * @returns {Promise<Object>} Generated floor plan data
   */
  generateFloorPlan: async (prompt, options = {}) => {
    return fetchApi("generate-floor-plan", {
      method: "POST",
      body: JSON.stringify({
        prompt,
        num_inference_steps: options.numInferenceSteps || 50,
        guidance_scale: options.guidanceScale || 7.5,
        seed: options.seed,
      }),
    });
  },

  /**
   * Get a list of previously generated floor plans
   * @returns {Promise<Array>} List of floor plans
   */
  getFloorPlans: async () => {
    return fetchApi("floor-plans");
  },
};

export default apiService;
