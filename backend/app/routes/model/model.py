from ..utils import auth_info_required
from fastapi import APIRouter, Depends, Request
from common.services.model.model import *
from app.schemas.model.model import *
from app.schemas.base import BaseSuccessEmptyResponse, BaseSuccessDataResponse, BaseSuccessListResponse
from common.models import Model, SerializePurpose

router = APIRouter()


@router.get(
    "/models", tags=["Model"], summary="List Models", operation_id="list_models", response_model=BaseSuccessListResponse
)
async def api_list_models(
    request: Request,
    data: ModelListRequest = Depends(),
    auth_info: Dict = Depends(auth_info_required),
):
    models, total, has_more = await list_models(
        limit=data.limit,
        order=data.order,
        after=data.after,
        before=data.before,
        offset=data.offset,
        id_search=data.id_search,
        name_search=data.name_search,
        provider_id=data.provider_id,
        model_type=data.type,
    )
    return BaseSuccessListResponse(
        data=[model.to_dict(purpose=SerializePurpose.RESPONSE) for model in models],
        fetched_count=len(models),
        total_count=total,
        has_more=has_more,
    )


@router.get(
    "/models/{model_id}",
    tags=["Model"],
    summary="Get Model",
    operation_id="get_model",
    response_model=BaseSuccessDataResponse,
)
async def api_get_model(
    model_id: str,
    request: Request,
    auth_info: Dict = Depends(auth_info_required),
):
    model: Model = await get_model(
        model_id=model_id,
    )
    return BaseSuccessDataResponse(data=model.to_dict(purpose=SerializePurpose.RESPONSE))


@router.post(
    "/models",
    tags=["Model"],
    summary="Create Model",
    operation_id="create_model",
    response_model=BaseSuccessDataResponse,
)
async def api_create_model(
    request: Request,
    data: ModelCreateRequest,
    auth_info: Dict = Depends(auth_info_required),
):
    model: Model = await create_model(
        name=data.name,
        model_schema_id=data.model_schema_id,
        credentials=data.credentials,
        properties=data.properties,
    )
    return BaseSuccessDataResponse(data=model.to_dict(purpose=SerializePurpose.RESPONSE))


@router.post(
    "/models/{model_id}",
    tags=["Model"],
    summary="Update Model",
    operation_id="update_model",
    response_model=BaseSuccessDataResponse,
)
async def api_update_model(
    model_id: str,
    request: Request,
    data: ModelUpdateRequest,
    auth_info: Dict = Depends(auth_info_required),
):
    model: Model = await update_model(
        model_id=model_id,
        name=data.name,
        credentials=data.credentials,
        properties=data.properties,
    )
    return BaseSuccessDataResponse(data=model.to_dict(purpose=SerializePurpose.RESPONSE))


@router.delete(
    "/models/{model_id}",
    tags=["Model"],
    summary="Delete Model",
    operation_id="delete_model",
    response_model=BaseSuccessEmptyResponse,
)
async def api_delete_model(
    model_id: str,
    request: Request,
    auth_info: Dict = Depends(auth_info_required),
):
    await delete_model(
        model_id=model_id,
    )
    return BaseSuccessEmptyResponse()
