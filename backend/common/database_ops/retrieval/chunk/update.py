from common.database.postgres.pool import postgres_db_pool
from common.models import Chunk, Collection
from typing import Dict, Optional, List
from common.database_ops.utils import update_object
from .get import get_chunk


async def update_chunk(
    collection: Collection,
    chunk: Chunk,
    content: Optional[str],
    embedding: Optional[List[float]],
    metadata: Optional[Dict],
):
    # build update dict
    update_dict = {}
    if content is not None and embedding is not None:
        update_dict["content"] = content
        update_dict["embedding"] = embedding
    if metadata is not None:
        update_dict["metadata"] = metadata

    chunk_name = Collection.get_chunk_table_name(collection.collection_id)

    # 1. Update chunk in database
    async with postgres_db_pool.get_db_connection() as conn:
        if len(update_dict) > 0:
            await update_object(
                conn,
                update_dict=update_dict,
                update_time=True,
                table_name=chunk_name,
                equal_filters={"chunk_id": chunk.chunk_id},
            )

    # 2. Get updated chunk
    chunk = await get_chunk(collection, chunk.chunk_id)

    return chunk
