from app.database.connection import postgres_pool
from app.models import Collection
from typing import Dict, List
import json


async def create_chunk(
    chunk_id: str,
    collection: Collection,
    content: str,
    embedding: List[float],
    num_tokens: int,
    metadata: Dict[str, str],
):
    """
    Create chunk
    :param chunk_id: the chunk id
    :param collection: the collection where the chunk belongs to
    :param content: the text content
    :param embedding: the embedding vector
    :param num_tokens: the number of tokens in the chunk
    :param metadata: the chunk metadata
    :return: None
    """

    # generate new chunk id
    chunk_table = Collection.get_chunk_table_name(collection.collection_id)

    async with postgres_pool.get_db_connection() as conn:
        async with conn.transaction():
            # 1. insert chunk

            await conn.execute(
                f"""
                INSERT INTO {chunk_table} (chunk_id, collection_id, content, embedding, metadata, num_tokens)
                VALUES ($1, $2, $3, $4, $5, $6)
            """,
                chunk_id,
                collection.collection_id,
                content,
                json.dumps(embedding),
                json.dumps(metadata),
                num_tokens,
            )

            # 2. update collection stats
            await conn.execute(
                """
                UPDATE collection
                SET num_chunks = num_chunks + 1
                WHERE collection_id = $1
            """,
                collection.collection_id,
            )
