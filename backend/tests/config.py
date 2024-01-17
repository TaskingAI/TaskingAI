import os
from config import CONFIG

HOST = "http://127.0.0.1"
WEB_SERVICE_PORT = os.environ.get("WEB_SERVICE_PORT", CONFIG.SERVICE_PORT)
API_SERVICE_PORT = os.environ.get("API_SERVICE_PORT", CONFIG.SERVICE_PORT)


