import os
from dotenv import load_dotenv
import logging

logger = logging.Logger(__name__)
load_dotenv()

default_env_values = {
    "MODE": "PROD",
    "LOG_LEVEL": "INFO",
    "SERVICE_PORT": 8000,
    "AES_ENCRYPTION_KEY": "b90e4648ad699c3bdf62c0860e09eb9efc098ee75f215bf750847ae19d41e4b0",
    "PATH_TO_VOLUME": "/data",
    "DEFAULT_LANG": "en",
    "INCLUDE_FILE_CATEGORY_IN_STORAGE_PATH": 1,
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
        # version
        self.VERSION = "v0.2.13"

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

        # ALLOWED_BUNDLES
        self.ALLOWED_BUNDLES = load_str_env("ALLOWED_BUNDLES", required=False)
        if self.ALLOWED_BUNDLES:
            self.ALLOWED_BUNDLES = self.ALLOWED_BUNDLES.split(",")
            self.ALLOWED_BUNDLES = [provider.strip() for provider in self.ALLOWED_BUNDLES]

        # FORBIDDEN_BUNDLES
        self.FORBIDDEN_BUNDLES = load_str_env("FORBIDDEN_BUNDLES", required=False)
        if self.FORBIDDEN_BUNDLES:
            self.FORBIDDEN_BUNDLES = self.FORBIDDEN_BUNDLES.split(",")
            self.FORBIDDEN_BUNDLES = [provider.strip() for provider in self.FORBIDDEN_BUNDLES]

        # secret
        self.AES_ENCRYPTION_KEY = load_str_env("AES_ENCRYPTION_KEY", required=True)

        # prefix
        self.ICON_URL_PREFIX = load_str_env("ICON_URL_PREFIX")
        if not self.ICON_URL_PREFIX:
            self.ICON_URL_PREFIX = f"http://localhost:{self.SERVICE_PORT}"

        # i18b
        self.DEFAULT_LANG = load_str_env("DEFAULT_LANG", required=True)

        # file storage
        self.OBJECT_STORAGE_TYPE = load_str_env("OBJECT_STORAGE_TYPE", required=True)
        self.PATH_TO_VOLUME = load_str_env("PATH_TO_VOLUME", required=True)
        self.INCLUDE_FILE_CATEGORY_IN_STORAGE_PATH = bool(
            load_int_env("INCLUDE_FILE_CATEGORY_IN_STORAGE_PATH", required=True)
        )

        if self.OBJECT_STORAGE_TYPE == "s3":
            self.S3_ACCESS_KEY_ID = load_str_env("S3_ACCESS_KEY_ID", required=True)
            self.S3_ACCESS_KEY_SECRET = load_str_env("S3_ACCESS_KEY_SECRET", required=True)
            self.S3_ENDPOINT = load_str_env("S3_ENDPOINT", required=True)
            self.S3_BUCKET_PUBLIC_DOMAIN = load_str_env("S3_BUCKET_PUBLIC_DOMAIN")

            self.S3_IMAGE_BUCKET_NAME = load_str_env("S3_IMAGE_BUCKET_NAME")

            if not self.S3_IMAGE_BUCKET_NAME:
                self.S3_IMAGE_BUCKET_NAME = load_str_env("S3_BUCKET_NAME")
            if not self.S3_IMAGE_BUCKET_NAME:
                raise Exception(f"Env S3_IMAGE_BUCKET_NAME is not set")

        elif self.OBJECT_STORAGE_TYPE == "local":
            self.HOST_URL = load_str_env("HOST_URL", required=True)
        else:
            raise Exception("No image storage service specified")


CONFIG = Config()
