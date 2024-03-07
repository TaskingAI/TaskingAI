from typing import Dict

from tkhelper.models.operator.postgres_operator import PostgresModelOperator, ModelEntity
from tkhelper.error import raise_http_error, ErrorCode

from app.database import postgres_pool
from app.models import Record, RecordType, TextSplitter
from app.database_ops.retrieval import record as db_record

from .collection import collection_ops
from ..model import model_ops

__all__ = ["record_ops"]


class RecordModelOperator(PostgresModelOperator):
    async def create(
        self,
        create_dict: Dict,
        **kwargs,
    ) -> ModelEntity:
        from app.services.retrieval.embedding import embed_documents

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

        # validate model
        embedding_model = await model_ops.get(model_id=collection.embedding_model_id)

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
        record = await self.get(collection_id=collection_id, record_id=new_record_id)

        return record

    async def update(
        self,
        update_dict: Dict,
        **kwargs,
    ) -> ModelEntity:
        from app.services.retrieval.embedding import embed_documents

        # handle kwargs
        self._check_kwargs(object_id_required=None, **kwargs)
        collection_id = kwargs["collection_id"]
        record_id = kwargs["record_id"]

        type = RecordType(update_dict["type"])
        title = update_dict["title"]
        content = update_dict["content"]
        text_splitter = TextSplitter(**update_dict["text_splitter"])
        metadata = update_dict["metadata"]

        collection = await collection_ops.get(collection_id=collection_id)
        record = await self.get(collection_id=collection_id, record_id=record_id)
        new_type = type if type is not None else record.type
        new_title = title if title is not None else record.title

        chunk_text_list, num_tokens_list, embeddings = None, None, None

        if content is not None:
            # validate model
            embedding_model = await model_ops.get(model_id=collection.embedding_model_id)

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
