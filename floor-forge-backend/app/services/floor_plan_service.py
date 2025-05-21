#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Business logic for floor plan generation.
"""

import os
import time
import json  # Add this import for JSON handling
import uuid
import logging
import torch  # Add this import for torch
from flask import current_app

# Import from within the application
from app.stable_diffusion.inference import generate_floor_plan as generate_image
from app.stable_diffusion.model_loader import get_pipeline
from app.utils.helpers import ensure_directory, save_json, generate_timestamp

# Configure logging
logger = logging.getLogger(__name__)

def load_model():
    """
    Load the Stable Diffusion model.
    
    Returns:
        bool: True if loaded successfully
    """
    try:
        # Get the pipeline path from configuration
        pipeline_path = current_app.config.get("PIPELINE_PATH")
        base_model_id = current_app.config.get("BASE_MODEL_ID", "stabilityai/stable-diffusion-2-1-base")
        
        # Log the paths
        logger.info(f"Attempting to load model from: {pipeline_path}")
        logger.info(f"Fallback model ID: {base_model_id}")
        
        # Try to load the pipeline
        pipeline = get_pipeline(
            pipeline_path=pipeline_path,
            model_id=base_model_id
        )
        
        # If we get here, the pipeline was loaded successfully
        return pipeline is not None
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return False

# Removed prompt enhancement function to use raw prompts only

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
        enhance_prompt_flag (bool): Whether to enhance the prompt
        
    Returns:
        tuple: (image_path, generation_time)
    """
    # Set default values from configuration if not provided
    # if num_inference_steps is None:
    num_inference_steps = 10
    
    if guidance_scale is None:
        guidance_scale = current_app.config.get("DEFAULT_GUIDANCE_SCALE", 7.5)
    
    # Set output filename if not provided
    if output_filename is None:
        output_filename = f"floor_plan_{uuid.uuid4()}.png"
    
    # Ensure the output directory exists
    output_dir = current_app.config.get("GENERATED_IMAGES_DIR")
    ensure_directory(output_dir)
    
    # Full path for the output image
    output_path = os.path.join(output_dir, output_filename)
    
    try:
        # Log the generation attempt
        logger.info(f"Generating floor plan with prompt: '{prompt}'")
        logger.info(f"Using {num_inference_steps} inference steps and guidance scale {guidance_scale}")
        
        # Start the timer
        start_time = time.time()
        
        # Make sure the model is loaded
        pipeline = get_pipeline()
        
        # Generate the image
        with torch.no_grad():
            output = pipeline(
                prompt=prompt,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                generator=None if seed is None else torch.Generator(device=pipeline.device).manual_seed(seed)
            )
        
        # Get the image from the result
        image = output.images[0]
        
        # Save the image
        image.save(output_path)
        
        # Calculate generation time
        generation_time = time.time() - start_time
        
        # Log the success
        logger.info(f"Floor plan generated in {generation_time:.2f} seconds")
        logger.info(f"Saved to {output_path}")
        
        # Save metadata
        metadata = {
            "prompt": prompt,
            "num_inference_steps": num_inference_steps,
            "guidance_scale": guidance_scale,
            "seed": seed,
            "generation_time": generation_time,
            "output_path": output_path,
            "timestamp": generate_timestamp()
        }
        
        # Save metadata to a JSON file
        metadata_path = os.path.splitext(output_path)[0] + ".json"
        save_json(metadata, metadata_path)
        
        return output_path, generation_time
        
    except Exception as e:
        logger.error(f"Error generating floor plan: {e}")
        raise