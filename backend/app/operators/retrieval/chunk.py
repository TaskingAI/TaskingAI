from typing import Dict, Optional, List

from tkhelper.models import SortOrderEnum
from tkhelper.models.operator.postgres_operator import PostgresModelOperator, ModelEntity
from tkhelper.database.postgres import ops as postgres_ops

from app.database import postgres_pool
from app.models import Chunk, Collection, default_tokenizer
from app.database_ops.retrieval import chunk as db_chunk
from app.schemas import ChunkUpdateRequest, ChunkCreateRequest
from .collection import collection_ops
from ..model import model_ops

__all__ = [
    "chunk_ops",
]


class ChunkModelOperator(PostgresModelOperator):
    async def create(
        self,
        create_dict: Dict,
        **kwargs,
    ) -> ModelEntity:
        from app.services.retrieval.embedding import embed_documents

        # handle kwargs
        self._check_kwargs(object_id_required=None, **kwargs)
        collection_id = kwargs["collection_id"]

        request = ChunkCreateRequest(**create_dict)
        content = request.content
        metadata = request.metadata

        # Get collection
        collection: Collection = await collection_ops.get(collection_id=collection_id)

        # Get model
        embedding_model = await model_ops.get(model_id=collection.embedding_model_id)

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
        chunk = await self.get(collection_id=collection_id, chunk_id=new_chunk_id)

        # pop collection redis
        await collection_ops.redis.pop(collection)
        return chunk

    async def update(
        self,
        update_dict: Dict,
        **kwargs,
    ) -> ModelEntity:
        from app.services.retrieval.embedding import embed_documents

        # handle kwargs
        self._check_kwargs(object_id_required=None, **kwargs)
        collection_id = kwargs["collection_id"]
        chunk_id = kwargs["chunk_id"]

        request = ChunkUpdateRequest(**update_dict)
        content = request.content
        metadata = request.metadata
        collection = await collection_ops.get(collection_id=collection_id)
        chunk = await self.get(collection_id=collection_id, chunk_id=chunk_id)

        num_tokens, embedding = None, None

        if content:
            # Get model
            embedding_model = await model_ops.get(model_id=collection.embedding_model_id)

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
        chunk = await chunk_ops.get(collection_id=collection_id, chunk_id=chunk_id)
        return chunk

    async def delete(self, **kwargs) -> None:
        # handle kwargs
        self._check_kwargs(object_id_required=None, **kwargs)
        collection_id = kwargs["collection_id"]
        chunk_id = kwargs["chunk_id"]

        # delete chunk
        collection = await collection_ops.get(collection_id=collection_id)
        chunk = await self.get(collection_id=collection_id, chunk_id=chunk_id)
        await db_chunk.delete_chunk(chunk=chunk)
        await collection_ops.redis.pop(collection)

    async def list(
        self,
        limit: int,
        order: SortOrderEnum,
        after_id: Optional[str] = None,
        before_id: Optional[str] = None,
        prefix_filters: Optional[Dict] = None,
        equal_filters: Optional[Dict] = None,
        **kwargs,
    ) -> (List[ModelEntity], bool):
        # check kwargs contains all the primary key fields except the id field
        kwargs = self._check_kwargs(object_id_required=False, **kwargs)
        collection = await collection_ops.get(collection_id=kwargs["collection_id"])
        table_name = Collection.get_chunk_table_name(collection_id=collection.collection_id)

        after = None
        if after_id:
            after_kwargs = {**kwargs, self.entity_class.id_field_name(): after_id}
            after = await self.get(**after_kwargs)

        before = None
        if before_id:
            before_kwargs = {**kwargs, self.entity_class.id_field_name(): before_id}
            before = await self.get(**before_kwargs)

        # update equal_filters with kwargs
        if not equal_filters:
            equal_filters = {}
        equal_filters.update({k: v for k, v in kwargs.items()})

        async with self.postgres_pool.get_db_connection() as conn:
            object_dicts, has_more = await postgres_ops.list_objects(
                conn=conn,
                table_name=table_name,
                order=order,
                sort_field="created_timestamp",
                object_id_name=self.entity_class.id_field_name(),
                limit=limit,
                after_id=getattr(after, self.entity_class.id_field_name()) if after else None,
                after_value=getattr(after, "created_timestamp") if after else None,
                before_id=getattr(before, self.entity_class.id_field_name()) if before else None,
                before_value=getattr(before, "created_timestamp") if before else None,
                offset=None,
                prefix_filters=prefix_filters,
                equal_filters=equal_filters,
            )
            entities = [self.entity_class.build(object_dict) for object_dict in object_dicts]
            return entities, has_more

    async def _get_entity(self, conn, **kwargs) -> Optional[ModelEntity]:
        collection = await collection_ops.get(collection_id=kwargs["collection_id"])
        table_name = Collection.get_chunk_table_name(collection_id=collection.collection_id)

        object_dict = await postgres_ops.get_object(
            conn=conn,
            table_name=table_name,
            equal_filters={k: v for k, v in kwargs.items() if k in self.entity_class.primary_key_fields()},
        )
        return self.entity_class.build(object_dict) if object_dict else None


chunk_ops = ChunkModelOperator(
    postgres_pool=postgres_pool,
    entity_class=Chunk,
    redis=None,
)
