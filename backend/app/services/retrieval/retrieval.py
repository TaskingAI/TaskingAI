from typing import Dict, List, Optional

from fastapi import APIRouter

from app.models import Chunk, Collection, RetrievalRef, RetrievalResult, RetrievalType
from tkhelper.error import ErrorCode, raise_http_error

from .chunk import query_chunks

router = APIRouter()

__all__ = ["verify_retrievals", "query_retrievals", "ui_fetch_retrievals"]


async def verify_retrievals(retrieval_refs: List[RetrievalRef]):
    from app.operators import collection_ops

    embedding_model_id = None
    for retrieval_ref in retrieval_refs:
        if retrieval_ref.type == RetrievalType.COLLECTION:
            collection: Collection = await collection_ops.get(collection_id=retrieval_ref.id)
            if embedding_model_id is None:
                embedding_model_id = collection.embedding_model_id
            elif embedding_model_id != collection.embedding_model_id:
                raise_http_error(
                    error_code=ErrorCode.REQUEST_VALIDATION_ERROR,
                    message="All retrieval collections must have the same embedding model",
                )
        else:
            raise_http_error(
                error_code=ErrorCode.REQUEST_VALIDATION_ERROR,
                message=f"Unsupported retrieval type {retrieval_ref.type}",
            )


async def query_retrievals(
    retrieval_refs: List[RetrievalRef],
    top_k: int,
    max_tokens: Optional[int],
    score_threshold: Optional[float],
    query_text: str,
    rerank_model_id: Optional[str] = None,
) -> List[RetrievalResult]:
    """
    Query the top_k related chunks from the specified collections.
    :param retrieval_refs: a list of retrieval references
    :param top_k: the number of most relevant chunks to be returned.
    :param max_tokens: the maximum number of tokens in the chunks.
    :param score_threshold: the minimum score threshold to return the chunks.
    :param query_text: the query text.
    :return: the list of retrieval results
    """

    collection_ids = []
    for retrieval_ref in retrieval_refs:
        if retrieval_ref.type == RetrievalType.COLLECTION:
            collection_ids.append(retrieval_ref.id)
        else:
            raise_http_error(
                error_code=ErrorCode.REQUEST_VALIDATION_ERROR,
                message=f"Unsupported retrieval type {retrieval_ref.type}",
            )

    chunks: List[Chunk] = await query_chunks(
        collection_ids=collection_ids,
        top_k=top_k,
        max_tokens=max_tokens,
        score_threshold=score_threshold,
        query_text=query_text,
        rerank_model_id=rerank_model_id,
    )

    retrieval_results: List[RetrievalResult] = []
    for chunk in chunks:
        result = RetrievalResult(
            ref={
                "type": "collection",
                "collection_id": chunk.collection_id,
                "chunk_id": chunk.chunk_id,
            },
            content=chunk.content,
        )
        retrieval_results.append(result)

    return retrieval_results


async def ui_fetch_retrievals(retrievals: List[Dict]) -> List[Dict]:
    from app.operators import collection_ops

    for retrieval in retrievals:
        if retrieval["type"] == RetrievalType.COLLECTION:
            collection = await collection_ops.get(collection_id=retrieval["id"])
            if collection:
                retrieval["name"] = collection.name
        else:
            raise ValueError(f"Unsupported retrieval type {retrieval['type']}")
    return retrievals
