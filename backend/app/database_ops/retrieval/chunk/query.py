from app.database.connection import postgres_pool
import json
from typing import List
from app.models import Collection, Chunk
from .utils import get_ef_search
import logging
import heapq

logger = logging.getLogger(__name__)


async def _query_chunks_in_one_collection(
    collection: Collection,
    top_k: int,
    query_vector: List[float],
):
    """
    Query top_k related chunks in one collection
    :param collection: the collection where the chunks belong to
    :param top_k: the number of chunks to be returned
    :param query_vector: the query vector
    :return: the top_k related chunks
    """

    table_name = Collection.get_chunk_table_name(collection.collection_id)
    ef_search = get_ef_search(
        capacity=collection.capacity, num_chunks=collection.num_chunks, embedding_size=collection.embedding_size
    )

    # we use cosine distance by default
    async with postgres_pool.get_db_connection() as conn:
        async with conn.transaction():
            logger.debug(f"_query_chunks_in_one_collection: Query with ef_search = {ef_search}")

            await conn.execute(
                f"""
                SET LOCAL hnsw.ef_search = {ef_search};
            """
            )

            # by default, use cosine distance
            sql = f"""
                SELECT *, 1 - (embedding <=> $1) AS score
                FROM {table_name}
                ORDER BY embedding <=> $1
                LIMIT $2
            """

            rows = await conn.fetch(sql, json.dumps(query_vector), top_k)

    chunks = [Chunk.build(row) for row in rows]

    return chunks


async def query_chunks(
    collections: List[Collection],
    top_k: int,
    query_vector: List[float],
) -> List[Chunk]:
    """
    Query top_k related chunks in all collections
    :param collections: the collections where the chunks belong to
    :param top_k: the number of chunks to be returned
    :param query_vector: the query vector
    :return: the top_k related chunks
    """

    results = []
    for collection in collections:
        # query chunks in one collection
        chunks = await _query_chunks_in_one_collection(
            collection=collection,
            top_k=top_k,
            query_vector=query_vector,
        )
        results.append(chunks)

    # merge chunks from all collections
    top_k_chunks = []
    for chunk in heapq.merge(*results, key=lambda x: x.score, reverse=True):
        top_k_chunks.append(chunk)
        if len(top_k_chunks) >= top_k:
            break

    return top_k_chunks
