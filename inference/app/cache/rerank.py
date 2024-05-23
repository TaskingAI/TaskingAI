from typing import List
import importlib
import os
import logging

logger = logging.getLogger(__name__)

# Dictionary to store instantiated models
models = {}


def get_provider_model_class(provider_id: str):
    # Generate the model class name based on provider_id
    class_name = "".join(word.title() for word in provider_id.split("_")) + "RerankModel"

    # Import the corresponding module
    module = importlib.import_module(f"providers.{provider_id}.rerank")

    # Return the class from the module
    return getattr(module, class_name)


def get_rerank_model(provider_id: str):
    if provider_id not in models:
        # Get the corresponding model class
        model_class = get_provider_model_class(provider_id)
        # Create an instance of the model
        models[provider_id] = model_class()

    return models[provider_id]


# Automatically search and import all providers
def load_all_rerank_models(provider_ids: List[str]):
    providers_dir = os.path.join(os.path.dirname(__file__), "../../providers")
    for provider_id in provider_ids:
        provider_path = os.path.join(providers_dir, provider_id)
        if os.path.isdir(provider_path) and os.path.exists(os.path.join(provider_path, "rerank.py")):
            try:
                get_rerank_model(provider_id)
                logger.info(f"Loaded rerank models from {provider_id}")
            except Exception as e:
                logger.error(f"load_all_rerank_models: Error loading rerank models from {provider_id}: {e}")
