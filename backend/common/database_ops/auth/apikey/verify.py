from common.models import Apikey
from .get import get_apikey


async def verify_apikey(
    conn,
    apikey: str,
) -> bool:
    # 1. get from redis
    apikey_id = Apikey.get_apikey_id_from_apikey(apikey)
    apikey: Apikey = await get_apikey(apikey_id)
    if apikey:
        return False

    # 2. write to redis
    # todo: use AES to encrypt the apikey
    if apikey.apikey == apikey:
        return True

    return False
