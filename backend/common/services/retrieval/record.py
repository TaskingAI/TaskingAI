from typing import Optional, Dict
from common.models import Collection, Record, RecordType, SortOrderEnum, TextSplitter, ListResult, Model
from common.database_ops.retrieval import record as db_record
from common.error import ErrorCode, raise_http_error
from .collection import validate_and_get_collection
from common.services.model.model import get_model
from .embedding import embed_documents

__all__ = [
    "list_records",
    "create_record",
    "update_record",
    "get_record",
    "delete_record",
]


async def validate_and_get_record(collection: Collection, record_id: str) -> Record:
    record = await db_record.get_record(collection, record_id)
    if not record:
        raise_http_error(ErrorCode.OBJECT_NOT_FOUND, message=f"Record {record_id} not found.")
    return record


async def list_records(
    collection_id: str,
    limit: int,
    order: SortOrderEnum,
    after: Optional[str],
    before: Optional[str],
    offset: Optional[int],
    id_search: Optional[str],
) -> ListResult:
    """
    List records
    :param collection_id: the collection id
    :param limit: the limit of the query
    :param order: the order of the query, asc or desc
    :param after: the cursor ID to query after
    :param before: the cursor ID to query before
    :param offset: the offset of the query
    :param id_search: the record ID to search for
    :return: a list of records, total count of records, and whether there are more records
    """

    # validate collection
    collection = await validate_and_get_collection(collection_id=collection_id)

    # validate after and before
    after_record, before_record = None, None

    if after:
        after_record = await validate_and_get_record(collection, after)

    if before:
        before_record = await validate_and_get_record(collection, before)

    return await db_record.list_records(
        collection=collection,
        limit=limit,
        order=order,
        after_record=after_record,
        before_record=before_record,
        offset=offset,
        prefix_filters={
            "record_id": id_search,
        },
    )


async def create_record(
    collection_id: str,
    title: str,
    type: RecordType,
    content: str,
    text_splitter: TextSplitter,
    metadata: Dict[str, str],
) -> Record:
    """
    Create record
    :param collection_id: the collection id
    :param title: the record title
    :param type: the record type
    :param content: the record content
    :param text_splitter: the text splitter to split the content into chunks
    :param metadata: the record metadata
    :return: the created record
    """

    # validate collection
    collection: Collection = await validate_and_get_collection(collection_id=collection_id)

    # validate model
    embedding_model: Model = await get_model(collection.embedding_model_id)

    # split content into chunks
    if type == RecordType.TEXT:
        content = content.strip()
        if not content:
            raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, message="Content cannot be empty.")
        documents = text_splitter.split_text(text=content, title=title)
    else:
        raise NotImplementedError(f"Record type {type} is not supported yet.")

    # embed the documents
    embeddings = await embed_documents(
        documents=documents,
        embedding_model=embedding_model,
        embedding_size=collection.embedding_size,
    )

    # create record
    record = await db_record.create_record_and_chunks(
        collection=collection,
        chunk_texts=documents,
        chunk_embeddings=embeddings,
        title=title,
        type=type,
        content=content,
        metadata=metadata,
    )
    return record


async def update_record(
    collection_id: str,
    record_id: str,
    title: Optional[str],
    type: Optional[RecordType],
    content: Optional[str],
    text_splitter: Optional[TextSplitter],
    metadata: Dict[str, str],
) -> Record:
    """
    Update record
    :param collection_id: the collection id
    :param record_id: the record id
    :param title: the record title
    :param type: the record type
    :param content: the record content
    :param text_splitter: the text splitter to split the content into chunks
    :param metadata: the record metadata
    :return: the created record
    """

    collection: Collection = await validate_and_get_collection(collection_id=collection_id)
    record: Record = await validate_and_get_record(collection=collection, record_id=record_id)
    new_type = type if type is not None else record.type
    new_title = title if title is not None else record.title

    documents = None
    embeddings = None
    if content is not None:
        # validate model
        embedding_model: Model = await get_model(collection.embedding_model_id)

        # split content into chunks
        if new_type == RecordType.TEXT:
            content = content.strip()
            if not content:
                raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, message="Content cannot be empty.")
            documents = text_splitter.split_text(text=content, title=new_title)
        else:
            raise NotImplementedError(f"Record type {type} is not supported yet.")

        # embed the documents
        embeddings = await embed_documents(
            documents=documents,
            embedding_model=embedding_model,
            embedding_size=collection.embedding_size,
        )

    # create record
    record = await db_record.update_record(
        collection=collection,
        record=record,
        title=title,
        type=type,
        chunk_texts=documents,
        chunk_embeddings=embeddings,
        metadata=metadata,
    )

    return record


async def get_record(collection_id: str, record_id: str) -> Record:
    """
    Get record
    :param collection_id: the collection id
    :param record_id: the record id
    :return: the record
    """
    collection: Collection = await validate_and_get_collection(collection_id=collection_id)
    record: Record = await validate_and_get_record(collection, record_id)
    return record


async def delete_record(collection_id: str, record_id: str) -> None:
    """
    Delete record
    :param collection_id: the collection id
    :param record_id: the record id
    """
    collection: Collection = await validate_and_get_collection(collection_id=collection_id)
    record: Record = await validate_and_get_record(collection, record_id)
    await db_record.delete_record(collection, record)
