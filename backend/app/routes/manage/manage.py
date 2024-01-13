from fastapi import APIRouter
from app.schemas.base import BaseSuccessEmptyResponse, BaseSuccessDataResponse
from config import CONFIG
from common.services.auth.admin import create_default_admin_if_needed
import logging

logger = logging.Logger(__name__)

router = APIRouter()


# todo: add apikey auth
@router.get(
    "/health_check",
    tags=["manage"],
    operation_id="health_check",
    summary="Health check",
    response_model=BaseSuccessEmptyResponse,
)
async def api_health_check():
    return BaseSuccessEmptyResponse()


@router.get(
    "/version",
    tags=["manage"],
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


if CONFIG.TEST or CONFIG.DEV:
    from common.database.postgres.pool import postgres_db_pool
    from common.database.redis import redis_pool

    @router.post("/clean_data", response_model=BaseSuccessEmptyResponse)
    async def api_clean_data():
        await redis_pool.clean_data()
        await postgres_db_pool.clean_data()

        conn = await postgres_db_pool.db_pool.acquire()
        await create_default_admin_if_needed(postgres_conn=conn)
        await postgres_db_pool.db_pool.release(conn)

        return BaseSuccessEmptyResponse()
