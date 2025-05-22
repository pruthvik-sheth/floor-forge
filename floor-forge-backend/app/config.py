#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Configuration settings for the FloorForge application.
"""

import os
from datetime import timedelta

class BaseConfig:
    """Base configuration with common settings."""
    
    # Security settings
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    
    # API settings
    JSON_SORT_KEYS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload size
    
    # Model settings
    MODEL_BASE_DIR = os.getenv("MODEL_BASE_DIR", "app/models")
    PIPELINE_PATH = os.getenv("PIPELINE_PATH", os.path.join(MODEL_BASE_DIR, "floor_plan_model"))
    BASE_MODEL_ID = "stabilityai/stable-diffusion-2-1-base"  # Fallback model if custom model not found
    
    # Model loading
    EAGER_LOAD_MODEL = os.getenv("EAGER_LOAD_MODEL", "false").lower() == "true"
    
    # Inference settings
    DEFAULT_NUM_INFERENCE_STEPS = int(os.getenv("DEFAULT_NUM_INFERENCE_STEPS", "10"))
    DEFAULT_GUIDANCE_SCALE = float(os.getenv("DEFAULT_GUIDANCE_SCALE", "7.5"))
    DEFAULT_SEED = None  # Random seed by default
    
    # Image settings
    DEFAULT_IMAGE_WIDTH = int(os.getenv("DEFAULT_IMAGE_WIDTH", "512"))
    DEFAULT_IMAGE_HEIGHT = int(os.getenv("DEFAULT_IMAGE_HEIGHT", "512"))
    
    # Cache settings
    CACHE_DIR = os.getenv("CACHE_DIR", "cache")
    CACHE_TIMEOUT = int(os.getenv("CACHE_TIMEOUT", "3600"))  # 1 hour
    
    # Image settings
    GENERATED_IMAGES_DIR = os.getenv("GENERATED_IMAGES_DIR", "static/generated")
    
    # Ensure directories exist
    @classmethod
    def init_app(cls, app):
        """Initialize application with this configuration."""
        for directory in [cls.MODEL_BASE_DIR, cls.CACHE_DIR, cls.GENERATED_IMAGES_DIR]:
            os.makedirs(directory, exist_ok=True)


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    
    DEBUG = True
    TESTING = False
    ENV = "development"
    
    # Shorter inference for faster development
    DEFAULT_NUM_INFERENCE_STEPS = int(os.getenv("DEFAULT_NUM_INFERENCE_STEPS", "10"))
    
    # Override init_app to include development-specific setup
    @classmethod
    def init_app(cls, app):
        BaseConfig.init_app(app)
        
        # Set up logging for development
        import logging
        logging.basicConfig(level=logging.INFO)
        app.logger.setLevel(logging.INFO)


class TestingConfig(BaseConfig):
    """Testing configuration."""
    
    DEBUG = False
    TESTING = True
    ENV = "testing"
    
    # Use minimal settings for tests
    DEFAULT_NUM_INFERENCE_STEPS = 10
    
    # Use temporary directory for test outputs
    GENERATED_IMAGES_DIR = os.getenv("GENERATED_IMAGES_DIR", "static/test-generated")
    
    # Override init_app to include test-specific setup
    @classmethod
    def init_app(cls, app):
        BaseConfig.init_app(app)
        
        # Set up testing-specific configurations
        import tempfile
        if not os.getenv("GENERATED_IMAGES_DIR"):
            temp_dir = tempfile.mkdtemp(prefix="floorforge_test_")
            app.config["GENERATED_IMAGES_DIR"] = temp_dir


class ProductionConfig(BaseConfig):
    """Production configuration."""
    
    DEBUG = False
    TESTING = False
    ENV = "production"
    
    # In production, the secret key must be set by environment variable
    SECRET_KEY = os.getenv("SECRET_KEY")
    
    # Stricter security settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True
    
    # Enforce path settings from environment variables
    MODEL_BASE_DIR = os.getenv("MODEL_BASE_DIR", "/app/models")
    CACHE_DIR = os.getenv("CACHE_DIR", "/app/cache")
    GENERATED_IMAGES_DIR = os.getenv("GENERATED_IMAGES_DIR", "/app/static/generated")
    
    # Override init_app to include production-specific setup
    @classmethod
    def init_app(cls, app):
        BaseConfig.init_app(app)
        
        # Check if SECRET_KEY is set
        if not cls.SECRET_KEY:
            import logging
            logging.error("SECRET_KEY environment variable is not set in production!")
        
        # Set up production logging
        import logging
        from logging.handlers import RotatingFileHandler
        
        # Configure file handler
        log_dir = os.getenv("LOG_DIR", "/app/logs")
        os.makedirs(log_dir, exist_ok=True)
        
        file_handler = RotatingFileHandler(
            os.path.join(log_dir, "floorforge.log"),
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('FloorForge starting up in production mode')