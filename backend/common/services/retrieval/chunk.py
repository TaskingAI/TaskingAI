from typing import List, Optional, Dict
from common.models import Collection, Chunk, SortOrderEnum, ListResult, Model
from common.database_ops.retrieval import chunk as db_chunk
from common.error import ErrorCode, raise_http_error
from common.services.model.model import get_model
from .collection import get_collection
from .record import get_record
from .embedding import embed_query, embed_documents

__all__ = [
    "query_chunks",
    "list_collection_chunks",
    "list_record_chunks",
    "create_chunk",
    "get_chunk",
    "delete_chunk",
]


async def validate_and_get_chunk(collection: Collection, chunk_id: str) -> Chunk:
    chunk = await db_chunk.get_chunk(collection, chunk_id)
    if not chunk:
        raise_http_error(ErrorCode.OBJECT_NOT_FOUND, message=f"Chunk {chunk_id} not found.")
    return chunk


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


async def list_collection_chunks(
    collection_id: str,
    limit: int,
    order: SortOrderEnum,
    after: Optional[str],
    before: Optional[str],
    offset: Optional[int],
    id_search: Optional[str],
) -> ListResult:
    """
    List collection chunks
    :param collection_id: the collection ID
    :param limit: the limit of the query
    :param order: the order of the query, asc or desc
    :param after: the cursor ID to query after
    :param before: the cursor ID to query before
    :param offset: the offset of the query
    :param id_search: the chunk ID to search for
    :return: a list of chunks, total count of chunks, and whether there are more chunks
    """

    collection = await get_collection(collection_id=collection_id)

    after_chunk, before_chunk = None, None

    if after:
        after_chunk = await validate_and_get_chunk(collection=collection, chunk_id=after)

    if before:
        before_chunk = await validate_and_get_chunk(collection=collection, chunk_id=before)

    return await db_chunk.list_get_collection_chunks(
        collection=collection,
        limit=limit,
        order=order,
        after_chunk=after_chunk,
        before_chunk=before_chunk,
        offset=offset,
        prefix_filters={"chunk_id": id_search},
    )


async def list_record_chunks(
    collection_id: str,
    record_id: str,
    limit: int,
    order: SortOrderEnum,
    after: Optional[str],
    before: Optional[str],
    offset: Optional[int],
    id_search: Optional[str],
) -> ListResult:
    """
    List record chunks
    :param collection_id: the collection ID
    :param record_id: the record ID
    :param limit: the limit of the query
    :param order: the order of the query, asc or desc
    :param after: the cursor ID to query after
    :param before: the cursor ID to query before
    :param offset: the offset of the query
    :param id_search: the chunk ID to search for
    :return: a list of chunks, total count of chunks, and whether there are more chunks
    """

    collection = await get_collection(collection_id=collection_id)
    record = await get_record(collection_id=collection_id, record_id=record_id)

    after_chunk, before_chunk = None, None

    if after:
        after_chunk = await validate_and_get_chunk(collection=collection, chunk_id=after)

    if before:
        before_chunk = await validate_and_get_chunk(collection=collection, chunk_id=before)

    return await db_chunk.list_get_record_chunks(
        record=record,
        limit=limit,
        order=order,
        after_chunk=after_chunk,
        before_chunk=before_chunk,
        offset=offset,
        prefix_filters={"chunk_id": id_search},
    )


async def create_chunk(
    collection_id: str,
    content: str,
    metadata: Dict[str, str],
) -> Chunk:
    """
    Create chunk
    :param collection_id: the collection id
    :param record_id: the record id
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

    # create record
    record = await db_chunk.create_chunk(
        collection=collection,
        content=content,
        embedding=embedding,
        metadata=metadata,
    )
    return record


async def get_chunk(
    collection_id: str,
    chunk_id: str,
) -> Chunk:
    """
    Get chunk
    :param collection_id: the collection id
    :param chunk_id: the chunk id
    :return: the chunk
    """

    # Get collection
    collection: Collection = await get_collection(collection_id=collection_id)

    # Get chunk
    chunk = await validate_and_get_chunk(collection=collection, chunk_id=chunk_id)
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

    # Get collection
    collection: Collection = await get_collection(collection_id=collection_id)

    # Get chunk
    chunk = await validate_and_get_chunk(collection=collection, chunk_id=chunk_id)

    # delete chunk
    await db_chunk.delete_chunk(chunk=chunk)
    return
