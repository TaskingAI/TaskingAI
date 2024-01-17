from common.database.postgres.pool import postgres_db_pool
from common.models import Apikey


async def delete_apikey(apikey: Apikey):
    # 1. delete from database
    async with postgres_db_pool.get_db_connection() as conn:
        await conn.execute("DELETE FROM apikey WHERE apikey_id=$1;", apikey.apikey_id)

    # 2. delete from redis
    await apikey.pop_redis()
