import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    BASE_URL = "http://127.0.0.1:8000/v1"
    IMAGE_BASE_URL = "http://127.0.0.1:8000"
    PROVIDER_URL_BLACK_LIST = os.environ.get("PROVIDER_URL_BLACK_LIST").split(",")
    CUSTOM_HOST_API_KEY = os.environ.get("CUSTOM_HOST_API_KEY")
    HELICONE_API_KEY = os.environ.get("HELICONE_API_KEY")
