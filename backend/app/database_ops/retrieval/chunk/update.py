from app.database.connection import postgres_pool
from app.models import Chunk, Collection
from typing import Dict, Optional, List
from app.database_ops.utils import update_object


async def update_chunk(
    collection: Collection,
    chunk: Chunk,
    content: Optional[str],
    embedding: Optional[List[float]],
    num_tokens: Optional[int],
    metadata: Optional[Dict],
) -> None:
    # build update dict
    update_dict = {}
    if content is not None and embedding is not None and num_tokens is not None:
        update_dict["content"] = content
        update_dict["embedding"] = embedding
        update_dict["num_tokens"] = num_tokens
    if metadata is not None:
        update_dict["metadata"] = metadata

    chunk_name = Collection.get_chunk_table_name(collection.collection_id)

    # 1. Update chunk in database
    async with postgres_pool.get_db_connection() as conn:
        if len(update_dict) > 0:
            await update_object(
                conn,
                update_dict=update_dict,
                update_time=True,
                table_name=chunk_name,
                equal_filters={"chunk_id": chunk.chunk_id},
            )
