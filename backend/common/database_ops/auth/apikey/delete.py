from common.models import Apikey
from common.database.redis import redis_object_pop


async def delete_apikey(postgres_conn, apikey: Apikey):
    # 1. delete from database
    await postgres_conn.execute("DELETE FROM apikey WHERE apikey_id=$1;", apikey.apikey_id)

    # 2. delete from redis
    await redis_object_pop(Apikey, apikey.apikey_id)
