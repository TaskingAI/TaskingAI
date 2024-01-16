from common.database.postgres.pool import postgres_db_pool
from common.models import Collection


async def get_collection(collection_id: str):
    # 1. get from redis
    collection: Collection = await Collection.get_redis(collection_id)
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
        await collection.set_redis()
        return collection

    return None
