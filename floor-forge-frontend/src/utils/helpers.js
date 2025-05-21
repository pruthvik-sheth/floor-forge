/**
 * Utility helper functions for the FloorForge application
 */

/**
 * Format a date string or timestamp into a human-readable format
 * @param {string|number} dateInput - Date string, ISO string, or timestamp
 * @param {Object} options - Intl.DateTimeFormat options
 * @returns {string} Formatted date string
 */
export const formatDate = (dateInput, options = {}) => {
  if (!dateInput) return "N/A";

  const date = new Date(dateInput);

  // Check if date is valid
  if (isNaN(date.getTime())) return "Invalid date";

  // Default options
  const defaultOptions = {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    ...options,
  };

  return new Intl.DateTimeFormat("en-US", defaultOptions).format(date);
};

/**
 * Truncate a string to a specified length and add ellipsis if needed
 * @param {string} str - String to truncate
 * @param {number} maxLength - Maximum length before truncation
 * @returns {string} Truncated string
 */
export const truncateString = (str, maxLength = 100) => {
  if (!str || str.length <= maxLength) return str;
  return `${str.substring(0, maxLength).trim()}...`;
};

/**
 * Generate a unique ID for temporary use
 * Note: Not for security-critical applications
 * @returns {string} Unique ID
 */
export const generateId = () => {
  return Date.now().toString(36) + Math.random().toString(36).substring(2, 9);
};

/**
 * Download data as a file
 * @param {Object|string} data - Data to download
 * @param {string} filename - Name of the file
 * @param {string} type - MIME type of the file
 */
export const downloadFile = (data, filename, type = "text/plain") => {
  // Convert data to appropriate format if needed
  let content = data;
  if (typeof data === "object") {
    content = JSON.stringify(data, null, 2);
    type = "application/json";
  }

  // Create blob and link
  const blob = new Blob([content], { type });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");

  // Set link properties
  link.href = url;
  link.download = filename;

  // Trigger download
  document.body.appendChild(link);
  link.click();

  // Clean up
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
};

/**
 * Get file extension from a filename or path
 * @param {string} filename - Filename or path
 * @returns {string} File extension without the dot
 */
export const getFileExtension = (filename) => {
  if (!filename) return "";
  return filename.split(".").pop().toLowerCase();
};

/**
 * Convert byte size to human-readable format
 * @param {number} bytes - Size in bytes
 * @param {number} decimals - Number of decimal places
 * @returns {string} Formatted size string
 */
export const formatFileSize = (bytes, decimals = 2) => {
  if (bytes === 0) return "0 Bytes";

  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB", "TB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(decimals))} ${
    sizes[i]
  }`;
};

/**
 * Debounce a function call
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @returns {Function} Debounced function
 */
export const debounce = (func, wait = 300) => {
  let timeout;

  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };

    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
};

/**
 * Convert a prompt to a searchable slug
 * @param {string} prompt - Input text
 * @returns {string} URL-friendly slug
 */
export const createSlugFromPrompt = (prompt) => {
  if (!prompt) return "";

  // Extract key terms and create slug
  return prompt
    .toLowerCase()
    .replace(/[^\w\s-]/g, "") // Remove special characters
    .replace(/\s+/g, "-") // Replace spaces with hyphens
    .replace(/-+/g, "-") // Remove consecutive hyphens
    .substring(0, 60) // Limit length
    .replace(/^-+|-+$/g, ""); // Remove leading/trailing hyphens
};

/**
 * Extract room information from a floor plan prompt
 * @param {string} prompt - Floor plan description
 * @returns {Object} Room counts and features
 */
export const extractRoomInfo = (prompt) => {
  if (!prompt) return {};

  const roomTypes = [
    "bedroom",
    "bathroom",
    "kitchen",
    "living room",
    "dining room",
    "office",
    "studio",
    "balcony",
    "patio",
    "garage",
  ];

  const result = {};

  // Count room mentions
  roomTypes.forEach((type) => {
    // Look for patterns like "2 bedrooms" or "one bedroom"
    const patterns = [
      new RegExp(`(\\d+)\\s+${type}s?`, "i"),
      new RegExp(`(one|two|three|four|five)\\s+${type}s?`, "i"),
    ];

    // Check each pattern
    for (const pattern of patterns) {
      const match = prompt.match(pattern);
      if (match) {
        // Convert text numbers to digits if needed
        let count = match[1];
        if (isNaN(count)) {
          const textToNumber = {
            one: 1,
            two: 2,
            three: 3,
            four: 4,
            five: 5,
          };
          count = textToNumber[count.toLowerCase()] || 1;
        }

        result[type] = parseInt(count, 10);
        break;
      }
    }

    // Check for simple mentions without a number (assume 1)
    if (!result[type] && new RegExp(`\\b${type}\\b`, "i").test(prompt)) {
      result[type] = 1;
    }
  });

  return result;
};
