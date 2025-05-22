#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Standalone script to test model loading and generation.
"""

import os
import torch
from diffusers import StableDiffusionPipeline
import time
import uuid

def main():
    # Set up paths
    MODEL_DIR = "app/models/floor_plan_model"
    OUTPUT_DIR = "static/generated"
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Force CPU mode
    device = "cpu"
    print(f"Using device: {device}")
    
    # Load the pipeline
    print(f"Loading pipeline from {MODEL_DIR}")
    
    # Check if pipeline exists
    if not os.path.exists(MODEL_DIR):
        raise ValueError(f"Model not found at {MODEL_DIR}")
    
    # Load the pipeline
    pipeline = StableDiffusionPipeline.from_pretrained(
        MODEL_DIR,
        torch_dtype=torch.float32,  # Use float32 for CPU
        safety_checker=None
    )
    
    # Move to device
    pipeline = pipeline.to(device)
    
    # Apply basic optimizations
    pipeline.enable_attention_slicing()
    print("Pipeline loaded successfully!")
    
    # Test generation
    prompt = "A simple floor plan with one bedroom and one bathroom"
    print(f"Generating floor plan for: '{prompt}'")
    
    # Start the timer
    start_time = time.time()
    
    # Generate image with reduced size and steps
    result = pipeline(
        prompt=prompt,
        num_inference_steps=5,  # Use minimal steps
        guidance_scale=7.5,
        height=256,  # Reduced size
        width=256    # Reduced size
    )
    
    # Get image from result
    image = result.images[0]
    
    # Save the image
    output_filename = f"floor_plan_{uuid.uuid4()}.png"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    image.save(output_path)
    
    # Calculate generation time
    generation_time = time.time() - start_time
    
    # Log the success
    print(f"Floor plan generated in {generation_time:.2f} seconds")
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    main()