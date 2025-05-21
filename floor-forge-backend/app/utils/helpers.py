#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Utility helper functions for the FloorForge API.
"""

import os
import time
import json
import logging
import base64
from io import BytesIO
from PIL import Image

# Set up logging
logger = logging.getLogger(__name__)

def ensure_directory(directory_path):
    """
    Ensure a directory exists, create it if it doesn't.
    
    Args:
        directory_path (str): Path to the directory
        
    Returns:
        str: The directory path
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path, exist_ok=True)
        logger.info(f"Created directory: {directory_path}")
    return directory_path

def image_to_base64(image, format="PNG"):
    """
    Convert a PIL Image to a base64 encoded string.
    
    Args:
        image (PIL.Image): The image to convert
        format (str): The image format (PNG, JPEG, etc.)
        
    Returns:
        str: Base64 encoded image string
    """
    buffered = BytesIO()
    image.save(buffered, format=format)
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return f"data:image/{format.lower()};base64,{img_str}"

def base64_to_image(base64_str):
    """
    Convert a base64 encoded image string to a PIL Image.
    
    Args:
        base64_str (str): Base64 encoded image string
        
    Returns:
        PIL.Image: The decoded image
    """
    # Remove the data URL prefix if present
    if "base64," in base64_str:
        base64_str = base64_str.split("base64,")[1]
    
    img_data = base64.b64decode(base64_str)
    return Image.open(BytesIO(img_data))

def save_json(data, filepath):
    """
    Save data as a JSON file.
    
    Args:
        data (dict): The data to save
        filepath (str): Path to the output file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        logger.error(f"Error saving JSON to {filepath}: {e}")
        return False

def load_json(filepath):
    """
    Load data from a JSON file.
    
    Args:
        filepath (str): Path to the JSON file
        
    Returns:
        dict: The loaded data, or None if loading failed
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading JSON from {filepath}: {e}")
        return None

def generate_timestamp():
    """
    Generate a formatted timestamp for the current time.
    
    Returns:
        str: Formatted timestamp (YYYY-MM-DD_HH-MM-SS)
    """
    return time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

def clean_prompt(prompt):
    """
    Clean and normalize a user prompt.
    
    Args:
        prompt (str): The user prompt
        
    Returns:
        str: Cleaned prompt
    """
    # Remove leading/trailing whitespace
    prompt = prompt.strip()
    
    # Ensure the prompt ends with a period
    if prompt and not prompt.endswith(('.', '!', '?')):
        prompt += '.'
    
    return prompt

def get_file_size(filepath):
    """
    Get the size of a file in bytes.
    
    Args:
        filepath (str): Path to the file
        
    Returns:
        int: Size in bytes
    """
    try:
        return os.path.getsize(filepath)
    except Exception as e:
        logger.error(f"Error getting file size for {filepath}: {e}")
        return 0

def format_file_size(size_bytes):
    """
    Format a file size in bytes to a human-readable string.
    
    Args:
        size_bytes (int): Size in bytes
        
    Returns:
        str: Formatted size string
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024**2:
        return f"{size_bytes/1024:.1f} KB"
    elif size_bytes < 1024**3:
        return f"{size_bytes/1024**2:.1f} MB"
    else:
        return f"{size_bytes/1024**3:.1f} GB"