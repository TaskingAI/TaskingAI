import importlib
from typing import List, Dict

__all__ = [
    "get_plugin_handler",
    "load_all_plugin_handlers",
]

# Dictionary to store instantiated plugins
__plugin_handlers: Dict[str, Dict] = {}


def __load_plugin_handler_class(bundle_id: str, plugin_schema_id: str):
    # Generate the model class name based on bundle_id
    class_name = "".join(word.title() for word in plugin_schema_id.split("_"))

    # Import the corresponding module
    module = importlib.import_module(f"bundles.{bundle_id}.plugins.{plugin_schema_id}.plugin")

    # Return the class from the module
    return getattr(module, class_name)


def get_plugin_handler(bundle_id: str, plugin_id: str):

    """
    Get the plugin handler for the given bundle id and plugin id.
    :param bundle_id: bundle id.
    :param plugin_id: plugin id.
    :return: the plugin.
    """
    if __plugin_handlers.get(bundle_id, {}).get(plugin_id):
        return __plugin_handlers[bundle_id][plugin_id]

    if bundle_id not in __plugin_handlers:
        __plugin_handlers[bundle_id] = {}

    try:
        # Get the corresponding plugin class
        model_class = __load_plugin_handler_class(bundle_id, plugin_id)
        # Instantiate the model class
        __plugin_handlers[bundle_id][plugin_id] = model_class()
    except (ImportError, AttributeError):
        raise Exception(f"get_plugin_handler: error loading plugin_handler of {bundle_id}/{plugin_id}")

    return __plugin_handlers[bundle_id][plugin_id]


# Automatically search and import all providers
def load_all_plugin_handlers(bundle_plugin_ids: Dict[str, List[str]]):

    """
    Load all plugin handlers from the given bundle plugin ids.
    :param bundle_plugin_ids: a dictionary of bundle ids and a list of plugin ids.
    :return: None
    """

    for bundle_id, plugin_ids in bundle_plugin_ids.items():
        for plugin_id in plugin_ids:
            get_plugin_handler(bundle_id, plugin_id)
