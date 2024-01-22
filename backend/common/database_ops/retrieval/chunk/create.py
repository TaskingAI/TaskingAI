from common.database.postgres.pool import postgres_db_pool
from common.models import Collection, Chunk
from .get import get_chunk
from typing import Dict, List
import json


async def create_chunk(
    collection: Collection,
    content: str,
    embedding: List[float],
    num_tokens: int,
    metadata: Dict[str, str],
) -> Chunk:
    """
    Create chunk
    :param collection: the collection where the chunk belongs to
    :param content: the text content
    :param embedding: the embedding vector
    :param metadata: the chunk metadata
    :return: the created chunk
    """

    # generate new chunk id
    new_chunk_id = Chunk.generate_random_id()
    chunk_table = Collection.get_chunk_table_name(collection.collection_id)

    async with postgres_db_pool.get_db_connection() as conn:
        async with conn.transaction():
            # 1. insert chunk

            await conn.execute(
                f"""
                INSERT INTO {chunk_table} (chunk_id, collection_id, content, embedding, metadata, num_tokens)
                VALUES ($1, $2, $3, $4, $5, $6)
            """,
                new_chunk_id,
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

    # 3. get and return
    chunk = await get_chunk(collection, new_chunk_id)

    return chunk
