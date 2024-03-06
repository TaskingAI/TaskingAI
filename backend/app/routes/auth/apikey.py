from ..utils import auth_info_required
from fastapi import APIRouter, Depends, Request
from typing import Dict
from app.schemas.auth.apikey import *
from app.schemas.base import BaseSuccessDataResponse
from app.services.auth.apikey import *

router = APIRouter()


@router.get(
    "/apikeys/{apikey_id}",
    tags=["API Key"],
    summary="Get API Key",
    operation_id="get_apikey",
    response_model=BaseSuccessDataResponse,
)
async def api_get_apikey(
    apikey_id: str,
    request: Request,
    data: ApikeyGetRequest = Depends(),
    auth_info: Dict = Depends(auth_info_required),
):
    apikey_dict = await get_apikey(
        apikey_id=apikey_id,
        plain=data.plain,
    )
    return BaseSuccessDataResponse(data=apikey_dict)
