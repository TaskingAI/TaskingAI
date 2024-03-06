from typing import List, Optional, Dict

from tkhelper.error import ErrorCode, raise_http_error
from tkhelper.models import SortOrderEnum, ListResult

from app.models import Collection, Chunk, Model, default_tokenizer
from app.operators import chunk_ops, collection_ops
from app.database_ops.retrieval import chunk as db_chunk
from app.services.model.model import get_model

from .collection import get_collection
from .embedding import embed_query, embed_documents

__all__ = [
    "query_chunks",
    "create_chunk",
    "delete_chunk",
    "update_chunk",
    "list_record_chunks",
]


async def query_chunks(
    collection_ids: List[str],
    top_k: int,
    query_text: str,
) -> List[Chunk]:
    """
    Query the top_k related chunks from the specified collections.
    :param collection_ids: the collection ids.
    :param top_k: the number of chunks to query.
    :param query_text: the query text.
    :return: the created record
    """

    # fetch all collections
    collections = []
    for collection_id in collection_ids:
        # currently, raise error when collection is not found
        collection: Collection = await get_collection(collection_id=collection_id)
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
    record = await db_chunk.query_chunks(
        collections=collections,
        top_k=top_k,
        query_vector=query_vector,
    )
    return record


async def create_chunk(
    collection_id: str,
    content: str,
    metadata: Dict[str, str],
) -> Chunk:
    """
    Create chunk
    :param collection_id: the collection id
    :param content: the chunk content
    :param metadata: the chunk metadata
    :return: the created chunk
    """

    # Get collection
    collection: Collection = await get_collection(collection_id=collection_id)

    # Get model
    embedding_model: Model = await get_model(collection.embedding_model_id)

    # embed the document
    embeddings = await embed_documents(
        documents=[content],
        embedding_model=embedding_model,
        embedding_size=collection.embedding_size,
    )
    embedding = embeddings[0]

    # create chunk
    num_tokens = default_tokenizer.count_tokens(content)
    new_chunk_id = Chunk.generate_random_id()
    await db_chunk.create_chunk(
        chunk_id=new_chunk_id,
        collection=collection,
        content=content,
        embedding=embedding,
        metadata=metadata,
        num_tokens=num_tokens,
    )

    # get the created chunk
    chunk: Chunk = await chunk_ops.get(collection_id=collection_id, chunk_id=new_chunk_id)

    # pop collection redis
    await collection_ops.redis.pop(collection)
    return chunk


async def update_chunk(
    collection_id: str,
    chunk_id: str,
    content: Optional[str],
    metadata: Optional[Dict[str, str]],
) -> Chunk:
    """
    Update chunk
    :param collection_id: the collection id
    :param chunk_id: the chunk id
    :param content: the chunk content
    :param metadata: the chunk metadata
    :return: the created chunk
    """

    collection: Collection = await get_collection(collection_id=collection_id)
    chunk: Chunk = await chunk_ops.get(collection_id=collection_id, chunk_id=chunk_id)

    num_tokens, embedding = None, None

    if content:
        # Get model
        embedding_model: Model = await get_model(collection.embedding_model_id)

        # embed the document
        embeddings = await embed_documents(
            documents=[content],
            embedding_model=embedding_model,
            embedding_size=collection.embedding_size,
        )
        embedding = embeddings[0]

        # update chunk
        num_tokens = default_tokenizer.count_tokens(content)

    # update chunk
    await db_chunk.update_chunk(
        collection=collection,
        chunk=chunk,
        content=content,
        embedding=embedding,
        num_tokens=num_tokens,
        metadata=metadata,
    )

    # get the updated chunk
    chunk: Chunk = await chunk_ops.get(collection_id=collection_id, chunk_id=chunk_id)
    return chunk


async def delete_chunk(
    collection_id: str,
    chunk_id: str,
) -> None:
    """
    Delete chunk
    :param collection_id: the collection id
    :param chunk_id: the chunk id
    :return: None
    """

    collection: Collection = await get_collection(collection_id=collection_id)
    chunk: Chunk = await chunk_ops.get(collection_id=collection_id, chunk_id=chunk_id)
    await db_chunk.delete_chunk(chunk=chunk)
    await collection_ops.redis.pop(collection)


async def list_record_chunks(
    collection_id: str,
    record_id: str,
    limit: int,
    order: SortOrderEnum,
    after_id: Optional[str] = None,
    before_id: Optional[str] = None,
    prefix_filters: Optional[Dict] = None,
) -> ListResult:
    """
    List record chunks
    :param collection_id: the collection id
    :param record_id: the record id
    :param limit: the limit of the query
    :param order: the order of the query, asc or desc
    :param after_id: the cursor ID to query after
    :param before_id: the cursor ID to query before
    :param prefix_filters: the prefix filters
    :return: a tuple of the list of chunks and has_more
    """

    chunks, has_more = await chunk_ops.list(
        collection_id=collection_id,
        limit=limit,
        order=order,
        after_id=after_id,
        before_id=before_id,
        prefix_filters=prefix_filters,
        equal_filters={"record_id": record_id},
    )
    return chunks, has_more
