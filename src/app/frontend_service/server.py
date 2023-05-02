#!/usr/bin/env python3

"""
This module creates a flask instance and ties it up with blueprints
"""
import os
from app_factory import create_app

app = create_app(app_name="frontend_service")

if __name__ == "__main__":
    app.run(host=os.environ.get("HOST_IP", "localhost"), port=app.config['APP_PORT'])