#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Flask application factory for FloorForge.
"""

import os
import logging
from flask import Flask, jsonify
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app(config_name):
    """
    Application factory function that creates and configures the Flask app.
    
    Args:
        config_name (str): The configuration to use (development, production, testing)
        
    Returns:
        Flask: The configured Flask application
    """
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    
    # Enable CORS
    CORS(app)
    
    # Load configuration based on environment
    app.config.from_object(f"app.config.{config_name.capitalize()}Config")
    
    # Ensure required directories exist
    for directory in [
        app.config.get("GENERATED_IMAGES_DIR", "static/generated"),
        app.config.get("MODEL_BASE_DIR", "models"),
        app.config.get("CACHE_DIR", "cache")
    ]:
        os.makedirs(directory, exist_ok=True)
    
    # Register global error handlers
    register_error_handlers(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Initialize model if eager loading is enabled
    if app.config.get("EAGER_LOAD_MODEL", False):
        with app.app_context():
            initialize_model()
    
    # Health check endpoint
    @app.route("/health")
    def health_check():
        return jsonify({"status": "healthy", "service": "FloorForge API"})
    
    # Direct static route for images
    @app.route('/api/static/<path:filename>')
    def serve_static(filename):
        return app.send_static_file(filename)
    
    # Print startup message
    logger.info(f"Starting FloorForge API in {config_name} mode")
    
    return app

def initialize_model():
    """Initialize the Stable Diffusion model."""
    try:
        import torch  # Import here to avoid issues if torch is not installed
        
        from app.services.floor_plan_service import load_model
        success = load_model()
        
        if success:
            logger.info("Stable Diffusion model initialized!")
        else:
            logger.warning("Failed to initialize model - will attempt to load on first request")
            
    except Exception as e:
        logger.error(f"Error initializing model: {e}")
        logger.warning("Model will be loaded on first request.")

def register_blueprints(app):
    """
    Register all Flask blueprints.
    
    Args:
        app (Flask): The Flask application
    """
    from app.routes.floor_plan import floor_plan_bp
    
    # Register blueprints
    app.register_blueprint(floor_plan_bp, url_prefix="/api")

def register_error_handlers(app):
    """
    Register error handlers for the application.
    
    Args:
        app (Flask): The Flask application
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not Found", "message": "The requested resource was not found"}), 404
    
    @app.errorhandler(500)
    def server_error(error):
        logger.error(f"Server error: {error}")
        return jsonify({"error": "Internal Server Error", "message": "An unexpected error occurred"}), 500
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Bad Request", "message": str(error)}), 400
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({"error": "Method Not Allowed", "message": "The method is not allowed for the requested URL"}), 405