import json
from typing import List
from common.models import Collection
from .utils import get_ef_search
import logging
import heapq

logger = logging.getLogger(__name__)


async def _query_chunks_in_one_collection(
    conn,
    collection: Collection,
    query_vector: List[float],
    top_k: int,
):
    table_name = Collection.get_chunk_table_name(collection.collection_id)
    ef_search = get_ef_search(
        capacity=collection.capacity, num_chunks=collection.num_chunks, embedding_size=collection.embedding_size
    )

    # we use cosine distance by default

    async with conn.transaction():
        # logger.debug(f"searching with ef_search = {ef_search}")

        await conn.execute(
            f"""
            SET LOCAL hnsw.ef_search = {ef_search};
        """
        )

        # by default, use cosine distance
        sql = f"""
            SELECT chunk_id, record_id, content, metadata,
            created_timestamp, updated_timestamp, 1 - (embedding <=> $1) AS score
            FROM {table_name}
            ORDER BY embedding <=> $1
            LIMIT $2
        """

        rows = await conn.fetch(sql, json.dumps(query_vector), top_k)

    chunks = [
        {
            "chunk_id": row["chunk_id"],
            "record_id": row["record_id"],
            "collection_id": collection.collection_id,
            "score": row["score"],
            "text": row["text"],
            "metadata": json.loads(row["metadata"]) if row["metadata"] else None,
        }
        for row in rows
    ]

    return chunks


async def query_chunks(
    conn,
    query_vector: List[float],
    top_k: int,
    collections: List[Collection],
):
    results = []
    for collection in collections:
        # query chunks in one collection
        chunks = await _query_chunks_in_one_collection(
            conn=conn,
            collection=collection,
            query_vector=query_vector,
            top_k=top_k,
        )
        results.append(chunks)

    # merge chunks from all collections
    chunks = heapq.merge(*results, key=lambda x: x["score"], reverse=True)
    top_k_chunks = chunks[:top_k]

    return top_k_chunks
