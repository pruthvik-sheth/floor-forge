import { useState, useCallback, useEffect } from "react";
import apiService from "../services/api";

/**
 * Custom hook for managing floor plan data and operations
 * @returns {Object} Floor plan state and methods
 */
const useFloorPlan = () => {
  // State for floor plans
  const [floorPlans, setFloorPlans] = useState([]);
  const [currentPlan, setCurrentPlan] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState(null);

  // Load initial floor plans
  useEffect(() => {
    const loadFloorPlans = async () => {
      try {
        setIsLoading(true);
        setError(null);

        // Fetch floor plans from the backend
        const data = await apiService.getFloorPlans();

        if (data && data.floorPlans && Array.isArray(data.floorPlans)) {
          setFloorPlans(data.floorPlans);
        } else {
          // If we don't have floor plans from the API yet, check localStorage
          const savedPlans = localStorage.getItem("floorPlans");
          if (savedPlans) {
            setFloorPlans(JSON.parse(savedPlans));
          }
        }
      } catch (err) {
        console.error("Failed to load floor plans:", err);

        // Try to load from localStorage as fallback
        const savedPlans = localStorage.getItem("floorPlans");
        if (savedPlans) {
          setFloorPlans(JSON.parse(savedPlans));
        }

        setError(
          "Failed to load floor plans from server. Using locally saved plans instead."
        );
      } finally {
        setIsLoading(false);
      }
    };

    loadFloorPlans();
  }, []);

  // Save floor plans to localStorage when they change
  useEffect(() => {
    if (floorPlans.length > 0) {
      localStorage.setItem("floorPlans", JSON.stringify(floorPlans));
    }
  }, [floorPlans]);

  /**
   * Generate a new floor plan based on prompt
   * @param {string} prompt - Text description of the floor plan
   * @param {Object} options - Generation options like numInferenceSteps, guidanceScale, seed
   */
  const generateFloorPlan = useCallback(async (prompt, options = {}) => {
    if (!prompt.trim()) {
      setError("Please enter a description for your floor plan");
      return null;
    }

    try {
      setIsGenerating(true);
      setError(null);

      // Call the API to generate a floor plan
      const data = await apiService.generateFloorPlan(prompt, options);

      // Create a floor plan object from the response
      const newFloorPlan = {
        id: data.id,
        prompt: data.prompt,
        imageUrl: data.imageUrl,
        createdAt: data.createdAt || new Date().toISOString(),
        parameters: data.parameters || {
          numInferenceSteps: options.numInferenceSteps || 50,
          guidanceScale: options.guidanceScale || 7.5,
          seed: options.seed || Math.floor(Math.random() * 1000000),
        },
        generationTime: data.generationTime || 0,
      };

      // Update state
      setCurrentPlan(newFloorPlan);
      setFloorPlans((prev) => [newFloorPlan, ...prev]);

      return newFloorPlan;
    } catch (err) {
      console.error("Failed to generate floor plan:", err);
      setError("Failed to generate floor plan. Please try again.");

      // If we're in development mode and API is not available, create a dummy floor plan
      if (process.env.NODE_ENV === "development") {
        console.log("Creating a demo floor plan for development");
        const demoFloorPlan = {
          id: Date.now().toString(),
          prompt,
          imageUrl:
            "https://placehold.co/600x600/e2e8f0/1e293b?text=Floor+Plan",
          createdAt: new Date().toISOString(),
          parameters: {
            numInferenceSteps: options.numInferenceSteps || 50,
            guidanceScale: options.guidanceScale || 7.5,
            seed: options.seed || Math.floor(Math.random() * 1000000),
          },
          generationTime: 1.5,
        };

        setCurrentPlan(demoFloorPlan);
        setFloorPlans((prev) => [demoFloorPlan, ...prev]);
        return demoFloorPlan;
      }

      return null;
    } finally {
      setIsGenerating(false);
    }
  }, []);

  /**
   * Save or update a floor plan
   * @param {Object} plan - Floor plan data
   */
  const saveFloorPlan = useCallback(
    async (plan) => {
      try {
        setIsLoading(true);
        setError(null);

        // For now, we'll just update locally since we don't have a save endpoint
        // In a real app, you would call an API to save the floor plan

        // Update state
        setFloorPlans((prev) => prev.map((p) => (p.id === plan.id ? plan : p)));

        if (currentPlan?.id === plan.id) {
          setCurrentPlan(plan);
        }

        return plan;
      } catch (err) {
        console.error("Failed to save floor plan:", err);
        setError("Failed to save floor plan. Please try again.");
        return null;
      } finally {
        setIsLoading(false);
      }
    },
    [currentPlan]
  );

  /**
   * Delete a floor plan
   * @param {string} id - Floor plan ID
   */
  const deleteFloorPlan = useCallback(
    async (id) => {
      try {
        setIsLoading(true);
        setError(null);

        // For now, we'll just update locally since we don't have a delete endpoint

        // Update state
        setFloorPlans((prev) => prev.filter((p) => p.id !== id));

        if (currentPlan?.id === id) {
          setCurrentPlan(null);
        }

        return true;
      } catch (err) {
        console.error("Failed to delete floor plan:", err);
        setError("Failed to delete floor plan. Please try again.");
        return false;
      } finally {
        setIsLoading(false);
      }
    },
    [currentPlan]
  );

  return {
    // State
    floorPlans,
    currentPlan,
    isLoading,
    isGenerating,
    error,

    // Actions
    setCurrentPlan,
    generateFloorPlan,
    saveFloorPlan,
    deleteFloorPlan,

    // Utility
    clearError: () => setError(null),
  };
};

export default useFloorPlan;
