#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
API routes for floor plan generation.
"""

import os
import uuid
import time
import json  # Add this import
import logging
import torch
from flask import Blueprint, request, jsonify, current_app, url_for, send_from_directory

# Import services
from app.services.floor_plan_service import generate_floor_plan, load_model

# Configure logging
logger = logging.getLogger(__name__)

# Create a blueprint for floor plan routes
floor_plan_bp = Blueprint("floor_plan", __name__)


@floor_plan_bp.route("/generate-floor-plan", methods=["POST"])
def create_floor_plan():
    """
    Generate a floor plan from a text prompt.
    
    Expected JSON body:
    {
        "prompt": "A modern one-bedroom apartment with an open kitchen and living room",
        "num_inference_steps": 50,  # Optional
        "guidance_scale": 7.5,      # Optional
        "seed": 42                  # Optional
    }
    
    Returns:
        JSON with the generated floor plan details
    """
    # Get request data
    data = request.get_json()
    
    # Validate input
    if not data or "prompt" not in data:
        return jsonify({
            "error": "Bad Request",
            "message": "Missing required field: prompt"
        }), 400
    
    prompt = data.get("prompt")
    
    # Validate prompt
    if not prompt or not isinstance(prompt, str) or len(prompt.strip()) == 0:
        return jsonify({
            "error": "Bad Request",
            "message": "Invalid prompt: must be a non-empty string"
        }), 400
    
    # Get optional parameters with defaults
    num_inference_steps = data.get("num_inference_steps", 
                                  current_app.config["DEFAULT_NUM_INFERENCE_STEPS"])
    guidance_scale = data.get("guidance_scale", 
                             current_app.config["DEFAULT_GUIDANCE_SCALE"])
    seed = data.get("seed")  # Allow None for random seed
    
    try:
        # Make sure model is loaded (this will be a no-op if already loaded)
        load_model()
        
        # Generate a unique ID for this floor plan
        floor_plan_id = str(uuid.uuid4())
        
        # Generate the floor plan - use the exact approach from Colab
        image_path, generation_time = generate_floor_plan(
            prompt=prompt,
            output_filename=f"{floor_plan_id}.png",
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            seed=seed
        )
        
        # Get the relative path for URL
        image_filename = os.path.basename(image_path)
        
        # Construct the URL for the generated image
        image_url = url_for('floor_plan.get_floor_plan_image', 
                           filename=image_filename, 
                           _external=True)
        
        # Return the result
        return jsonify({
            "id": floor_plan_id,
            "prompt": prompt,
            "imageUrl": image_url,
            "generationTime": generation_time,
            "parameters": {
                "numInferenceSteps": num_inference_steps,
                "guidanceScale": guidance_scale,
                "seed": seed
            },
            "createdAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }), 201
        
    except Exception as e:
        logger.error(f"Error generating floor plan: {e}", exc_info=True)
        return jsonify({
            "error": "Internal Server Error",
            "message": "Failed to generate floor plan"
        }), 500


@floor_plan_bp.route("/floor-plans/images/<filename>", methods=["GET"])
def get_floor_plan_image(filename):
    """
    Serve a generated floor plan image.
    
    Args:
        filename (str): The filename of the image to serve
        
    Returns:
        The image file
    """
    # Use absolute path to ensure we can find the file
    generated_dir = os.path.abspath(current_app.config["GENERATED_IMAGES_DIR"])
    logger.info(f"Serving image from: {generated_dir}/{filename}")
    return send_from_directory(generated_dir, filename)


@floor_plan_bp.route("/floor-plans", methods=["GET"])
def list_floor_plans():
    """
    List all generated floor plans.
    
    Returns:
        JSON list of floor plans
    """
    # Get the directory where images are stored
    generated_dir = current_app.config["GENERATED_IMAGES_DIR"]
    
    # Find all PNG files
    floor_plans = []
    if os.path.exists(generated_dir):
        for filename in os.listdir(generated_dir):
            if filename.endswith(".png"):
                # Check if there's a metadata file
                base_name = os.path.splitext(filename)[0]
                json_path = os.path.join(generated_dir, f"{base_name}.json")
                
                if os.path.exists(json_path):
                    try:
                        with open(json_path, 'r') as f:
                            metadata = json.load(f)
                            
                            # Add image URL
                            metadata["imageUrl"] = url_for('floor_plan.get_floor_plan_image', 
                                                          filename=filename, 
                                                          _external=True)
                            
                            floor_plans.append(metadata)
                    except Exception as e:
                        logger.error(f"Error loading metadata from {json_path}: {e}")
                else:
                    # Create basic metadata if JSON file doesn't exist
                    floor_plans.append({
                        "id": base_name,
                        "imageUrl": url_for('floor_plan.get_floor_plan_image', 
                                           filename=filename, 
                                           _external=True),
                        "createdAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", 
                                                 time.gmtime(os.path.getmtime(
                                                     os.path.join(generated_dir, filename))))
                    })
    
    # Sort by creation time (newest first)
    floor_plans.sort(key=lambda x: x.get("createdAt", ""), reverse=True)
    
    return jsonify({"floorPlans": floor_plans}), 200


@floor_plan_bp.route("/model-info", methods=["GET"])
def get_model_info():
    """
    Get information about the loaded model.
    
    Returns:
        JSON with model information
    """
    try:
        from app.stable_diffusion.model_loader import _pipeline
        
        # Check if model is loaded
        if _pipeline is None:
            return jsonify({
                "status": "not_loaded",
                "message": "Model has not been loaded yet"
            })
        
        # Get model info
        info = {
            "status": "loaded",
            "device": str(_pipeline.device),
            "model_id": _pipeline._name_or_path,
            "pipeline_type": type(_pipeline).__name__,
        }
        
        # Add memory info if on CUDA
        if torch.cuda.is_available():
            info["memory"] = {
                "allocated_gb": torch.cuda.memory_allocated() / 1e9,
                "reserved_gb": torch.cuda.memory_reserved() / 1e9,
                "max_gb": torch.cuda.get_device_properties(0).total_memory / 1e9
            }
        
        return jsonify(info)
        
    except Exception as e:
        logger.error(f"Error getting model info: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500