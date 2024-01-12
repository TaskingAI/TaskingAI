from common.models import Apikey
from .redis import redis_get_apikey, redis_set_apikey


async def get_apikey(postgres_conn, apikey_id: str):
    # 1. get from redis
    apikey: Apikey = await redis_get_apikey(apikey_id)
    if apikey:
        return apikey

    # 2. get from database
    row = await postgres_conn.fetchrow(
        """
        SELECT * FROM apikey WHERE apikey_id = $1
    """,
        apikey_id,
    )

    # 3. write to redis
    if row:
        apikey = Apikey.build(row)
        await redis_set_apikey(apikey=apikey)
        return apikey

    return None
