from app.database.connection import postgres_pool
from app.models import Collection


async def delete_collection(collection: Collection):
    async with postgres_pool.get_db_connection() as conn:
        async with conn.transaction():
            # 1. delete from collection table
            await conn.execute("DELETE FROM collection WHERE collection_id=$1;", collection.collection_id)

            # 2. drop the corresponding chunk table
            chunk_table_name = Collection.get_chunk_table_name(collection.collection_id)
            await conn.execute(f"DROP TABLE IF EXISTS {chunk_table_name};")
