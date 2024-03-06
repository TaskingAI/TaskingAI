from typing import Optional, Dict
from tkhelper.error import ErrorCode, raise_http_error

from app.models import Collection, Record, RecordType, TextSplitter, Model
from app.operators import record_ops, collection_ops
from app.services.model.model import get_model
from app.database_ops.retrieval import record as db_record

from .collection import get_collection
from .embedding import embed_documents

__all__ = [
    "create_record",
    "update_record",
    "get_record",
    "delete_record",
]


async def get_record(collection_id: str, record_id: str) -> Record:
    """
    Get record
    :param collection_id: the collection id
    :param record_id: the record id
    :return: the record
    """
    record: Record = await record_ops.get(collection_id=collection_id, record_id=record_id)
    return record


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
    collection: Collection = await get_collection(collection_id=collection_id)

    # validate model
    embedding_model: Model = await get_model(collection.embedding_model_id)

    # split content into chunks
    if type == RecordType.TEXT:
        content = content.strip()
        if not content:
            raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, message="Content cannot be empty.")
        chunk_text_list, num_tokens_list = text_splitter.split_text(text=content, title=title)
    else:
        raise NotImplementedError(f"Record type {type} is not supported yet.")

    # embed the documents
    embeddings = await embed_documents(
        documents=chunk_text_list,
        embedding_model=embedding_model,
        embedding_size=collection.embedding_size,
    )

    # create record
    new_record_id = Record.generate_random_id()
    await db_record.create_record_and_chunks(
        record_id=new_record_id,
        collection=collection,
        chunk_text_list=chunk_text_list,
        chunk_embedding_list=embeddings,
        chunk_num_tokens_list=num_tokens_list,
        title=title,
        type=type,
        content=content,
        metadata=metadata,
    )

    # get the created record
    record = await get_record(collection_id=collection_id, record_id=new_record_id)

    # pop collection redis
    await collection_ops.redis.pop(collection)
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

    collection: Collection = await get_collection(collection_id=collection_id)
    record: Record = await get_record(collection_id=collection_id, record_id=record_id)
    new_type = type if type is not None else record.type
    new_title = title if title is not None else record.title

    chunk_text_list, num_tokens_list, embeddings = None, None, None

    if content is not None:
        # validate model
        embedding_model: Model = await get_model(collection.embedding_model_id)

        # split content into chunks
        if new_type == RecordType.TEXT:
            content = content.strip()
            if not content:
                raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, message="Content cannot be empty.")
            chunk_text_list, num_tokens_list = text_splitter.split_text(text=content, title=new_title)
        else:
            raise NotImplementedError(f"Record type {type} is not supported yet.")

        # embed the documents
        embeddings = await embed_documents(
            documents=chunk_text_list,
            embedding_model=embedding_model,
            embedding_size=collection.embedding_size,
        )

    # update record
    await db_record.update_record(
        collection=collection,
        record=record,
        title=title,
        type=type,
        content=content,
        chunk_text_list=chunk_text_list,
        chunk_num_tokens_list=num_tokens_list,
        chunk_embedding_list=embeddings,
        metadata=metadata,
    )

    # get the updated record
    record = await get_record(collection_id=collection_id, record_id=record_id)
    return record


async def delete_record(collection_id: str, record_id: str) -> None:
    """
    Delete record
    :param collection_id: the collection id
    :param record_id: the record id
    :return: None
    """
    collection: Collection = await get_collection(collection_id=collection_id)
    record: Record = await get_record(collection_id=collection_id, record_id=record_id)
    await db_record.delete_record(record)
    await collection_ops.redis.pop(collection)
