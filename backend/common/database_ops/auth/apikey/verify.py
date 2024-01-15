from common.models import Apikey
from .get import get_apikey


async def verify_apikey(
    apikey: str,
) -> bool:
    # 1. get from redis
    apikey_id = Apikey.get_apikey_id_from_apikey(apikey)
    apikey_object: Apikey = await get_apikey(apikey_id)
    if apikey_object is None:
        return False

    # 2. write to redis
    # todo: use AES to encrypt the apikey
    if apikey_object.apikey == apikey:
        return True

    return False
