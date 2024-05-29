import logging
from typing import List, Optional, Dict
import os
import yaml
from app.models import Plugin
import re
from app.utils import checksum

logger = logging.getLogger(__name__)

__all__ = [
    "list_plugins",
    "get_plugin",
    "load_plugin_data",
    "get_plugin_cache",
    "get_plugin_checksum",
]

__plugins: List[Plugin] = []
__bundle_plugin_dict: Dict[str, Dict[str, Plugin]] = {}
__bundle_plugin_list: Dict[str, List[Plugin]] = {}
__plugin_cache: List[Dict] = []
__plugin_schema_checksum: str = ""


def load_plugin_data(bundle_ids: List[str]) -> Dict[str, List[str]]:

    """
    Load plugin data from YAML files.
    :param bundle_ids: a list of bundle ids.
    :return: a dictionary of bundle ids and a list of plugin ids.
    """
    global __plugins, __bundle_plugin_list, __bundle_plugin_dict, __plugin_cache, __plugin_schema_checksum
    bundle_plugin_ids = {}

    bundles_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../bundles")

    # Iterate through each file in the directory
    for bundle_id in bundle_ids:

        plugin_dir_path = os.path.join(bundles_path, bundle_id, "plugins")
        # List all entries in the plugins directory that are directories
        plugin_ids = [i for i in os.listdir(plugin_dir_path) if os.path.isdir(os.path.join(plugin_dir_path, i))]
        pattern = re.compile(r'^[a-z0-9][a-z0-9_]*$')
        plugin_ids = [i for i in plugin_ids if pattern.match(i)]

        __bundle_plugin_list[bundle_id] = []
        __bundle_plugin_dict[bundle_id] = {}
        bundle_plugin_ids[bundle_id] = []

        for plugin_id in plugin_ids:
            file_path = os.path.join(plugin_dir_path, plugin_id, "plugin_schema.yml")

            # Check if file is not empty
            if os.path.getsize(file_path) > 0:
                try:

                    # Open and read the file
                    with open(file_path, "r") as file:
                        plugin_data = yaml.safe_load(file)  # Use yaml.safe_load to load YAML data

                    # Process the data
                    plugin = Plugin.build(bundle_id, plugin_data)
                    __plugins.append(plugin)
                    __bundle_plugin_list[bundle_id].append(plugin)
                    __bundle_plugin_dict[bundle_id][plugin_id] = plugin
                    bundle_plugin_ids[bundle_id].append(plugin_id)
                except yaml.YAMLError as e:
                    print(f"Error loading YAML from file {file_path}: {e}")
            else:
                print(f"Skipping empty file: {file_path}")

        __bundle_plugin_list[bundle_id].sort(key=lambda x: x.plugin_id)
        bundle_plugin_ids[bundle_id].sort()

    __plugin_cache = [plugin.to_dict(lang=None) for plugin in __plugins]
    __plugin_schema_checksum = checksum(__plugin_cache)
    return bundle_plugin_ids


def list_plugins(bundle_id: Optional[str]) -> List[Plugin]:
    """
    List plugins.

    :param bundle_id: the bundle id to filter by.
    :return: a list of plugins.
    """

    # Filter by bundle_id and type
    if bundle_id:
        filtered_schemas = [schema for schema in __bundle_plugin_list.get(bundle_id, [])]
        return filtered_schemas

    return __plugins


def get_plugin(bundle_id, plugin_id: str) -> Optional[Plugin]:
    """
    Get a plugin by plugin_id.

    :param bundle_id: the bundle id.
    :param plugin_id: the plugin id.
    :return: the plugin or None if not found.
    """

    return __bundle_plugin_dict.get(bundle_id, {}).get(plugin_id, None)


def get_plugin_cache() -> List[Dict]:
    """
    Get the plugin cache.
    :return: the plugin cache.
    """
    return __plugin_cache


def get_plugin_checksum() -> str:
    """
    Get the plugin checksum.
    :return: the plugin checksum.
    """
    return __plugin_schema_checksum
