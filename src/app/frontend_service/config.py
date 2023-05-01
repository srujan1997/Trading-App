import os
# import json

SERVICE_NAME = "frontend_service"

DEBUG = False
ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")

APP_PORT = 8081

REDIS = {
    "HOST": os.environ.get("CACHE_URL", ""),
    "PORT": 6379,
    "DB": 0,
    "PASSWORD": os.environ.get("CACHE_PASSWORD", ""),
}