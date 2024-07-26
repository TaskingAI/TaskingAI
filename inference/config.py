import os
from dotenv import load_dotenv
import logging
from app.error.error_code import ErrorCode, raise_http_error

logger = logging.Logger(__name__)
load_dotenv()

default_env_values = {
    "MODE": "PROD",
    "LOG_LEVEL": "INFO",
    "SERVICE_PORT": 8000,
    "AES_ENCRYPTION_KEY": "b90e4648ad699c3bdf62c0860e09eb9efc098ee75f215bf750847ae19d41e4b0",
    "DEFAULT_LANG": "en",
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
        raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, f"Env {name} is not set")


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
        raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, f"Env {name} is not set")


class Config:
    """Backend configuration"""

    def __init__(self):
        # version
        self.VERSION = "v0.2.18"

        # mode
        self.MODE = load_str_env("MODE", required=True)
        self.MODE = self.MODE.lower()
        self.DEV = True if self.MODE == "dev" else False
        self.TEST = True if self.MODE == "test" else False
        self.PROD = True if self.MODE == "prod" else False

        # service
        self.SERVICE_PORT = load_int_env("SERVICE_PORT", required=True)
        self.PROXY = load_str_env("PROXY")
        self.API_ROUTE_PREFIX = "/v1"
        self.IMAGE_ROUTE_PREFIX = "/images"

        # allowed_providers
        self.ALLOWED_PROVIDERS = load_str_env("ALLOWED_PROVIDERS", required=False)
        if self.ALLOWED_PROVIDERS:
            self.ALLOWED_PROVIDERS = self.ALLOWED_PROVIDERS.split(",")
            self.ALLOWED_PROVIDERS = [provider.strip() for provider in self.ALLOWED_PROVIDERS]

        # secret
        self.AES_ENCRYPTION_KEY = load_str_env("AES_ENCRYPTION_KEY", required=True)

        # prefix
        self.IMAGE_URL_PREFIX = load_str_env("IMAGE_URL_PREFIX")
        if not self.IMAGE_URL_PREFIX:
            self.IMAGE_URL_PREFIX = f"http://localhost:{self.SERVICE_PORT}"

        # i18b
        self.DEFAULT_LANG = load_str_env("DEFAULT_LANG", required=True)

        # host url black list
        self.PROVIDER_URL_BLACK_LIST = load_str_env("PROVIDER_URL_BLACK_LIST")
        if not self.PROVIDER_URL_BLACK_LIST:
            self.PROVIDER_URL_BLACK_LIST = []
        else:
            self.PROVIDER_URL_BLACK_LIST = self.PROVIDER_URL_BLACK_LIST.split(",")
            self.PROVIDER_URL_BLACK_LIST = [url.strip() for url in self.PROVIDER_URL_BLACK_LIST]

        self.PATH_TO_VOLUME = load_str_env("PATH_TO_VOLUME")


CONFIG = Config()
