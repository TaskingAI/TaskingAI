from fastapi import APIRouter
from app.schemas.base import BaseSuccessEmptyResponse, BaseSuccessDataResponse
from config import CONFIG
from common.services.auth.admin import create_default_admin_if_needed
import logging

logger = logging.Logger(__name__)

router = APIRouter()


@router.get(
    "/health_check",
    tags=["Manage"],
    operation_id="health_check",
    summary="Health check",
    response_model=BaseSuccessEmptyResponse,
)
async def api_health_check():
    return BaseSuccessEmptyResponse()


@router.get(
    "/version",
    tags=["Manage"],
    operation_id="get_version",
    summary="Get application version",
    response_model=BaseSuccessDataResponse,
)
async def api_version():
    return BaseSuccessDataResponse(
        data={
            "version": CONFIG.VERSION,
            "postgres_schema_version": CONFIG.POSTGRES_SCHEMA_VERSION,
        }
    )


if CONFIG.WEB and (CONFIG.TEST or CONFIG.DEV):
    from common.database.redis import redis_pool
    from common.database.postgres import postgres_db_pool

    @router.post(
        "/clean_data",
        tags=["Manage"],
        operation_id="clean_data",
        summary="Clean application version",
        response_model=BaseSuccessEmptyResponse,
    )
    async def api_clean_data():
        await redis_pool.clean_data()
        await postgres_db_pool.clean_data()
        await create_default_admin_if_needed()

        return BaseSuccessEmptyResponse()
