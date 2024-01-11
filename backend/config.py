import os
from dotenv import load_dotenv
import logging

logger = logging.Logger(__name__)
load_dotenv()


def load_str_env(name: str, default: str = None) -> str:
    """Load environment variable as string"""
    value = os.environ.get(name)
    if not value:
        if default is None:
            raise Exception(f"Env {name} is not set")
        return default
    return value


def load_int_env(name: str, default: int = None) -> int:
    """Load environment variable as int"""
    value = os.environ.get(name)
    if not value:
        if default is None:
            raise Exception(f"Env {name} is not set")
        return default
    return int(value)


def load_bool_env(name: str, default: bool = None) -> bool:
    """Load environment variable as bool"""
    value = os.environ.get(name)
    if not value:
        if default is None:
            raise Exception(f"Env {name} is not set")
        return default
    return value.lower() == "true"


class Config:
    """Backend configuration"""

    def __init__(self):
        logger.info(f"Init Config")

        # version
        self.VERSION = "0.0.1"
        self.POSTGRES_SCHEMA_VERSION = 1
        self.PGVECTOR_SCHEMA_VERSION = 1

        # mode
        self.MODE = load_str_env("MODE").lower()
        logger.info(f"MODE = {self.MODE}")
        self.DEV = True if self.MODE == "dev" else False
        self.TEST = True if self.MODE == "test" else False
        self.PROD = True if self.MODE == "prod" else False

        # service
        self.SERVICE_PORT = load_int_env("SERVICE_PORT", default=8000)
        self.APP_ROUTE_PREFIX = "/api/v1"
        self.API_ROUTE_PREFIX = "/v1"

        # database
        self.POSTGRES_URL = load_str_env("POSTGRES_URL")
        self.POSTGRES_MAX_CONNECTIONS = load_int_env("POSTGRES_MAX_CONNECTIONS", default=10)
        self.REDIS_URL = load_str_env("REDIS_URL")
        self.PGVECTOR_URL = load_str_env("PGVECTOR_URL")
        self.PGVECTOR_MAX_CONNECTIONS = load_int_env("PGVECTOR_MAX_CONNECTIONS", default=10)

        # secret
        self.AES_ENCRYPTION_KEY = load_str_env("AES_ENCRYPTION_KEY")
        self.JWT_SECRET_KEY = load_str_env("JWT_SECRET_KEY")
        self.DEFAULT_USER = load_str_env("DEFAULT_USER")
        self.DEFAULT_PASSWORD = load_str_env("DEFAULT_PASSWORD")


CONFIG = Config()
