import logging
from typing import List, Optional, Dict
import os
import yaml
import re
from app.models import Provider
from app.utils import checksum
from app.utils.i18n import set_i18n, collect_i18n_values
from app.error import raise_http_error, ErrorCode
from config import CONFIG

logger = logging.getLogger(__name__)

__all__ = [
    "list_providers",
    "get_provider",
    "load_provider_data",
    "get_provider_cache",
    "get_provider_checksum",
]

__providers: List = []
__provider_dict: Dict = {}
__providers_cache: List[Dict] = []
__provider_checksum: str = ""


def load_provider_data() -> List[str]:
    """
    Load provider data from YAML files.
    :return: a list of provider ids.
    """

    global __providers, __provider_dict, __providers_cache, __provider_checksum

    providers_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../providers")
    # List all entries in the providers directory that are directories
    provider_ids = [i for i in os.listdir(providers_path) if os.path.isdir(os.path.join(providers_path, i))]
    pattern = re.compile(r"^[a-z0-9][a-z0-9_]*$")
    provider_ids = [i for i in provider_ids if pattern.match(i) and not i.startswith("template")]
    # todo: check provider_ids in a-z, 0-9, _

    # Iterate through each file in the directory
    for provider_id in provider_ids:
        if CONFIG.ALLOWED_PROVIDERS and provider_id not in CONFIG.ALLOWED_PROVIDERS:
            continue
        if provider_id == "debug" and CONFIG.PROD:
            continue
        file_path = os.path.join(providers_path, provider_id, "resources/provider.yml")
        logger.info(f"Loading provider data from providers/{provider_id}/resources/provider.yml")
        i18n_dir_path = os.path.join(providers_path, provider_id, "resources/i18n")
        # Check if file is not empty
        if os.path.getsize(file_path) > 0:
            try:

                # Open and read the file
                with open(file_path, "r") as file:
                    provider_str = file.read()
                    provider_dict = yaml.safe_load(provider_str)  # Use yaml.safe_load to load YAML data

                # read all the necessary i18n keys
                i18n_keys = collect_i18n_values(provider_str)
                model_schema_dir = os.path.join(providers_path, provider_id, "resources/models")
                if os.path.exists(model_schema_dir):
                    for file_name in os.listdir(model_schema_dir):
                        if not file_name.endswith(".yml"):
                            continue
                        file_path = os.path.join(model_schema_dir, file_name)
                        if os.path.getsize(file_path) > 0:
                            with open(file_path, "r") as file:
                                model_str = file.read()
                                i18n_keys.extend(collect_i18n_values(model_str))

                # read i18n files: en.yml, zh.yml, fr.yml, etc.
                for i18n_file in os.listdir(i18n_dir_path):
                    if i18n_file.endswith(".yml"):
                        lang = i18n_file.split(".")[0]
                        with open(os.path.join(i18n_dir_path, i18n_file), "r") as file:
                            i18n_data = yaml.safe_load(file)
                            # check if all keys are present
                            for key in i18n_keys:
                                if key[5:] not in i18n_data:
                                    raise_http_error(
                                        ErrorCode.OBJECT_NOT_FOUND,
                                        f"{provider_id}'s i18n key {key[5:]} is missing in {i18n_file}",
                                    )
                            set_i18n(provider_id, lang, i18n_data)

                # Process the data
                provider = Provider.build(
                    provider_dict,
                )
                __provider_dict[provider_id] = provider
                __providers.append(provider)

            except yaml.YAMLError as e:
                logger.error(f"Error loading YAML from file {file_path}: {e}")
        else:
            logger.debug(f"Skipping empty file: {file_path}")

    __providers.sort(key=lambda x: x.provider_id)
    __providers_cache = [provider.to_dict(lang=None) for provider in __providers]
    __provider_checksum = checksum(__providers_cache)
    return provider_ids


def list_providers() -> List[Provider]:
    """
    List model models.
    :return: a list of model schemas.
    """
    # todo: add filter
    return __providers


def get_provider(provider_id: str) -> Optional[Provider]:
    """
    Get a providers by provider_id.

    :param provider_id: the providers id.
    :return: the providers or None if not found.
    """
    return __provider_dict.get(provider_id)


def get_provider_cache() -> List[Dict]:
    """
    Get the providers cache.
    :return: the providers cache.
    """
    return __providers_cache


def get_provider_checksum() -> str:
    """
    Get the provider checksum.
    :return: the provider checksum.
    """
    return __provider_checksum
