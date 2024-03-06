from app.database.connection import postgres_pool
from app.models import Chunk, Collection


async def delete_chunk(chunk: Chunk):
    chunk_table_name = Collection.get_chunk_table_name(chunk.collection_id)

    # 1. delete from db
    async with postgres_pool.get_db_connection() as conn:
        await conn.execute(f"DELETE FROM {chunk_table_name} WHERE chunk_id=$1;", chunk.chunk_id)

        # 2. update collection num_chunks
        await conn.execute(
            "UPDATE collection " "SET num_chunks = num_chunks - 1 " "WHERE collection_id=$1;", chunk.collection_id
        )

        if chunk.record_id:
            # 3. update record num_chunks
            await conn.execute(
                "UPDATE record " "SET num_chunks = num_chunks - 1 " "WHERE collection_id=$1 AND record_id=$2;",
                chunk.collection_id,
                chunk.record_id,
            )
