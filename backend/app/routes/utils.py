from common.error import raise_http_error, ErrorCode
from starlette.requests import Request
from fastapi import HTTPException, Depends
from config import CONFIG
from typing import Dict
from common.services.auth.admin import verify_admin_token
from common.services.auth.apikey import verify_apikey
from common.database.postgres import postgres_db_pool


def check_http_error(response):
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json().get("error", {}))


async def app_admin_auth_info_required(request: Request, postgres_conn) -> Dict:
    ret = {}

    # 1. extract token
    authorization = request.headers.get("Authorization", "")
    if authorization.startswith("Bearer "):
        ret["token"] = authorization[7:]

    if not ret.get("token"):
        raise_http_error(ErrorCode.TOKEN_VALIDATION_FAILED, message="Token is missing")

    # 2. verify token
    admin = await verify_admin_token(postgres_conn=postgres_conn, token=ret["token"])
    ret["admin_id"] = admin.admin_id

    return ret


async def api_auth_info_required(request: Request, postgres_conn) -> Dict:
    apikey = None

    # 1. extract apikey
    authorization = request.headers.get("Authorization", "")
    if authorization.startswith("Bearer "):
        apikey = authorization[7:]

    if not apikey:
        raise_http_error(ErrorCode.APIKEY_VALIDATION_FAILED, message="API Key validation failed")

    # 2. verify apikey
    await verify_apikey(postgres_conn=postgres_conn, apikey=apikey)
    ret = {
        "apikey": apikey,
    }

    return ret


async def auth_info_required(request: Request, postgres_conn=Depends(postgres_db_pool.get_db_connection)) -> Dict:
    if request.url.path.startswith(CONFIG.APP_ROUTE_PREFIX):
        return await app_admin_auth_info_required(request, postgres_conn)

    elif request.url.path.startswith(CONFIG.API_ROUTE_PREFIX):
        return await api_auth_info_required(request, postgres_conn)

    raise NotImplementedError("Unknown auth type")
