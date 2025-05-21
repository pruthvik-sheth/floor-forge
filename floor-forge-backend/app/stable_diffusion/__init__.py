#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Stable Diffusion integration package for the FloorForge API.
"""

from app.stable_diffusion.model_loader import get_pipeline, unload_pipeline, get_model_info
from app.stable_diffusion.inference import generate_floor_plan  # Remove functions that don't exist

# Export public functions
__all__ = [
    'get_pipeline',
    'unload_pipeline',
    'get_model_info',
    'generate_floor_plan'
]

def init_app(app):
    """
    Initialize the Stable Diffusion models for the application.
    
    Args:
        app (Flask): The Flask application
    """
    # Register a teardown function to unload the model when the app context ends
    @app.teardown_appcontext
    def cleanup_model(exception=None):
        """Unload the model when the app context ends."""
        unload_pipeline()