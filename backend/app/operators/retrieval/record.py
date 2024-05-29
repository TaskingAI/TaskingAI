from typing import Dict, Optional

from tkhelper.models.operator.postgres_operator import PostgresModelOperator, ModelEntity
from tkhelper.error import raise_http_error, ErrorCode, raise_request_validation_error

from app.database import postgres_pool
from app.models import Record, RecordType, TextSplitter, Collection
from app.database_ops.retrieval import record as db_record
from app.services.retrieval.content_loader import load_db_content, load_content_to_split

from .collection import collection_ops
from ..model import model_ops

__all__ = ["record_ops"]


async def process_content(
    collection: Collection,
    type: RecordType,
    title: str,
    text_splitter: TextSplitter,
    max_num_chunks: int,
    content: Optional[str] = None,
    file_id: Optional[str] = None,
    url: Optional[str] = None,
):
    from app.services.retrieval.embedding import embed_documents

    # split content into chunks
    db_content = await load_db_content(
        record_type=type,
        content=content,
        file_id=file_id,
        url=url,
    )

    content_to_split = await load_content_to_split(
        record_type=type,
        content=content,
        file_id=file_id,
        url=url,
    )

    # embed the documents
    chunk_text_list, num_tokens_list = text_splitter.split_text(text=content_to_split, title=title)
    if len(chunk_text_list) > max_num_chunks:
        raise_http_error(
            ErrorCode.RESOURCE_LIMIT_REACHED,
            "The collection has no enough capacity to store the new chunks created from the record content.",
        )

    # validate model
    embedding_model = await model_ops.get(model_id=collection.embedding_model_id)

    # embed the documents
    embeddings = await embed_documents(
        documents=chunk_text_list,
        embedding_model=embedding_model,
        embedding_size=collection.embedding_size,
    )

    return chunk_text_list, num_tokens_list, embeddings, db_content


class RecordModelOperator(PostgresModelOperator):
    async def create(
        self,
        create_dict: Dict,
        **kwargs,
    ) -> ModelEntity:
        # handle kwargs
        self._check_kwargs(object_id_required=None, **kwargs)
        collection_id = kwargs["collection_id"]

        type = RecordType(create_dict["type"])
        title = create_dict["title"]
        content = create_dict["content"]
        text_splitter = TextSplitter(**create_dict["text_splitter"])
        metadata = create_dict["metadata"]

        # validate collection
        collection = await collection_ops.get(collection_id=collection_id)

        # split content into chunks
        chunk_text_list, num_tokens_list, embeddings, db_content = await process_content(
            collection=collection,
            type=type,
            title=title,
            content=create_dict.get("content"),
            file_id=create_dict.get("file_id"),
            url=create_dict.get("url"),
            text_splitter=text_splitter,
            max_num_chunks=collection.rest_capacity(),
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
            content=db_content,
            metadata=metadata,
        )

        # get the created record
        record = await self.get(collection_id=collection_id, record_id=new_record_id)

        return record

    async def update(
        self,
        update_dict: Dict,
        **kwargs,
    ) -> ModelEntity:
        # handle kwargs
        self._check_kwargs(object_id_required=None, **kwargs)
        collection_id = kwargs["collection_id"]
        record_id = kwargs["record_id"]
        new_metadata = update_dict.get("metadata")

        collection = await collection_ops.get(collection_id=collection_id)
        record: Record = await self.get(collection_id=collection_id, record_id=record_id)

        if record.type == RecordType.FILE:
            raise_request_validation_error("Cannot update a file record. Please delete and create a new record.")

        chunk_text_list, num_tokens_list, embeddings, db_content = None, None, None, None
        new_type, new_title = None, None
        if (
            (update_dict.get("type") is not None)
            or (update_dict.get("content") is not None)
            or (update_dict.get("title") is not None)
        ):
            new_type = RecordType(update_dict.get("type", record.type))
            new_title = update_dict.get("title", record.title)
            new_content = update_dict.get("content", record.content) if new_type == RecordType.TEXT else None
            text_splitter = TextSplitter(**update_dict["text_splitter"])

            # split content into chunks
            chunk_text_list, num_tokens_list, embeddings, db_content = await process_content(
                collection=collection,
                type=new_type,
                title=new_title,
                content=new_content,
                file_id=update_dict.get("file_id"),
                url=update_dict.get("url"),
                text_splitter=text_splitter,
                max_num_chunks=record.num_chunks + collection.rest_capacity(),
            )

        # update record
        await db_record.update_record(
            collection=collection,
            record=record,
            title=new_title,
            type=new_type,
            content=db_content,
            chunk_text_list=chunk_text_list,
            chunk_num_tokens_list=num_tokens_list,
            chunk_embedding_list=embeddings,
            metadata=new_metadata,
        )

        # get the updated record
        record = await self.get(collection_id=collection_id, record_id=record_id)
        return record

    async def delete(self, **kwargs) -> None:
        # handle kwargs
        self._check_kwargs(object_id_required=None, **kwargs)
        collection_id = kwargs["collection_id"]
        record_id = kwargs["record_id"]

        # delete record
        collection = await collection_ops.get(collection_id=collection_id)
        record = await self.get(collection_id=collection_id, record_id=record_id)
        await db_record.delete_record(record)
        await collection_ops.redis.pop(collection)


record_ops = RecordModelOperator(
    postgres_pool=postgres_pool,
    entity_class=Record,
    redis=None,
)
