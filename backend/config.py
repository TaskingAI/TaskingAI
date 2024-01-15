import os
from dotenv import load_dotenv
import logging

logger = logging.Logger(__name__)
load_dotenv()

default_env_values = {
    "MODE": "prod",
    "PURPOSE": "api",
    "SERVICE_PORT": 8000,
    "POSTGRES_MAX_CONNECTIONS": 10,
    "AES_ENCRYPTION_KEY": "1234567890123456789012345678901234567890123456789012345678901234",
    "JWT_SECRET_KEY": "1234567890123456789012345678901234567890123456789012345678901234",
    "DEFAULT_ADMIN_USERNAME": "admin",
    "DEFAULT_ADMIN_PASSWORD": "password",
}


def load_str_env(name: str) -> str:
    """
    Load environment variable as string
    :param name: name of the environment variable
    """
    if os.environ.get(name):
        return os.environ.get(name)

    if default_env_values.get(name) is not None:
        return default_env_values.get(name)

    raise Exception(f"Env {name} is not set")


def load_int_env(name: str) -> int:
    """
    Load environment variable as int
    :param name: name of the environment variable
    """
    if os.environ.get(name):
        return int(os.environ.get(name))

    if default_env_values.get(name) is not None:
        return default_env_values.get(name)

    raise Exception(f"Env {name} is not set")


class Config:
    """Backend configuration"""

    def __init__(self):
        logger.info(f"Init Config")

        # version
        self.VERSION = "0.0.1"
        self.POSTGRES_SCHEMA_VERSION = 1

        # mode
        self.MODE = load_str_env("MODE").lower()
        logger.info(f"MODE = {self.MODE}")
        self.DEV = True if self.MODE == "dev" else False
        self.TEST = True if self.MODE == "test" else False
        self.PROD = True if self.MODE == "prod" else False

        # purpose
        self.PURPOSE = load_str_env("PURPOSE").lower()
        logger.info(f"PURPOSE = {self.PURPOSE}")
        self.WEB = True if self.PURPOSE == "web" else False
        self.API = True if self.PURPOSE == "api" else False

        # service
        self.SERVICE_PORT = load_int_env("SERVICE_PORT")
        self.WEB_ROUTE_PREFIX = "/api/v1"
        self.API_ROUTE_PREFIX = "/v1"

        # inference
        self.TASKINGAI_INFERENCE_URL = load_str_env("TASKINGAI_INFERENCE_URL")

        # database
        self.POSTGRES_URL = load_str_env("POSTGRES_URL")
        self.POSTGRES_MAX_CONNECTIONS = load_int_env("POSTGRES_MAX_CONNECTIONS")
        self.REDIS_URL = load_str_env("REDIS_URL")

        # secret
        self.AES_ENCRYPTION_KEY = load_str_env(
            "AES_ENCRYPTION_KEY",
        )
        self.JWT_SECRET_KEY = load_str_env("JWT_SECRET_KEY")
        self.DEFAULT_ADMIN_USERNAME = load_str_env("DEFAULT_ADMIN_USERNAME")
        self.DEFAULT_ADMIN_PASSWORD = load_str_env("DEFAULT_ADMIN_PASSWORD")


CONFIG = Config()
