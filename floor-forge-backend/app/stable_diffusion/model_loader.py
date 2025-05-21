#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Model loader for Stable Diffusion models.
"""

import os
import torch
import logging
from diffusers import StableDiffusionPipeline, UNet2DConditionModel

# Configure logging
logger = logging.getLogger(__name__)

# Global variable to store the loaded pipeline
_pipeline = None

def optimize_pipeline(pipeline, device):
    """
    Apply optimizations to the pipeline for better performance.
    
    Args:
        pipeline: StableDiffusionPipeline
        device: The device (cuda or cpu)
    """
    # Check environment variables for optimizations
    use_attention_slicing = os.environ.get("USE_ATTENTION_SLICING", "true").lower() == "true"
    use_cpu_offload = os.environ.get("USE_CPU_OFFLOAD", "true").lower() == "true"
    use_float16 = os.environ.get("USE_FLOAT16", "true").lower() == "true"
    
    # Apply general optimizations
    if use_attention_slicing:
        pipeline.enable_attention_slicing()
        logger.info("✅ Enabled attention slicing for better memory efficiency")
    
    # GPU-specific optimizations
    if device == "cuda":
        # Try to enable xformers for memory efficiency
        if hasattr(pipeline, "enable_xformers_memory_efficient_attention"):
            try:
                pipeline.enable_xformers_memory_efficient_attention()
                logger.info("✅ Enabled xformers memory efficient attention")
            except Exception as e:
                logger.warning(f"❌ Failed to enable xformers: {e}")
        
        # Enable model offloading if low on VRAM
        if use_cpu_offload:
            try:
                pipeline.enable_sequential_cpu_offload()
                logger.info("✅ Enabled sequential CPU offloading to save GPU memory")
            except Exception as e:
                logger.warning(f"❌ Failed to enable sequential CPU offloading: {e}")
        
        # Enable TF32 for better performance on newer GPUs
        if torch.cuda.is_available() and hasattr(torch.cuda, 'amp') and hasattr(torch.cuda.amp, 'autocast'):
            try:
                torch.backends.cuda.matmul.allow_tf32 = True
                torch.backends.cudnn.allow_tf32 = True
                logger.info("✅ Enabled TF32 for better performance on newer GPUs")
            except Exception as e:
                logger.warning(f"❌ Failed to enable TF32: {e}")
        
        # Log VRAM usage
        try:
            total_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
            reserved_memory = torch.cuda.memory_reserved(0) / 1e9
            allocated_memory = torch.cuda.memory_allocated(0) / 1e9
            logger.info(f"GPU Memory: {allocated_memory:.2f}GB allocated, {reserved_memory:.2f}GB reserved, {total_memory:.2f}GB total")
        except Exception as e:
            logger.warning(f"❌ Failed to log VRAM usage: {e}")
    
    return pipeline

def load_pipeline(pipeline_path=None, model_id="stabilityai/stable-diffusion-2-1-base"):
    """
    Load the Stable Diffusion pipeline.
    
    Args:
        pipeline_path (str, optional): Path to a saved pipeline
        model_id (str, optional): HuggingFace model ID to use if local model not found
        
    Returns:
        StableDiffusionPipeline: The loaded pipeline
    """
    global _pipeline
    
    # If pipeline is already loaded, return it
    if _pipeline is not None:
        return _pipeline
    
    # Check environment variable for GPU usage
    use_gpu = os.environ.get("USE_GPU", "true").lower() == "true"
    
    # Set CUDA device if specified
    cuda_device = os.environ.get("CUDA_VISIBLE_DEVICES", "0")
    if cuda_device:
        os.environ["CUDA_VISIBLE_DEVICES"] = cuda_device
        logger.info(f"Set CUDA_VISIBLE_DEVICES to {cuda_device}")
    
    # Determine the device to use
    if use_gpu and torch.cuda.is_available():
        device = "cuda"
        gpu_name = torch.cuda.get_device_name(0)
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
        logger.info(f"✅ Using GPU: {gpu_name} with {gpu_memory:.2f} GB memory")
    else:
        device = "cpu"
        if use_gpu and not torch.cuda.is_available():
            logger.warning("❌ GPU requested but not available! Using CPU which will be much slower.")
        else:
            logger.warning("Using CPU by configuration. This will be much slower than GPU.")
    
    # Check if we should use float16
    use_float16 = os.environ.get("USE_FLOAT16", "true").lower() == "true"
    
    # Set the dtype based on device and settings
    dtype = torch.float16 if device == "cuda" and use_float16 else torch.float32
    logger.info(f"Using precision: {dtype}")
    
    # Log VRAM info for RTX 3050
    if device == "cuda":
        try:
            vram_total = torch.cuda.get_device_properties(0).total_memory / (1024**3)
            logger.info(f"GPU VRAM: {vram_total:.2f} GB total")
            if vram_total < 6:
                logger.info(f"⚠️ Limited VRAM detected ({vram_total:.2f}GB). Using memory optimizations.")
        except Exception as e:
            logger.warning(f"Failed to get VRAM info: {e}")
    logger.info(f"Using device: {device} with dtype: {dtype}")
    
    try:
        # Check if we have a custom pipeline saved
        logger.info(f"Checking for custom pipeline at: {pipeline_path}")
        logger.info(f"Absolute path: {os.path.abspath(pipeline_path) if pipeline_path else 'None'}")
        
        if pipeline_path and os.path.exists(pipeline_path):
            logger.info(f"✅ Custom pipeline found at {pipeline_path}")
            logger.info(f"Directory contents: {os.listdir(pipeline_path)}")
            
            try:
                # Try to load the complete pipeline directly
                logger.info("Attempting to load fine-tuned model...")
                _pipeline = StableDiffusionPipeline.from_pretrained(
                    pipeline_path,
                    torch_dtype=dtype,
                    safety_checker=None,
                    local_files_only=True  # Don't try to download
                )
                logger.info("Successfully loaded complete pipeline")
                logger.info(f"Model ID: {_pipeline._name_or_path}")
            except Exception as pipeline_error:
                logger.error(f"Error loading complete pipeline: {pipeline_error}")
                logger.info(f"Falling back to base model: {model_id}")
                
                # Load base model as fallback
                _pipeline = StableDiffusionPipeline.from_pretrained(
                    model_id,
                    torch_dtype=dtype,
                    safety_checker=None
                )
                logger.warning("USING BASE MODEL, NOT FINE-TUNED MODEL!")
        else:
            # No pipeline path provided or doesn't exist
            logger.error(f"❌ Custom pipeline NOT found at {pipeline_path}")
            if pipeline_path:
                logger.error(f"Current working directory: {os.getcwd()}")
                # Check parent directories
                parent_dir = os.path.dirname(pipeline_path)
                if os.path.exists(parent_dir):
                    logger.info(f"Parent directory exists at: {parent_dir}")
                    logger.info(f"Parent directory contents: {os.listdir(parent_dir)}")
                else:
                    logger.error(f"Parent directory does not exist: {parent_dir}")
            
            logger.error(f"Loading base model: {model_id}")
            _pipeline = StableDiffusionPipeline.from_pretrained(
                model_id,
                torch_dtype=dtype,
                safety_checker=None
            )
            logger.warning("USING BASE MODEL, NOT FINE-TUNED MODEL!")
            
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        logger.info(f"Attempting to load base model as fallback: {model_id}")
        
        try:
            _pipeline = StableDiffusionPipeline.from_pretrained(
                model_id,
                torch_dtype=dtype,
                safety_checker=None
            )
            logger.info("Successfully loaded base model as fallback")
        except Exception as fallback_error:
            logger.error(f"Failed to load base model: {fallback_error}")
            raise RuntimeError("Failed to load any model")
    
    # Move the pipeline to the device
    logger.info(f"Moving pipeline to {device}")
    _pipeline = _pipeline.to(device)
    
    # Apply optimizations
    logger.info("Applying optimizations to pipeline")
    _pipeline = optimize_pipeline(_pipeline, device)
    
    logger.info("Pipeline loaded and ready")
    return _pipeline

def unload_pipeline():
    """
    Unload the pipeline to free up memory.
    """
    global _pipeline
    
    if _pipeline is not None:
        logger.info("Unloading model from memory")
        
        try:
            # Move to CPU first
            _pipeline = _pipeline.to("cpu")
            
            # Delete and clear cache
            del _pipeline
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            
            _pipeline = None
            logger.info("Model unloaded successfully")
        except Exception as e:
            logger.error(f"Error unloading model: {e}")

def get_model_info():
    """
    Get information about the loaded model.
    """
    global _pipeline
    
    if _pipeline is None:
        return {
            "status": "not_loaded",
            "message": "Model has not been loaded yet"
        }
    
    # Get memory usage if on CUDA
    memory_info = {}
    if torch.cuda.is_available():
        memory_info = {
            "allocated_memory_gb": torch.cuda.memory_allocated() / 1e9,
            "reserved_memory_gb": torch.cuda.memory_reserved() / 1e9,
            "max_memory_gb": torch.cuda.get_device_properties(0).total_memory / 1e9
        }
    
    return {
        "status": "loaded",
        "device": str(_pipeline.device),
        "dtype": str(_pipeline.unet.dtype),
        "memory_info": memory_info,
        "pipeline_info": {
            "scheduler_type": _pipeline.scheduler.__class__.__name__,
            "unet_type": _pipeline.unet.__class__.__name__,
            "vae_type": _pipeline.vae.__class__.__name__,
            "text_encoder_type": _pipeline.text_encoder.__class__.__name__
        }
    }

# Public API functions
def get_pipeline(pipeline_path=None, model_id="stabilityai/stable-diffusion-2-1-base"):
    """
    Get the Stable Diffusion pipeline, loading it if necessary.
    
    Args:
        pipeline_path (str, optional): Path to a saved pipeline
        model_id (str, optional): HuggingFace model ID to use if local model not found
        
    Returns:
        StableDiffusionPipeline: The loaded pipeline
    """
    return load_pipeline(pipeline_path, model_id)