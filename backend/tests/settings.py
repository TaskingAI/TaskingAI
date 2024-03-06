import os
from app.config import CONFIG, load_str_env

HOST = "http://127.0.0.1"
WEB_SERVICE_PORT = os.environ.get("WEB_SERVICE_PORT", CONFIG.SERVICE_PORT)
API_SERVICE_PORT = os.environ.get("API_SERVICE_PORT", CONFIG.SERVICE_PORT)
OPENAI_API_KEY = load_str_env("OPENAI_API_KEY", required=True)
