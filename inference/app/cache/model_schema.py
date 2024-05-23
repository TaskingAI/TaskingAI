import logging
import os
import yaml
from typing import List, Dict
from app.models import ModelSchema
from config import CONFIG
from app.utils import checksum

logger = logging.getLogger(__name__)

_model_schemas, _model_schema_dict, _provider_model_schema_dict = ([], {}, {})
__model_schema_cache: List[Dict] = []
__model_schema_checksum: str = ""

__all__ = [
    "load_model_schema_data",
    "list_model_schemas",
    "get_model_schema",
    "get_model_schema_by_provider",
    "get_model_schema_cache",
    "get_model_schema_checksum",
]


def load_model_schema_data(provider_ids: List[str]) -> None:
    """
    Load model schema data for given provider IDs.
    """

    model_schemas = []

    providers_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../providers")
    for provider_id in provider_ids:
        model_schema_dir = os.path.join(providers_path, provider_id, "resources/models")
        if not os.path.exists(model_schema_dir):
            continue

        model_schema_ids = {}

        for file_name in os.listdir(model_schema_dir):
            if not file_name.endswith(".yml"):
                continue
            file_path = os.path.join(model_schema_dir, file_name)
            if os.path.getsize(file_path) > 0:
                try:
                    with open(file_path, "r") as file:
                        data = yaml.safe_load(file)

                    model_schema_id = data.get("model_schema_id")
                    if model_schema_id in model_schema_ids:
                        raise ValueError(f"Duplicate model_schema_id {model_schema_id} found in provider {provider_id}")
                    model_schema_ids[model_schema_id] = True

                    data["provider_id"] = provider_id
                    model_schema = ModelSchema.build(data)
                    model_schemas.append(model_schema)

                except yaml.YAMLError as e:
                    logger.error(f"Error loading YAML from file {file_path}: {e}")

    model_schemas = [
        model_schema
        for model_schema in model_schemas
        if not CONFIG.ALLOWED_PROVIDERS or model_schema.provider_id in CONFIG.ALLOWED_PROVIDERS
    ]
    model_schemas.sort(key=lambda x: x.model_schema_id)
    model_schema_dict = {model_schema.model_schema_id: model_schema for model_schema in model_schemas}
    provider_model_schema_dict = {
        f"{model_schema.provider_id}:{model_schema.provider_model_id}": model_schema for model_schema in model_schemas
    }

    global _model_schemas, _model_schema_dict, _provider_model_schema_dict, __model_schema_cache, __model_schema_checksum
    _model_schemas, _model_schema_dict, _provider_model_schema_dict = (
        model_schemas,
        model_schema_dict,
        provider_model_schema_dict,
    )
    __model_schema_cache = [model_schema.to_dict(lang=None) for model_schema in model_schemas]
    __model_schema_checksum = checksum(__model_schema_cache)
    logger.info(f"Loaded model schemas for providers: {provider_ids}")


def list_model_schemas(provider_id: str, type: str) -> List[ModelSchema]:
    filtered_schemas = [
        schema
        for schema in _model_schemas
        if (provider_id is None or schema.provider_id == provider_id) and (type is None or schema.type == type)
    ]
    return filtered_schemas


def get_model_schema(model_schema_id: str) -> ModelSchema:
    return _model_schema_dict.get(model_schema_id)


def get_model_schema_by_provider(provider_id: str, provider_model_id: str) -> ModelSchema:
    return _provider_model_schema_dict.get(f"{provider_id}:{provider_model_id}")


def get_model_schema_cache() -> List[Dict]:
    return __model_schema_cache


def get_model_schema_checksum() -> str:
    return __model_schema_checksum
