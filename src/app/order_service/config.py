# Config file for http server

import os

SERVICE_NAME = "order_service"
SERVICE_ID = os.environ.get("ID", "default")

ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")
# DEBUG = False if ENVIRONMENT == "production" else True
DEBUG = True

APP_PORT = os.environ.get("HTTP_PORT", 6298)

REDIS = {
    "HOST": os.environ.get("CACHE_URL", ""),
    "PORT": 6379,
    "DB": 0,
    "PASSWORD": os.environ.get("CACHE_PASSWORD", ""),
}