from tkhelper.schemas.base import BaseDataResponse, BaseListResponse

from ..utils import auth_info_required

from fastapi import APIRouter, Depends, Request
from typing import Dict
from app.schemas.model.model_schema import *
from tkhelper.error import ErrorCode, raise_http_error
from app.services.model.model_schema import *

router = APIRouter()


@router.get(
    "/providers",
    response_model=BaseListResponse,
    tags=["Model"],
)
async def api_list_providers(
    request: Request,
    data: ProviderListRequest = Depends(),
    auth_info: Dict = Depends(auth_info_required),
):
    providers, total, has_more = list_providers(limit=data.limit, offset=data.offset, type=data.type)
    return BaseListResponse(
        data=[provider.to_dict(lang="en") for provider in providers],
        fetched_count=len(providers),
        total_count=total,
        has_more=has_more,
    )


@router.get(
    "/providers/get",
    response_model=BaseDataResponse,
    tags=["Model"],
)
async def api_get_provider(
    request: Request,
    data: ProviderGetRequest = Depends(),
    auth_info: Dict = Depends(auth_info_required),
):
    provider = get_provider(data.provider_id)
    if not provider:
        raise_http_error(
            ErrorCode.OBJECT_NOT_FOUND,
            message=f"Provider {data.provider_id} not found.",
        )
    return BaseDataResponse(
        data=provider.to_dict(lang="en"),
    )


@router.get(
    "/model_schemas",
    response_model=BaseListResponse,
    tags=["Model"],
)
async def api_list_model_schemas(
    request: Request,
    data: ModelSchemaListRequest = Depends(),
    auth_info: Dict = Depends(auth_info_required),
):
    model_schemas, total, has_more = await list_model_schemas(
        limit=data.limit,
        offset=data.offset,
        provider_id=data.provider_id,
        type=data.type,
    )
    return BaseListResponse(
        data=[model_schema.to_dict(lang="en") for model_schema in model_schemas],
        fetched_count=len(model_schemas),
        total_count=total,
        has_more=has_more,
    )


@router.get(
    "/model_schemas/get",
    response_model=BaseDataResponse,
    tags=["Model"],
)
async def api_get_model_schema(
    request: Request,
    data: ModelSchemaGetRequest = Depends(),
    auth_info: Dict = Depends(auth_info_required),
):
    model_schema = get_model_schema(data.model_schema_id)
    if not model_schema:
        raise_http_error(
            ErrorCode.OBJECT_NOT_FOUND,
            message=f"Model schema {data.model_schema_id} not found.",
        )
    return BaseDataResponse(
        data=model_schema.to_dict(lang="en"),
    )
