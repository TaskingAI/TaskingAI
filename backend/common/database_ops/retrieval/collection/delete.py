from common.database.postgres.pool import postgres_db_pool
from common.models import Collection
from common.database.redis import redis_object_pop


async def delete_collection(collection: Collection):
    # 1. pop from redis
    await redis_object_pop(Collection, collection.collection_id)

    async with postgres_db_pool.get_db_connection() as conn:
        async with conn.transaction():
            # 2. delete from collection table
            await conn.execute("DELETE FROM collection WHERE collection_id=$1;", collection.collection_id)

            # 3. drop the corresponding chunk table
            chunk_table_name = Collection.get_chunk_table_name(collection.collection_id)
            await conn.execute(f"DROP TABLE IF EXISTS {chunk_table_name};")
