from fastapi import APIRouter
from app.models.base import BaseSuccessEmptyResponse, BaseSuccessDataResponse
from config import CONFIG
import logging

logger = logging.Logger(__name__)

router = APIRouter()


@router.get(
    "/health_check",
    tags=["Manage"],
    operation_id="health_check",
    summary="Health check",
    response_model=BaseSuccessEmptyResponse,
    include_in_schema=False,
)
async def api_health_check():
    return BaseSuccessEmptyResponse()


@router.get(
    "/version",
    tags=["Manage"],
    operation_id="get_version",
    summary="Get version",
    response_model=BaseSuccessDataResponse,
    include_in_schema=False,
)
async def api_version():
    return BaseSuccessDataResponse(
        data={
            "version": CONFIG.VERSION,
        }
    )
