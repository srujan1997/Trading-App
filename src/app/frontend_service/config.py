# Config file for http server

import os

SERVICE_NAME = "frontend_service"

ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")
# DEBUG = False if ENVIRONMENT == "production" else True
DEBUG = True
APP_PORT = 8081

REDIS = {
    "HOST": os.environ.get("CACHE_URL", ""),
    "PORT": 6379,
    "DB": 0,
    "PASSWORD": os.environ.get("CACHE_PASSWORD", ""),
}