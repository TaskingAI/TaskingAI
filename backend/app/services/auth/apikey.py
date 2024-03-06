from typing import Dict
from app.models import Apikey
from app.operators import apikey_ops

from tkhelper.error import ErrorCode, raise_http_error

__all__ = [
    "get_apikey",
    "verify_apikey",
]


async def get_apikey(apikey_id: str, plain: bool = False) -> Dict:
    """
    Get apikey
    :param apikey_id: the apikey id
    :param plain: whether to return the plain apikey
    :return: the apikey
    """

    apikey: Apikey = await apikey_ops.get(apikey_id=apikey_id)
    apikey_dict = apikey.to_response_dict()
    if plain:
        apikey_dict["apikey"] = apikey.apikey
    return apikey_dict


async def verify_apikey(apikey: str):
    apikey_id = Apikey.get_apikey_id_from_apikey(apikey)
    apikey_object: Apikey = await apikey_ops.get(apikey_id=apikey_id)
    if apikey_object.apikey != apikey:
        raise_http_error(ErrorCode.TOKEN_VALIDATION_FAILED, message="Invalid apikey")
    return True
