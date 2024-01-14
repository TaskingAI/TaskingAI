from common.database.postgres.pool import postgres_db_pool
from common.models import Collection, SerializePurpose
from common.database.redis import redis_object_get_object, redis_object_set_object


async def get_collection(collection_id: str):
    # 1. get from redis
    collection: Collection = await redis_object_get_object(Collection, key=collection_id)
    if collection:
        return collection

    # 2. get from db
    async with postgres_db_pool.get_db_connection() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM collection WHERE collection_id = $1",
            collection_id,
        )

    # 3. write to redis and return
    if row:
        collection = Collection.build(row)
        await redis_object_set_object(
            Collection, key=collection_id, value=collection.to_dict(purpose=SerializePurpose.REDIS)
        )
        return collection

    return None
