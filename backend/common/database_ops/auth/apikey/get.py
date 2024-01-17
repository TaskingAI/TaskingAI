from common.database.postgres.pool import postgres_db_pool
from common.models import Apikey


async def get_apikey(apikey_id: str):
    # 1. get from redis
    apikey: Apikey = await Apikey.get_redis(apikey_id)
    if apikey:
        return apikey

    # 2. get from database
    async with postgres_db_pool.get_db_connection() as conn:
        row = await conn.fetchrow(
            """
            SELECT * FROM apikey WHERE apikey_id = $1
        """,
            apikey_id,
        )

    # 3. write to redis
    if row:
        apikey = Apikey.build(row)
        await apikey.set_redis()
        return apikey

    return None
