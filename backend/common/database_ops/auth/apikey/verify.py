from common.models import Apikey
from .get import get_apikey
from common.utils import aes_decrypt


async def verify_apikey(
    input_apikey: str,
) -> bool:
    # 1. get from redis
    apikey_id = Apikey.get_apikey_id_from_apikey(input_apikey)
    apikey_object: Apikey = await get_apikey(apikey_id)
    if apikey_object is None:
        return False

    # 2. write to redis
    decrypted_apikey = aes_decrypt(apikey_object.encrypted_apikey)
    if decrypted_apikey == input_apikey:
        return True

    return False
