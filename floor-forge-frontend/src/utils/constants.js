/**
 * Application constants for the FloorForge application
 */

// API configuration
export const API = {
  BASE_URL: "/api",
  ENDPOINTS: {
    GENERATE_FLOOR_PLAN: "generate-floor-plan",
    FLOOR_PLANS: "floor-plans",
  },
  TIMEOUT: 30000, // 30 seconds
};

// Local storage keys
export const STORAGE = {
  FLOOR_PLANS: "floorPlans",
  USER_PREFERENCES: "floorForgePreferences",
  AUTH_TOKEN: "floorForgeAuthToken",
};

// Room types for floor plans
export const ROOM_TYPES = {
  BEDROOM: "bedroom",
  BATHROOM: "bathroom",
  KITCHEN: "kitchen",
  LIVING_ROOM: "living room",
  DINING_ROOM: "dining room",
  OFFICE: "office",
  STUDY: "study room",
  BALCONY: "balcony",
  PATIO: "patio",
  GARAGE: "garage",
  LAUNDRY: "laundry room",
  STORAGE: "storage room",
  HALLWAY: "hallway",
  ENTRYWAY: "entryway",
};

// Floor plan styles
export const FLOOR_PLAN_STYLES = [
  { id: "modern", label: "Modern" },
  { id: "traditional", label: "Traditional" },
  { id: "minimalist", label: "Minimalist" },
  { id: "industrial", label: "Industrial" },
  { id: "scandinavian", label: "Scandinavian" },
  { id: "rustic", label: "Rustic" },
  { id: "contemporary", label: "Contemporary" },
  { id: "farmhouse", label: "Farmhouse" },
];

// Sample prompts for inspiration
export const SAMPLE_PROMPTS = [
  "A modern one-bedroom apartment with an open kitchen and living room",
  "A spacious three-bedroom house with two bathrooms and a large backyard",
  "A minimalist studio apartment with a kitchen island and built-in storage",
  "A two-story family home with four bedrooms and a home office",
  "A luxury penthouse with a wraparound balcony and floor-to-ceiling windows",
  "A cozy cabin with a loft bedroom and wood-burning fireplace",
  "A traditional farmhouse with a large kitchen, dining room, and front porch",
  "An industrial loft with exposed brick walls and open concept layout",
  "A beach house with three bedrooms and a large deck overlooking the ocean",
  "A compact tiny house with smart storage solutions and multifunctional furniture",
];

// Error messages
export const ERRORS = {
  GENERATION_FAILED: "Failed to generate floor plan. Please try again.",
  EMPTY_PROMPT: "Please enter a description for your floor plan.",
  NETWORK_ERROR: "Network error. Please check your connection and try again.",
  SERVER_ERROR: "Server error. Our team has been notified.",
  UNAUTHORIZED: "You must be logged in to perform this action.",
  FORBIDDEN: "You do not have permission to perform this action.",
  NOT_FOUND: "The requested resource was not found.",
};

// Dimensions
export const DIMENSIONS = {
  MAX_IMAGE_SIZE: 2048, // pixels
  THUMBNAIL_SIZE: 200, // pixels
  PREVIEW_SIZE: 600, // pixels
};

// Animation durations (ms)
export const ANIMATION = {
  FAST: 150,
  NORMAL: 300,
  SLOW: 500,
};

// Maximum lengths
export const MAX_LENGTHS = {
  PROMPT: 500,
  NAME: 100,
  DESCRIPTION: 1000,
};

// File types
export const FILE_TYPES = {
  PNG: "image/png",
  JPEG: "image/jpeg",
  SVG: "image/svg+xml",
  PDF: "application/pdf",
};

// Color palette (matching our theme)
export const COLORS = {
  PRIMARY: "#546e7a",
  SECONDARY: "#78909c",
  ACCENT: "#ff9800",
  SUCCESS: "#4caf50",
  WARNING: "#ff9800",
  ERROR: "#f44336",
  BACKGROUND: "#ffffff",
  FOREGROUND: "#263238",
  SURFACE: "#eceff1",
  MUTED: "#90a4ae",
};
