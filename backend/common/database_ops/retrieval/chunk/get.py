from common.database.postgres.pool import postgres_db_pool
from common.models import Chunk, Collection
from typing import Optional


async def get_chunk(
    collection: Collection,
    chunk_id: str,
) -> Optional[Chunk]:
    """
    Get chunk
    :param collection: the collection where the chunk belongs to
    :param chunk_id: the chunk id
    :return: the chunk
    """

    chunk_table = Collection.get_chunk_table_name(collection.collection_id)

    # 1. get from db
    async with postgres_db_pool.get_db_connection() as conn:
        row = await conn.fetchrow(f"SELECT * FROM {chunk_table} WHERE chunk_id = $1", chunk_id)

    # 2. return if exists
    if row:
        chunk = Chunk.build(row)
        return chunk

    return None
