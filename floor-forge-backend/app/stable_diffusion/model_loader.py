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
    Apply extreme optimizations to the pipeline for better performance with limited memory.
    
    Args:
        pipeline: StableDiffusionPipeline
        device: The device (cuda or cpu)
    """
    # Check environment variables for optimizations
    use_attention_slicing = os.environ.get("USE_ATTENTION_SLICING", "true").lower() == "true"
    use_cpu_offload = os.environ.get("USE_CPU_OFFLOAD", "true").lower() == "true"
    use_float16 = os.environ.get("USE_FLOAT16", "true").lower() == "true"
    
    # Free up memory before applying optimizations
    import gc
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    
    # Apply general optimizations
    if use_attention_slicing:
        # Use maximum slicing for better memory efficiency
        pipeline.enable_attention_slicing(1)
        logger.info("✅ Enabled maximum attention slicing for better memory efficiency")
    
    # Enable model offloading - most aggressive setting
    if hasattr(pipeline, "enable_model_cpu_offload"):
        pipeline.enable_model_cpu_offload()
        logger.info("✅ Enabled model CPU offloading")
    
    # Set up sequential CPU offload for extreme memory savings
    if hasattr(pipeline, "enable_sequential_cpu_offload"):
        pipeline.enable_sequential_cpu_offload()
        logger.info("✅ Enabled sequential CPU offloading")
    
    # GPU-specific optimizations with extreme memory savings
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
                # Try the newer API first
                if hasattr(pipeline, "enable_model_cpu_offload"):
                    pipeline.enable_model_cpu_offload()
                    logger.info("✅ Enabled model CPU offloading to save GPU memory")
                
                # Also enable sequential offloading for maximum memory savings
                if hasattr(pipeline, "enable_sequential_cpu_offload"):
                    pipeline.enable_sequential_cpu_offload()
                    logger.info("✅ Enabled sequential CPU offloading to save GPU memory")
            except Exception as e:
                logger.warning(f"❌ Failed to enable CPU offloading: {e}")
        
        # Enable TF32 for better performance on newer GPUs
        if torch.cuda.is_available() and hasattr(torch.cuda, 'amp') and hasattr(torch.cuda.amp, 'autocast'):
            try:
                torch.backends.cuda.matmul.allow_tf32 = True
                torch.backends.cudnn.allow_tf32 = True
                logger.info("✅ Enabled TF32 for better performance on newer GPUs")
            except Exception as e:
                logger.warning(f"❌ Failed to enable TF32: {e}")
        
        # Set PyTorch memory allocation strategy
        try:
            # Set to reduce fragmentation
            torch.cuda.set_per_process_memory_fraction(0.7)  # Use only 70% of available VRAM
            logger.info("✅ Limited CUDA memory usage to 70% to avoid OOM errors")
            
            # Set environment variables for better memory management
            os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:64"
            logger.info("✅ Set PyTorch CUDA allocation config for better memory management")
        except Exception as e:
            logger.warning(f"❌ Failed to set memory allocation strategy: {e}")
        
        # Log VRAM usage
        try:
            total_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
            reserved_memory = torch.cuda.memory_reserved(0) / 1e9
            allocated_memory = torch.cuda.memory_allocated(0) / 1e9
            logger.info(f"GPU Memory: {allocated_memory:.2f}GB allocated, {reserved_memory:.2f}GB reserved, {total_memory:.2f}GB total")
        except Exception as e:
            logger.warning(f"❌ Failed to log VRAM usage: {e}")
        
        # Try to increase Windows pagefile size programmatically
        try:
            import ctypes
            ctypes.windll.kernel32.SetProcessWorkingSetSize(-1, -1, -1)
            logger.info("✅ Adjusted Windows process working set size")
        except Exception as e:
            logger.warning(f"❌ Failed to adjust Windows process working set size: {e}")
    
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
    
    # Always use CPU to avoid memory issues
    device = "cpu"
    logger.info("✅ Forcing CPU mode to avoid memory issues")
    
    # Always use float32 for CPU
    dtype = torch.float32
    logger.info(f"Using precision: {dtype} for CPU")
    
    # Log that we're using CPU mode
    logger.info(f"Using device: {device} with dtype: {dtype}")
    logger.info("CPU mode will be slower but more reliable")
    
    try:
        # Check if we have a custom pipeline saved
        logger.info(f"Checking for custom pipeline at: {pipeline_path}")
        logger.info(f"Absolute path: {os.path.abspath(pipeline_path) if pipeline_path else 'None'}")
        
        if pipeline_path and os.path.exists(pipeline_path):
            logger.info(f"✅ Custom pipeline found at {pipeline_path}")
            logger.info(f"Directory contents: {os.listdir(pipeline_path)}")
            
            try:
                # Try to load the complete pipeline directly with extreme memory optimizations
                logger.info("Attempting to load fine-tuned model with extreme memory optimizations...")
                
                # Create a temporary offload folder
                import tempfile
                offload_folder = tempfile.mkdtemp()
                logger.info(f"Created temporary offload folder: {offload_folder}")
                
                # Load with maximum memory optimizations
                # Clear CUDA cache before loading
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                
                # Load components separately for better memory management
                logger.info("Loading custom fine-tuned model components...")
                
                # Load text encoder first
                from transformers import CLIPTextModel, CLIPTokenizer
                text_encoder = CLIPTextModel.from_pretrained(
                    f"{pipeline_path}/text_encoder",
                    torch_dtype=dtype,
                    low_cpu_mem_usage=True,
                )
                tokenizer = CLIPTokenizer.from_pretrained(
                    f"{pipeline_path}/tokenizer",
                    torch_dtype=dtype,
                )
                
                # Load UNet
                from diffusers import UNet2DConditionModel
                unet = UNet2DConditionModel.from_pretrained(
                    f"{pipeline_path}/unet",
                    torch_dtype=dtype,
                    low_cpu_mem_usage=True,
                )
                
                # Load VAE
                from diffusers import AutoencoderKL
                vae = AutoencoderKL.from_pretrained(
                    f"{pipeline_path}/vae",
                    torch_dtype=dtype,
                    low_cpu_mem_usage=True,
                )
                
                # Load scheduler
                from diffusers import PNDMScheduler
                scheduler = PNDMScheduler.from_pretrained(
                    f"{pipeline_path}/scheduler",
                )
                
                # Create pipeline from components
                _pipeline = StableDiffusionPipeline(
                    vae=vae,
                    text_encoder=text_encoder,
                    tokenizer=tokenizer,
                    unet=unet,
                    scheduler=scheduler,
                    safety_checker=None,
                    requires_safety_checker=False,
                )
                
                logger.info("✅ Successfully loaded CUSTOM FINE-TUNED model components")
                
                # Free up memory
                import gc
                gc.collect()
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                logger.info("Successfully loaded complete pipeline")
                logger.info(f"Model ID: {_pipeline._name_or_path}")
            except Exception as pipeline_error:
                logger.error(f"Error loading complete pipeline: {pipeline_error}")
                logger.error(f"Error details: {str(pipeline_error)}")
                logger.error(f"Error type: {type(pipeline_error)}")
                import traceback
                logger.error(f"Traceback: {traceback.format_exc()}")
                logger.info("Trying alternative loading approach for custom model...")
                
                # Try to load the custom model with a simpler approach
                try:
                    # Clear memory
                    import gc
                    gc.collect()
                    
                    # Load with simplest approach
                    _pipeline = StableDiffusionPipeline.from_pretrained(
                        pipeline_path,
                        torch_dtype=dtype,
                        safety_checker=None,
                        low_cpu_mem_usage=True
                    )
                    
                    logger.info("✅ Successfully loaded CUSTOM model with alternative approach")
                except Exception as alt_error:
                    logger.error(f"Alternative loading also failed: {alt_error}")
                    logger.warning("Falling back to base model as last resort")
                    
                    # Load base model as final fallback
                    _pipeline = StableDiffusionPipeline.from_pretrained(
                        model_id,
                        torch_dtype=dtype,
                        safety_checker=None,
                        low_cpu_mem_usage=True
                    )
                    
                    logger.warning("USING BASE MODEL, NOT FINE-TUNED MODEL!")
                
                # Free up memory
                gc.collect()
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
            
            logger.error("Custom model path not found, checking for alternative paths...")
            
            # Try to find the model in a different location
            alternative_paths = [
                "app/models/floor_plan_model",
                "../app/models/floor_plan_model",
                "models/floor_plan_model",
                "./models/floor_plan_model"
            ]
            
            found_model = False
            for alt_path in alternative_paths:
                if os.path.exists(alt_path):
                    logger.info(f"Found model at alternative path: {alt_path}")
                    try:
                        # Clear memory
                        import gc
                        gc.collect()
                        
                        # Try to load from alternative path
                        _pipeline = StableDiffusionPipeline.from_pretrained(
                            alt_path,
                            torch_dtype=dtype,
                            safety_checker=None,
                            low_cpu_mem_usage=True
                        )
                        
                        logger.info(f"✅ Successfully loaded CUSTOM model from alternative path: {alt_path}")
                        found_model = True
                        break
                    except Exception as alt_error:
                        logger.error(f"Failed to load from alternative path {alt_path}: {alt_error}")
            
            # If all alternative paths fail, use base model
            if not found_model:
                logger.warning("All attempts to load custom model failed, using base model")
                
                # Load base model as final fallback
                _pipeline = StableDiffusionPipeline.from_pretrained(
                    model_id,
                    torch_dtype=dtype,
                    safety_checker=None,
                    low_cpu_mem_usage=True
                )
                
                logger.warning("USING BASE MODEL, NOT FINE-TUNED MODEL!")
            
            # Free up memory
            gc.collect()
            
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        logger.error(f"Error details: {str(e)}")
        logger.error(f"Error type: {type(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        logger.info("Making one final attempt to load custom model...")
        
        try:
            # Try to find the model in a different location
            alternative_paths = [
                "app/models/floor_plan_model",
                "../app/models/floor_plan_model",
                "models/floor_plan_model",
                "./models/floor_plan_model",
                os.path.abspath("app/models/floor_plan_model")
            ]
            
            found_model = False
            for alt_path in alternative_paths:
                if os.path.exists(alt_path):
                    logger.info(f"Found model at alternative path: {alt_path}")
                    try:
                        # Clear memory
                        import gc
                        gc.collect()
                        
                        # Try to load from alternative path with absolute minimal settings
                        _pipeline = StableDiffusionPipeline.from_pretrained(
                            alt_path,
                            torch_dtype=dtype,
                            safety_checker=None,
                            low_cpu_mem_usage=True
                        )
                        
                        logger.info(f"✅ Successfully loaded CUSTOM model from alternative path: {alt_path}")
                        found_model = True
                        break
                    except Exception as alt_error:
                        logger.error(f"Failed to load from alternative path {alt_path}: {alt_error}")
            
            # If all alternative paths fail, use base model
            if not found_model:
                logger.warning("All attempts to load custom model failed, using base model")
                
                # Load base model as final fallback
                _pipeline = StableDiffusionPipeline.from_pretrained(
                    model_id,
                    torch_dtype=dtype,
                    safety_checker=None,
                    low_cpu_mem_usage=True
                )
                
                logger.warning("USING BASE MODEL, NOT FINE-TUNED MODEL!")
            
            # Free up memory
            gc.collect()
            logger.info("Successfully loaded model as fallback")
        except Exception as fallback_error:
            logger.error(f"Failed to load base model: {fallback_error}")
            logger.error(f"Fallback error details: {str(fallback_error)}")
            logger.error(f"Fallback error type: {type(fallback_error)}")
            logger.error(f"Fallback traceback: {traceback.format_exc()}")
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