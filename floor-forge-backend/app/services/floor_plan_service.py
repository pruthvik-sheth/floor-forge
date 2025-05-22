#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Business logic for floor plan generation.
"""

import os
import logging
from flask import current_app

# Import from within the application
from app.stable_diffusion.inference import load_model as load_inference_model
from app.stable_diffusion.inference import generate_floor_plan as generate_image

# Configure logging
logger = logging.getLogger(__name__)

def load_model():
    """
    Load the Stable Diffusion model.
    
    Returns:
        bool: True if loaded successfully
    """
    try:
        # Use the inference module to load the model
        success = load_inference_model()
        return success
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return False

def generate_floor_plan(
    prompt,
    output_filename=None,
    num_inference_steps=None,
    guidance_scale=None,
    seed=None
):
    """
    Generate a floor plan from a text prompt.
    
    Args:
        prompt (str): The text prompt describing the floor plan
        output_filename (str, optional): Filename for the output image
        num_inference_steps (int, optional): Number of inference steps
        guidance_scale (float, optional): Guidance scale for generation
        seed (int, optional): Random seed for reproducibility
        
    Returns:
        tuple: (image_path, generation_time)
    """
    try:
        # Use the inference module to generate the floor plan
        return generate_image(
            prompt=prompt,
            output_filename=output_filename,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            seed=seed
        )
    except Exception as e:
        logger.error(f"Error generating floor plan: {e}")
        raise