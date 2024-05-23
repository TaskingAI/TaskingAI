from fastapi import APIRouter, Depends, Request
from app.models import *
from .schema import *
from app.error import ErrorCode, raise_http_error
from app.cache import *
from app.utils import get_i18n_checksum, get_i18n_cache

router = APIRouter()


@router.get(
    "/providers",
    summary="List providers",
    operation_id="list_providers",
    response_model=ProviderListResponse,
    tags=["Model"],
    responses={422: {"description": "Unprocessable Entity"}},
)
async def api_list_providers(
    request: Request,
    data: ProviderListRequest = Depends(),
):
    providers: List[Provider] = list_providers()
    return ProviderListResponse(
        status="success",
        data=[p.to_dict(data.lang) for p in providers],
    )


@router.get(
    "/providers/get",
    summary="Get provider",
    operation_id="get_providers",
    response_model=BaseSuccessDataResponse,
    tags=["Model"],
    include_in_schema=False,
)
async def api_get_provider(
    request: Request,
    data: ProviderGetRequest = Depends(),
):
    provider = get_provider(data.provider_id)
    if not provider:
        raise_http_error(
            ErrorCode.OBJECT_NOT_FOUND,
            message=f"Provider {data.provider_id} not found.",
        )
    return BaseSuccessDataResponse(
        data=[provider.to_dict(data.lang)],
    )


@router.get(
    "/model_schemas",
    summary="List model schemas",
    operation_id="list_model_schemas",
    response_model=ModelSchemaListResponse,
    tags=["Model"],
    responses={422: {"description": "Unprocessable Entity"}},
)
async def api_list_model_schemas(
    request: Request,
    data: ModelSchemaListRequest = Depends(),
):
    model_schemas = list_model_schemas(
        provider_id=data.provider_id,
        type=data.type,
    )
    return ModelSchemaListResponse(
        data=[m.to_dict(data.lang) for m in model_schemas],
    )


@router.get(
    "/model_schemas/get",
    summary="Get model schema",
    operation_id="get_model_schema",
    response_model=BaseSuccessDataResponse,
    tags=["Model"],
    include_in_schema=False,
)
async def api_get_model_schema(
    request: Request,
    data: ModelSchemaGetRequest = Depends(),
):
    schema = get_model_schema(data.model_schema_id)
    if not schema:
        raise_http_error(
            ErrorCode.OBJECT_NOT_FOUND,
            message=f"Model schema {data.model_schema_id} not found.",
        )
    return BaseSuccessDataResponse(
        data=[schema.to_dict(data.lang)],
    )


@router.get(
    "/caches",
    summary="Get caches schema",
    operation_id="get_model_schema",
    response_model=BaseSuccessDataResponse,
    tags=["Model"],
    include_in_schema=False,
)
async def api_get_caches(
    request: Request,
):
    return BaseSuccessDataResponse(
        data={
            "providers": get_provider_cache(),
            "model_schemas": get_model_schema_cache(),
            "i18n": get_i18n_cache(),
        }
    )


@router.get(
    "/cache_checksums",
    tags=["Manage"],
    operation_id="get_cache_checksums",
    summary="Get Cache Checksums",
    response_model=BaseSuccessDataResponse,
    include_in_schema=False,
)
async def api_get_cache_checksums():
    return BaseSuccessDataResponse(
        data={
            "provider_checksum": get_provider_checksum(),
            "model_schema_checksum": get_model_schema_checksum(),
            "i18n_checksum": get_i18n_checksum(),
        }
    )


@router.get(
    "/model_property_schemas/{model_type}",
    summary="Get model property schema",
    operation_id="get_model_property_schema",
    response_model=BaseSuccessDataResponse,
    tags=["Model"],
    include_in_schema=False,
)
async def api_get_model_schema(
    request: Request,
    model_type: str,
):
    if model_type == "chat_completion":
        from app.routes.chat_completion.schema import ChatCompletionModelProperties

        return BaseSuccessDataResponse(
            data=ChatCompletionModelProperties.properties_schema(),
        )
    elif model_type == "text_embedding":
        from app.routes.text_embedding.schema import TextEmbeddingModelProperties

        return BaseSuccessDataResponse(
            data=TextEmbeddingModelProperties.properties_schema(),
        )
    else:
        raise_http_error(
            ErrorCode.OBJECT_NOT_FOUND,
            message=f"Model type {model_type} not found.",
        )
