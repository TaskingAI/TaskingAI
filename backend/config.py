import os
from dotenv import load_dotenv
import logging

logger = logging.Logger(__name__)
load_dotenv()

default_env_values = {
    "MODE": "PROD",
    "PURPOSE": "API",
    "SERVICE_PORT": 8000,
    "POSTGRES_MAX_CONNECTIONS": 10,
    "AES_ENCRYPTION_KEY": "b90e4648ad699c3bdf62c0860e09eb9efc098ee75f215bf750847ae19d41e4b0",
    "JWT_SECRET_KEY": "dbefe42f34473990a3fa903a6a3283acdc3a910beb1ae271a6463ffa5a926bfb",
    "DEFAULT_ADMIN_USERNAME": "admin",
    "DEFAULT_ADMIN_PASSWORD": "TaskingAI321",
}


def load_str_env(name: str, required: bool = False) -> str:
    """
    Load environment variable as string
    :param name: name of the environment variable
    :param required: whether the environment variable is required
    """
    if os.environ.get(name):
        return os.environ.get(name)

    if default_env_values.get(name) is not None:
        return default_env_values.get(name)

    if required:
        raise Exception(f"Env {name} is not set")


def load_int_env(name: str, required: bool = False) -> int:
    """
    Load environment variable as int
    :param name: name of the environment variable
    :param required: whether the environment variable is required
    """
    if os.environ.get(name):
        return int(os.environ.get(name))

    if default_env_values.get(name) is not None:
        return default_env_values.get(name)

    if required:
        raise Exception(f"Env {name} is not set")


class Config:
    """Backend configuration"""

    def __init__(self):
        logger.info(f"Init Config")

        # version
        self.VERSION = "0.1.3"
        self.POSTGRES_SCHEMA_VERSION = 3

        # mode
        self.MODE = load_str_env("MODE", required=True)
        self.MODE = self.MODE.lower()
        logger.info(f"MODE = {self.MODE}")
        self.DEV = True if self.MODE == "dev" else False
        self.TEST = True if self.MODE == "test" else False
        self.PROD = True if self.MODE == "prod" else False

        # purpose
        self.PURPOSE = load_str_env("PURPOSE", required=True)
        self.PURPOSE = self.PURPOSE.lower()
        logger.info(f"PURPOSE = {self.PURPOSE}")
        self.WEB = True if self.PURPOSE == "web" else False
        self.API = True if self.PURPOSE == "api" else False

        # service
        self.SERVICE_PORT = load_int_env("SERVICE_PORT", required=True)
        self.WEB_ROUTE_PREFIX = "/api/v1"
        self.API_ROUTE_PREFIX = "/v1"

        # inference
        self.TASKINGAI_INFERENCE_URL = load_str_env("TASKINGAI_INFERENCE_URL", required=True)

        # database
        self.POSTGRES_URL = load_str_env("POSTGRES_URL", required=True)
        self.POSTGRES_MAX_CONNECTIONS = load_int_env("POSTGRES_MAX_CONNECTIONS", required=True)
        self.REDIS_URL = load_str_env("REDIS_URL")

        # secret
        self.AES_ENCRYPTION_KEY = load_str_env("AES_ENCRYPTION_KEY", required=True)
        self.JWT_SECRET_KEY = load_str_env("JWT_SECRET_KEY", required=True)
        self.DEFAULT_ADMIN_USERNAME = load_str_env("DEFAULT_ADMIN_USERNAME", required=True)
        self.DEFAULT_ADMIN_PASSWORD = load_str_env("DEFAULT_ADMIN_PASSWORD", required=True)


CONFIG = Config()
