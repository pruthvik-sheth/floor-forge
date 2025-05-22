#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Business logic for floor plan generation.
"""

import os
import time
import json
import uuid
import logging
import torch
from flask import current_app
from diffusers import StableDiffusionPipeline
from app.utils.helpers import ensure_directory, save_json, generate_timestamp

# Configure logging
logger = logging.getLogger(__name__)

# Global variable to store the pipeline
_pipeline = None

def load_model():
    """
    Load the Stable Diffusion model.
    
    Returns:
        bool: True if loaded successfully
    """
    global _pipeline
    
    try:
        # Get the pipeline path from configuration
        pipeline_path = current_app.config.get("PIPELINE_PATH")
        base_model_id = current_app.config.get("BASE_MODEL_ID", "stabilityai/stable-diffusion-2-1-base")
        
        # Log the paths
        logger.info(f"Attempting to load model from: {pipeline_path}")
        logger.info(f"Fallback model ID: {base_model_id}")
        
        # Check if pipeline exists
        if not os.path.exists(pipeline_path):
            logger.warning(f"Custom model not found at {pipeline_path}, falling back to {base_model_id}")
            model_path = base_model_id
        else:
            logger.info(f"Found custom model at {pipeline_path}")
            model_path = pipeline_path
        
        # Check device
        device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {device}")
        
        # Set dtype based on device
        dtype = torch.float16 if device == "cuda" else torch.float32
        
        # Load the pipeline
        _pipeline = StableDiffusionPipeline.from_pretrained(
            model_path,
            torch_dtype=dtype,
            safety_checker=None
        )
        
        # Move to device
        _pipeline = _pipeline.to(device)
        
        # Apply basic optimizations
        if device == "cuda":
            _pipeline.enable_attention_slicing()
            # Try to enable xformers if available
            try:
                _pipeline.enable_xformers_memory_efficient_attention()
                logger.info("Enabled xformers memory efficient attention")
            except:
                logger.info("Xformers not available, using default attention")
        
        logger.info("Pipeline loaded successfully!")
        return True
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return False

def get_pipeline():
    """
    Get the loaded pipeline or load it if not already loaded.
    
    Returns:
        StableDiffusionPipeline: The loaded pipeline
    """
    global _pipeline
    
    if _pipeline is None:
        load_model()
    
    return _pipeline

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
    # Set default values from configuration if not provided
    if num_inference_steps is None:
        num_inference_steps = current_app.config.get("DEFAULT_NUM_INFERENCE_STEPS", 50)
    
    if guidance_scale is None:
        guidance_scale = current_app.config.get("DEFAULT_GUIDANCE_SCALE", 7.5)
    
    # Set output filename if not provided
    if output_filename is None:
        output_filename = f"{uuid.uuid4()}.png"
    
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
        
        # Set up generator if seed provided
        if seed is not None:
            generator = torch.Generator(device=pipeline.device).manual_seed(seed)
        else:
            generator = None
        
        # Generate image
        result = pipeline(
            prompt=prompt,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            generator=generator
        )
        
        # Get image from result
        image = result.images[0]
        
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