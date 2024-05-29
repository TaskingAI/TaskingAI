import logging
from typing import List, Optional, Dict
import os
import yaml
import re
from app.models import Bundle
from app.utils import checksum
from .i18n import set_i18n
from config import CONFIG

logger = logging.getLogger(__name__)

__all__ = [
    "list_bundles",
    "get_bundle",
    "load_bundle_data",
    "get_bundle_cache",
    "get_bundle_checksum",
]

__bundles: List = []
__bundle_dict: Dict = {}
__bundles_cache: List[Dict] = []
__bundle_checksum: str = ""


def collect_i18n_values(yaml_content: str):
    pattern = re.compile(r'i18n:[\w_]+')
    return pattern.findall(yaml_content)


def load_bundle_data() -> List[str]:
    """
    Load bundle data from YAML files.
    :return: a list of bundle ids.
    """

    global __bundles, __bundle_dict, __bundles_cache, __bundle_checksum

    bundles_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../bundles")
    # List all entries in the bundles directory that are directories
    bundle_ids = [i for i in os.listdir(bundles_path) if os.path.isdir(os.path.join(bundles_path, i))]
    pattern = re.compile(r'^[a-z0-9][a-z0-9_]*$')
    bundle_ids = [i for i in bundle_ids if pattern.match(i) and not i.startswith("template")]
    # todo: check bundle_ids in a-z, 0-9, _

    # Iterate through each file in the directory
    for bundle_id in bundle_ids:
        if CONFIG.ALLOWED_BUNDLES and bundle_id not in CONFIG.ALLOWED_BUNDLES:
            continue
        if CONFIG.FORBIDDEN_BUNDLES and bundle_id in CONFIG.FORBIDDEN_BUNDLES:
            continue
        file_path = os.path.join(bundles_path, bundle_id, "resources/bundle_schema.yml")
        logger.info(f"Loading bundle data from bundles/{bundle_id}/resources/bundle_schema.yml")
        i18n_dir_path = os.path.join(bundles_path, bundle_id, "resources/i18n")
        # Check if file is not empty
        if os.path.getsize(file_path) > 0:
            try:

                # Open and read the file
                with open(file_path, "r") as file:
                    bundle_str = file.read()
                with open(file_path, "r") as file:
                    bundle_dict = yaml.safe_load(file)  # Use yaml.safe_load to load YAML data

                # read all the necessary i18n keys
                i18n_keys = collect_i18n_values(bundle_str)
                model_schema_dir = os.path.join(bundles_path, bundle_id, "plugins")
                if os.path.exists(model_schema_dir):
                    for plugin_folder_name in os.listdir(model_schema_dir):
                        # read plugin_folder_name/plugin_schema.yml
                        if (plugin_folder_name.startswith("_") or
                                not os.path.isdir(os.path.join(model_schema_dir, plugin_folder_name))):
                            continue
                        file_path = os.path.join(model_schema_dir, plugin_folder_name, "plugin_schema.yml")
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
                                    raise ValueError(f"{bundle_id}'s i18n key {key[5:]} is missing in {i18n_file}")
                            set_i18n(bundle_id, lang, i18n_data)

                # Process the data
                bundle = Bundle.build(bundle_dict,)
                __bundle_dict[bundle_id] = bundle
                __bundles.append(bundle)

            except yaml.YAMLError as e:
                print(f"Error loading YAML from file {file_path}: {e}")
        else:
            print(f"Skipping empty file: {file_path}")

    __bundles.sort(key=lambda x: x.bundle_id)
    __bundles_cache = [bundle.to_dict(lang=None) for bundle in __bundles]
    __bundle_checksum = checksum(__bundles_cache)
    return [bundle.bundle_id for bundle in __bundles]


def list_bundles() -> List[Bundle]:
    """
    List bundles.
    :return: a list of model schemas.
    """
    # todo: add filter
    return __bundles


def get_bundle(bundle_id: str) -> Optional[Bundle]:
    """
    Get a bundles by bundle_id.

    :param bundle_id: the bundles id.
    :return: the bundles or None if not found.
    """
    return __bundle_dict.get(bundle_id)


def get_bundle_cache() -> List[Dict]:
    """
    Get the bundles cache.
    :return: the bundles cache.
    """
    return __bundles_cache


def get_bundle_checksum() -> str:
    """
    Get the bundle checksum.
    :return: the bundle checksum.
    """
    return __bundle_checksum
