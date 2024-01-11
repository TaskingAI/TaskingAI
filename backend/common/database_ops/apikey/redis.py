from common.database.redis import redis_object_get_object, redis_object_set_object, redis_object_pop
from common.models import Apikey
from common.models import SerializePurpose


async def redis_get_apikey(apikey_id: str):
    apikey: Apikey = await redis_object_get_object(Apikey, key=apikey_id)
    return apikey


async def redis_set_apikey(apikey: Apikey):
    await redis_object_set_object(Apikey, key=apikey.apikey_id, value=apikey.to_dict(purpose=SerializePurpose.REDIS))


async def redis_pop_apikey(apikey: Apikey):
    await redis_object_pop(Apikey, key=apikey.apikey_id)
