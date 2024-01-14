from common.models import Apikey, SerializePurpose
from common.database.redis import redis_object_get_object, redis_object_set_object


async def get_apikey(postgres_conn, apikey_id: str):
    # 1. get from redis
    apikey: Apikey = await redis_object_get_object(Apikey, key=apikey_id)
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
        await redis_object_set_object(
            Apikey,
            key=apikey_id,
            value=apikey.to_dict(purpose=SerializePurpose.REDIS),
        )
        return apikey

    return None
