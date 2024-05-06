from app.database.connection import postgres_pool
import json
from typing import List, Optional
from app.models import Collection, Chunk
from .utils import get_ef_search
import logging
import heapq

logger = logging.getLogger(__name__)


async def _query_chunks_in_one_collection(
    collection: Collection,
    top_k: int,
    score_threshold: Optional[float],
    query_vector: List[float],
):
    """
    Query top_k related chunks in one collection
    :param collection: the collection where the chunks belong to
    :param top_k: the number of chunks to be returned
    :param score_threshold: the minimum score threshold to return the chunks
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

            if score_threshold is not None:
                sql = f"""
                    SELECT *, 1 - (embedding <=> $1) AS score
                    FROM {table_name}
                    WHERE 1 - (embedding <=> $1) >= $3
                    ORDER BY score DESC
                    LIMIT $2
                """
                rows = await conn.fetch(sql, json.dumps(query_vector), top_k, score_threshold)
            else:
                # by default, use cosine distance
                sql = f"""
                    SELECT *, 1 - (embedding <=> $1) AS score
                    FROM {table_name}
                    ORDER BY score DESC
                    LIMIT $2
                """
                rows = await conn.fetch(sql, json.dumps(query_vector), top_k)

    chunks = [Chunk.build(row) for row in rows]

    return chunks


async def query_chunks(
    collections: List[Collection],
    top_k: int,
    max_tokens: Optional[int],
    score_threshold: Optional[float],
    query_vector: List[float],
) -> List[Chunk]:
    """
    Query top_k related chunks
    :param collections: the collections where the chunks belong to
    :param top_k: the number of chunks to be returned
    :param max_tokens: the maximum number of tokens in the chunks
    :param score_threshold: the minimum score threshold to return the chunks
    :param query_vector: the query vector
    :return: the top_k related chunks
    """

    results = []
    for collection in collections:
        # query chunks in one collection
        chunks = await _query_chunks_in_one_collection(
            collection=collection,
            top_k=top_k,
            score_threshold=score_threshold,
            query_vector=query_vector,
        )
        results.append(chunks)

    # merge chunks from all collections
    top_k_chunks = []
    for chunk in heapq.merge(*results, key=lambda x: x.score, reverse=True):
        top_k_chunks.append(chunk)
        if len(top_k_chunks) >= top_k:
            break

    # select chunks whose total tokens <= max_tokens
    total_tokens = 0
    if max_tokens is not None:
        result_chunks = []
        for chunk in top_k_chunks:
            if total_tokens + chunk.num_tokens <= max_tokens:
                result_chunks.append(chunk)
                total_tokens += chunk.num_tokens
    else:
        result_chunks = top_k_chunks

    return result_chunks
