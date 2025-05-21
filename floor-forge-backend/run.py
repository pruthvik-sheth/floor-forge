#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Entry point for the FloorForge Flask application.
"""

import os
from app import create_app

# Create application instance using environment variable or default to development
app_config = os.getenv("FLASK_CONFIG", "development")
app = create_app(app_config)

if __name__ == "__main__":
    # Get port from environment variable or use default 5000
    port = int(os.environ.get("PORT", 5000))
    
    # Determine if we should use debug mode with reloader
    use_reloader = os.environ.get("USE_RELOADER", "false").lower() == "true"
    is_debug = app_config == "development"
    
    # Run the application - disable reloader by default when using models
    # to prevent model from being loaded multiple times
    app.run(
        host="0.0.0.0", 
        port=port,
        debug=is_debug,
        use_reloader=use_reloader  # Disable reloader by default
    )