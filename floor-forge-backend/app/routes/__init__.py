#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Routes package for the FloorForge API.
"""

# This file marks routes/ as a Python package and can be used to 
# import and initialize all blueprints at once.

from app.routes.floor_plan import floor_plan_bp

# List of all blueprints for easy importing
blueprints = [
    floor_plan_bp,
]

# This function can be used to register all blueprints at once
def register_all_blueprints(app):
    """
    Register all blueprints with the Flask application.
    
    Args:
        app (Flask): The Flask application
    """
    for blueprint in blueprints:
        url_prefix = getattr(blueprint, 'url_prefix', '/api')
        app.register_blueprint(blueprint, url_prefix=url_prefix)