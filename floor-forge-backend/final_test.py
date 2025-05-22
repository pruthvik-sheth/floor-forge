#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Final test script with memory management.
"""

import os
import gc
import torch
import numpy as np
from diffusers import StableDiffusionPipeline
import time
import uuid
from PIL import Image

def main():
    # Set up paths
    MODEL_DIR = "app/models/floor_plan_model"
    OUTPUT_DIR = "static/generated"
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Force CPU mode
    device = "cpu"
    print(f"Using device: {device}")
    
    try:
        # Force garbage collection
        gc.collect()
        
        # Load the pipeline with minimal settings
        print(f"Loading pipeline from {MODEL_DIR}")
        
        # Check if model exists
        if not os.path.exists(MODEL_DIR):
            print(f"Model not found at {MODEL_DIR}")
            return
            
        # Try to load the model
        try:
            # Load with minimal settings
            pipeline = StableDiffusionPipeline.from_pretrained(
                MODEL_DIR,
                torch_dtype=torch.float32,
                safety_checker=None,
                requires_safety_checker=False,
                low_cpu_mem_usage=True
            )
            
            # Move to CPU
            pipeline = pipeline.to("cpu")
            
            # Enable memory efficient attention
            pipeline.enable_attention_slicing(1)
            
            print("Pipeline loaded successfully!")
            
            # Test generation
            prompt = "A simple floor plan with one bedroom and one bathroom"
            print(f"Generating floor plan for: '{prompt}'")
            
            # Start the timer
            start_time = time.time()
            
            # Generate with minimal settings
            with torch.no_grad():
                # Force garbage collection before generation
                gc.collect()
                
                # Generate with minimal settings
                result = pipeline(
                    prompt=prompt,
                    num_inference_steps=1,  # Absolute minimum steps
                    guidance_scale=1.0,     # Minimal guidance
                    height=128,             # Very small size
                    width=128               # Very small size
                )
                
                # Force garbage collection after generation
                gc.collect()
            
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
            
        except Exception as e:
            print(f"Error loading model: {e}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    main()