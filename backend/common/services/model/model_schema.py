from typing import Optional, List
from common.models import Provider, ModelSchema, ListResult
from config import CONFIG
import aiohttp
from common.utils import ResponseWrapper, check_http_error
import logging

logger = logging.getLogger(__name__)

__all__ = [
    "list_providers",
    "list_model_schemas",
    "get_provider",
    "get_model_schema",
    "load_model_schema_data",
]

_providers, _model_schemas, _provider_dict, _model_schema_dict = [], [], {}, {}


async def load_model_schema_data():
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            f"{CONFIG.TASKINGAI_INFERENCE_URL}/v1/providers",
        )
        response_wrapper = ResponseWrapper(response.status, await response.json())
        check_http_error(response_wrapper)
        providers = [Provider.build(provider_data) for provider_data in response_wrapper.json()["data"]]
        providers.sort(key=lambda x: x.provider_id)

    async with aiohttp.ClientSession() as session:
        response = await session.get(
            f"{CONFIG.TASKINGAI_INFERENCE_URL}/v1/model_schemas",
        )
        response_wrapper = ResponseWrapper(response.status, await response.json())
        check_http_error(response_wrapper)
        model_schemas = [ModelSchema.build(model_schema_data) for model_schema_data in response_wrapper.json()["data"]]
        model_schemas.sort(key=lambda x: x.model_schema_id)

    # sort provider by name
    provider_dict = {provider.provider_id: provider for provider in providers}

    # sort model schemas by provider_id, name
    model_schema_dict = {model_schema.model_schema_id: model_schema for model_schema in model_schemas}

    global _providers, _model_schemas, _provider_dict, _model_schema_dict
    _providers = providers
    _model_schemas = model_schemas
    _provider_dict = provider_dict
    _model_schema_dict = model_schema_dict

    logger.debug(f"load_model_schema_data succeeded!")
    logger.debug(f"_providers: {_providers}")
    logger.debug(f"_model_schemas: {_model_schemas}")


async def list_providers() -> List[Provider]:
    return _providers or []


async def list_model_schemas(
    limit: int,
    offset: Optional[int],
    provider_id: Optional[str],
    type: Optional[str],
) -> ListResult:
    """
    List model schemas.
    Only one in `offset`, `after` and `before` can be used at the same time.

    :param limit: the maximum number of model schemas to return.
    :param offset: the offset of model schemas to return.
    :param provider_id: the provider id to filter by.
    :param type: the model type to filter by.
    :return: a tuple of (model schemas, total count, has more)
    """

    # Filter by provider_id and type
    filtered_schemas = [
        schema
        for schema in _model_schemas
        if (provider_id is None or schema.provider_id == provider_id) and (type is None or schema.type == type)
    ]

    # Paginate
    end_index = offset + limit
    page = filtered_schemas[offset:end_index]

    # Check if there's more
    has_more = end_index < len(filtered_schemas)

    return page, len(filtered_schemas), has_more


def get_provider(provider_id: str) -> Optional[Provider]:
    """
    Get a provider by provider_id.

    :param provider_id: the provider id.
    :return: the provider or None if not found.
    """
    return _provider_dict.get(provider_id)


def get_model_schema(model_schema_id: str) -> Optional[ModelSchema]:
    """
    Get a model schema by model_schema_id.

    :param model_schema_id: the model schema id.
    :return: the model schema or None if not found.
    """
    return _model_schema_dict.get(model_schema_id)
