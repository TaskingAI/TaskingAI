from typing import List, Optional

from tkhelper.error import ErrorCode, raise_http_error

from app.models import Collection, Chunk, Model
from app.operators import collection_ops
from app.database_ops.retrieval import chunk as db_chunk
from app.services.model.model import get_model

from .embedding import embed_query

__all__ = [
    "query_chunks",
]


async def query_chunks(
    collection_ids: List[str],
    top_k: int,
    max_tokens: Optional[int],
    score_threshold: Optional[float],
    query_text: str,
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

    # fetch all collections
    collections = []
    for collection_id in collection_ids:
        # currently, raise error when collection is not found
        collection: Collection = await collection_ops.get(collection_id=collection_id)
        collections.append(collection)

    # check all collections have the same embedding model
    embedding_model_ids = set([collection.embedding_model_id for collection in collections])
    if len(embedding_model_ids) > 1:
        raise_http_error(
            ErrorCode.REQUEST_VALIDATION_ERROR, message="The specified collections use different embedding models."
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
    chunks = await db_chunk.query_chunks(
        collections=collections,
        top_k=top_k,
        max_tokens=max_tokens,
        score_threshold=score_threshold,
        query_vector=query_vector,
    )
    return chunks
