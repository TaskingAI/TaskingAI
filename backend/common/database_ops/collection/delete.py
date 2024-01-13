from common.models.collection import Collection
from common.database.redis import redis_object_pop


async def delete_collection(postgres_conn, collection: Collection):
    # 1. pop from redis
    await redis_object_pop(Collection, collection.collection_id)

    async with postgres_conn.transaction():
        # 2. delete from collection table
        await postgres_conn.execute("DELETE FROM collection WHERE collection_id=$1;", collection.collection_id)

        # 3. drop the corresponding chunk table
        chunk_table_name = Collection.get_chunk_table_name(collection.collection_id)
        await postgres_conn.execute(f"DROP TABLE IF EXISTS {chunk_table_name};")
