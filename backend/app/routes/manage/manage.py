from fastapi import APIRouter
from tkhelper.schemas.base import BaseEmptyResponse, BaseDataResponse
from app.config import CONFIG
from app.services.auth.admin import create_default_admin_if_needed
import logging

logger = logging.Logger(__name__)

router = APIRouter()


@router.get(
    "/health_check",
    tags=["Manage"],
    operation_id="health_check",
    summary="Health check",
    response_model=BaseEmptyResponse,
)
async def api_health_check():
    return BaseEmptyResponse()


@router.get(
    "/version",
    tags=["Manage"],
    operation_id="get_version",
    summary="Get application version",
    response_model=BaseDataResponse,
)
async def api_version():
    return BaseDataResponse(
        data={
            "version": CONFIG.VERSION,
            "postgres_schema_version": CONFIG.POSTGRES_SCHEMA_VERSION,
        }
    )


if CONFIG.WEB and (CONFIG.TEST or CONFIG.DEV):
    from app.database import redis_conn, postgres_pool

    @router.post(
        "/clean_data",
        tags=["Manage"],
        operation_id="clean_data",
        summary="Clean application version",
        response_model=BaseEmptyResponse,
    )
    async def api_clean_data():
        await redis_conn.clean_data()
        await postgres_pool.clean_data()
        await create_default_admin_if_needed()

        return BaseEmptyResponse()
