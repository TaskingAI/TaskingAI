from typing import Optional, List
from app.models import Provider, ModelSchema, ModelType
from app.config import CONFIG
import aiohttp
from tkhelper.utils import ResponseWrapper, check_http_error
from typing import Tuple
import logging

logger = logging.getLogger(__name__)

__all__ = [
    "list_providers",
    "list_model_schemas",
    "get_provider",
    "get_model_schema",
    "sync_model_schema_data",
    "i18n_text",
]

_providers, _model_schemas, _provider_dict, _model_schema_dict, _i18n_dict = [], [], {}, {}, {}
_provider_checksum, _model_schema_checksum, _i18n_checksum = "", "", ""
PINNED_PROVIDER_IDS = ["openai", "anthropic", "google_gemini", "mistralai"]


# Function to sort providers based on pinning and provider_id
def sort_providers(provider) -> Tuple[int, str]:
    try:
        pinned_index = PINNED_PROVIDER_IDS.index(provider.provider_id)
    except ValueError:
        pinned_index = float("inf")

    return pinned_index, provider.provider_id


async def sync_model_schema_data():
    global _provider_checksum, _model_schema_checksum, _i18n_checksum
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            f"{CONFIG.TASKINGAI_INFERENCE_URL}/v1/cache_checksums",
        )
        response_wrapper = ResponseWrapper(response.status, await response.json())
        check_http_error(response_wrapper)
        response_data = response_wrapper.json()["data"]
        provider_checksum = response_data["provider_checksum"]
        model_schema_checksum = response_data["model_schema_checksum"]
        i18n_checksum = response_data["i18n_checksum"]
        if (
            provider_checksum == _provider_checksum
            and model_schema_checksum == _model_schema_checksum
            and i18n_checksum == _i18n_checksum
        ):
            logger.debug(f"Checksums are the same, no need to sync model schema data.")
            return

    async with aiohttp.ClientSession() as session:
        response = await session.get(
            f"{CONFIG.TASKINGAI_INFERENCE_URL}/v1/caches",
        )
        response_wrapper = ResponseWrapper(response.status, await response.json())
        check_http_error(response_wrapper)
        response_data = response_wrapper.json()["data"]

        model_schemas = [ModelSchema.build(model_schema_data) for model_schema_data in response_data["model_schemas"]]
        model_schemas.sort(key=lambda x: x.model_schema_id)

        providers = []
        for provider_data in response_data["providers"]:
            num_model_schemas = len(
                [
                    model_schema
                    for model_schema in model_schemas
                    if model_schema.provider_id == provider_data["provider_id"]
                ]
            )
            model_types = list(
                set(
                    [
                        model_schema.type
                        for model_schema in model_schemas
                        if model_schema.provider_id == provider_data["provider_id"]
                        and model_schema.type != ModelType.WILDCARD
                    ]
                )
            )
            provider = Provider.build(provider_data, num_model_schemas, model_types)
            providers.append(provider)

        # put pinned providers at the front and sort the rest by provider_id
        providers.sort(key=sort_providers)

        i18n_dict = response_data["i18n"]

    # sort provider by name
    provider_dict = {provider.provider_id: provider for provider in providers}

    # sort model schemas by provider_id, name
    model_schema_dict = {model_schema.model_schema_id: model_schema for model_schema in model_schemas}

    # update data
    global _providers, _model_schemas, _provider_dict, _model_schema_dict, _i18n_dict
    _providers = providers
    _model_schemas = model_schemas
    _provider_dict = provider_dict
    _model_schema_dict = model_schema_dict
    _i18n_dict = i18n_dict

    # update checksum
    _provider_checksum = provider_checksum
    _model_schema_checksum = model_schema_checksum
    _i18n_checksum = i18n_checksum

    logger.debug(f"sync_model_schema_data succeeded!")


def list_providers(
    limit: int,
    offset: Optional[int],
    type: Optional[ModelType],
) -> Tuple[List[Provider], int, bool]:
    """
    List providers.
    :param limit: the maximum number of providers to return.
    :param offset: the offset of providers to return.
    :return: a tuple of (providers, total count, has more)
    """

    # Paginate
    end_index = offset + limit

    # Filter by type
    _filtered_providers = _providers
    if type:
        _filtered_providers = [provider for provider in _providers if provider.has_model_type(type)]

    page = _filtered_providers[offset:end_index]

    # Check if there's more
    has_more = end_index < len(_providers)

    return page, len(_filtered_providers), has_more


async def list_model_schemas(
    limit: int,
    offset: Optional[int],
    provider_id: Optional[str],
    type: Optional[ModelType],
) -> Tuple[List[ModelSchema], int, bool]:
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
        if (provider_id is None or schema.provider_id == provider_id) and (type is None or schema.type == type.value)
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


def i18n_text(
    provider_id: str,
    original: str,
    lang: str,
):
    """
    Translate the original text to the target language using i18n.

    :param provider_id: The provider ID.
    :param original: The original text.
    :param lang: The target language.
    :return: text in the target language.
    """
    global _i18n_dict
    if original.startswith("i18n:"):
        key = original[5:]
        i18n_key = f"{provider_id}:{lang}:{key}"
        return _i18n_dict.get(i18n_key, "") or _i18n_dict.get(f"{provider_id}:{CONFIG.DEFAULT_LANG}:{key}", "")

    return original
