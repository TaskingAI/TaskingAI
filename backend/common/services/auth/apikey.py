from common.models import Apikey, ListResult
from common.database_ops.auth import apikey as db_apikey
from common.error import ErrorCode, raise_http_error

__all__ = [
    "list_apikeys",
    "create_apikey",
    "update_apikey",
    "get_apikey",
    "delete_apikey",
    "verify_apikey",
]


async def validate_and_get_apikey(apikey_id: str) -> Apikey:
    apikey = await db_apikey.get_apikey(apikey_id)
    if not apikey:
        raise_http_error(ErrorCode.OBJECT_NOT_FOUND, message=f"API Key with apikey_id={apikey_id} not found.")
    return apikey


async def list_apikeys() -> ListResult:
    return await db_apikey.list_apikeys()


async def create_apikey(name: str):
    # at most 10 apikeys
    apikey = await db_apikey.create_apikey(name, max_count=10)
    return apikey


async def update_apikey(apikey_id: str, name: str):
    apikey: Apikey = await validate_and_get_apikey(apikey_id)
    apikey = await db_apikey.update_apikey(apikey, {"name": name})
    return apikey


async def get_apikey(apikey_id: str):
    apikey: Apikey = await validate_and_get_apikey(apikey_id)
    return apikey


async def delete_apikey(apikey_id: str):
    apikey: Apikey = await validate_and_get_apikey(apikey_id)
    await db_apikey.delete_apikey(apikey)
    return apikey


async def verify_apikey(apikey: str):
    verify = await db_apikey.verify_apikey(input_apikey=apikey)
    if not verify:
        raise_http_error(ErrorCode.APIKEY_VALIDATION_FAILED, message="Invalid API Key.")
    return True
