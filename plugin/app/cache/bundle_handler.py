import importlib
from typing import List, Dict

__all__ = [
    "get_bundle_handler",
    "load_all_bundle_handlers",
]

# Dictionary to store instantiated plugins
__bundle_handlers: Dict[str, Dict] = {}


def __load_bundle_handler_class(bundle_id: str):
    # Generate the model class name based on bundle_id
    class_name = "".join(word.title() for word in bundle_id.split("_"))

    # Import the corresponding module
    module = importlib.import_module(f"bundles.{bundle_id}.bundle")

    # Return the class from the module
    return getattr(module, class_name)


def get_bundle_handler(bundle_id: str):

    """
    Get the bundle handler for the given bundle id and plugin id.
    :param bundle_id: bundle id.
    :return: the plugin.
    """
    if __bundle_handlers.get(bundle_id):
        return __bundle_handlers[bundle_id]

    if bundle_id not in __bundle_handlers:
        __bundle_handlers[bundle_id] = {}

    try:
        # Get the corresponding plugin class
        model_class = __load_bundle_handler_class(bundle_id)
        # Instantiate the model class
        __bundle_handlers[bundle_id] = model_class()
    except (ImportError, AttributeError):
        raise Exception(f"get_bundle_handler: error loading bundle_handler of {bundle_id}")

    return __bundle_handlers[bundle_id]


# Automatically search and import all providers
def load_all_bundle_handlers(bundle_ids: List[str]):

    """
    Load all bundle handlers from the given bundle plugin ids.
    :param bundle_ids: a list of bundle ids.
    :return: None
    """

    for bundle_id in bundle_ids:
        get_bundle_handler(bundle_id)

