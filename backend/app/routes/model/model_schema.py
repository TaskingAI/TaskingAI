from app.schemas.base import BaseSuccessListResponse

from ..utils import auth_info_required

from fastapi import APIRouter, Depends, Request
from typing import List, Dict
from app.schemas.model.model_schema import ListModelSchemaRequest
from common.services.model.model_schema import list_providers, list_model_schemas
from common.models import SerializePurpose, Provider

router = APIRouter()


@router.get(
    "/providers",
    response_model=BaseSuccessListResponse,
    tags=["Model"],
)
async def api_list_providers(request: Request, auth_info: Dict = Depends(auth_info_required)):
    providers: List[Provider] = await list_providers()
    return BaseSuccessListResponse(
        data=[provider.to_dict(purpose=SerializePurpose.RESPONSE) for provider in providers],
        fetched_count=len(providers),
        total_count=len(providers),
        has_more=False,
    )


@router.get(
    "/model_schemas",
    response_model=BaseSuccessListResponse,
    tags=["Model"],
)
async def api_list_model_schemas(
    request: Request, data: ListModelSchemaRequest = Depends(), auth_info: Dict = Depends(auth_info_required)
):
    model_schemas, total, has_more = await list_model_schemas(
        limit=data.limit,
        after=data.after,
        before=data.before,
        offset=data.offset,
        provider_id=data.provider_id,
        type=data.type,
    )
    return BaseSuccessListResponse(
        data=[model_schema.to_dict(purpose=SerializePurpose.RESPONSE) for model_schema in model_schemas],
        fetched_count=len(model_schemas),
        total_count=total,
        has_more=has_more,
    )
