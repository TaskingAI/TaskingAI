import heapq
from itertools import islice
from typing import Dict, List, Optional

from app.database_ops.retrieval import chunk as db_chunk
from app.models import Chunk, Collection, Model
from app.services.inference.rerank import rerank
from app.services.model.model import get_model
from tkhelper.error import ErrorCode, raise_http_error

from .embedding import embed_query

__all__ = [
    "query_chunks",
]


async def _get_rerank_result(
    model: Model,
    encrypted_credentials: Dict,
    query: str,
    documents: List[str],
    top_n: int,
):
    """
    get rerank result
    :param model: the model
    :param encrypted_credentials: the encrypted credentials
    :param query: the query string
    :param documents: a list of document strings
    :param top_n: the top n
    :return: the rerank result
    """
    response = await rerank(
        model=model,
        encrypted_credentials=encrypted_credentials,
        query=query,
        documents=documents,
        top_n=top_n,
    )
    data = response.json()["data"]
    return [(d["index"], d["document"]["text"]) for d in data["results"]]


async def _rank_chunks(
    collections: List[Collection],
    top_k: int,
    max_tokens: Optional[int],
    score_threshold: Optional[float],
    query_vector: List[float],
    query_text: str,
    rerank_model_id: Optional[str] = None,
) -> List[Chunk]:
    """
    Rank the top_k related chunks.
    :param collections: the collections where the chunks belong to
    :param top_k: the number of chunks to be returned
    :param max_tokens: the maximum number of tokens to be returned
    :param query_vector: the query vector
    :return: the top_k related chunks
    """
    rerank_flag = bool(collections and rerank_model_id)

    results: List[List[Chunk]] = []
    for collection in collections:
        # query chunks in one collection
        chunks = await db_chunk.query_chunks_in_one_collection(
            collection=collection,
            top_k=top_k * 2 if rerank_flag and len(collections) == 1 else top_k,
            score_threshold=score_threshold,
            query_vector=query_vector,
        )
        results.append(chunks)

    if rerank_flag:
        model: Model = await get_model(model_id=rerank_model_id)

        chunk_list = [chunk for sublist in results for chunk in sublist]
        rerank_result = await _get_rerank_result(
            model=model,
            encrypted_credentials=model.encrypted_credentials,
            query=query_text,
            documents=[chunk.content for chunk in chunk_list],
            top_n=top_k,
        )
        top_k_chunks = [chunk_list[r[0]] for r in rerank_result[: top_k + 1]]
    else:
        # merge chunks from all vectordb_collections
        merged_chunks = heapq.merge(*results, key=lambda x: x.score, reverse=True)
        top_k_chunks = list(islice(merged_chunks, top_k))

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


async def query_chunks(
    collection_ids: List[str],
    top_k: int,
    max_tokens: Optional[int],
    score_threshold: Optional[float],
    query_text: str,
    rerank_model_id: Optional[str] = None,
) -> List[Chunk]:
    """
    Query the top_k related chunks from the specified collections.
    :param collection_ids: the collection ids.
    :param top_k: the number of chunks to query.
    :param max_tokens: the maximum number of tokens in the chunks.
    :param score_threshold: the minimum score threshold to return the chunks.
    :param query_text: the query text.
    :return: the created record
    """
    from app.operators import collection_ops

    # fetch all collections
    collections: List[Collection] = []
    for collection_id in collection_ids:
        # currently, raise error when collection is not found
        collection: Collection = await collection_ops.get(collection_id=collection_id)
        collections.append(collection)

    # check all collections have the same embedding model
    embedding_model_ids = set([collection.embedding_model_id for collection in collections])
    if len(embedding_model_ids) > 1:
        raise_http_error(
            ErrorCode.REQUEST_VALIDATION_ERROR,
            message="The specified collections use different embedding models.",
        )

    # validate model
    embedding_model: Model = await get_model(collections[0].embedding_model_id)

    # compute query vector
    query_vector = await embed_query(
        query=query_text,
        embedding_model=embedding_model,
        embedding_size=collections[0].embedding_size,
    )

    # query related chunks
    chunks = await _rank_chunks(
        collections=collections,
        top_k=top_k,
        max_tokens=max_tokens,
        score_threshold=score_threshold,
        query_vector=query_vector,
        query_text=query_text,
        rerank_model_id=rerank_model_id,
    )
    return chunks
