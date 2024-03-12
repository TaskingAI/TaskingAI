from typing import Dict

from tkhelper.models import RedisOperator, ModelEntity
from tkhelper.models.operator.postgres_operator import PostgresModelOperator
from tkhelper.error import raise_http_error, ErrorCode

from app.schemas import CollectionCreateRequest
from app.database import redis_conn, postgres_pool
from app.models import Collection
from app.database_ops.retrieval import collection as db_collection


__all__ = [
    "collection_ops",
]


async def _verify_embedding_model(embedding_model_id: str) -> int:
    """
    Verify the embedding model
    :param embedding_model_id: the embedding model id
    :return: the embedding size
    """
    from app.services.model import get_model

    # validate embedding model
    embedding_model = await get_model(embedding_model_id)
    if not embedding_model.is_text_embedding():
        raise_http_error(
            ErrorCode.REQUEST_VALIDATION_ERROR,
            message=f"Model {embedding_model_id} is not a valid embedding model.",
        )

    # validate embedding size
    embedding_size = embedding_model.properties.get("embedding_size")
    if not embedding_size:
        raise_http_error(
            ErrorCode.REQUEST_VALIDATION_ERROR,
            message=f"Embedding model {embedding_model_id} has an invalid embedding size.",
        )

    return embedding_size


class CollectionModelOperator(PostgresModelOperator):
    async def create(
        self,
        create_dict: Dict,
        **kwargs,
    ) -> ModelEntity:
        # handle kwargs
        self._check_kwargs(object_id_required=None, **kwargs)
        request = CollectionCreateRequest(**create_dict)
        name = request.name
        description = request.description
        capacity = request.capacity
        embedding_model_id = request.embedding_model_id
        metadata = request.metadata

        # verify embedding model
        embedding_size = await _verify_embedding_model(embedding_model_id)

        # create
        new_collection_id = Collection.generate_random_id()
        await db_collection.create_collection(
            collection_id=new_collection_id,
            name=name,
            description=description,
            capacity=capacity,
            embedding_model_id=embedding_model_id,
            embedding_size=embedding_size,
            metadata=metadata,
        )

        # get collection
        collection = await self.get(collection_id=new_collection_id)

        return collection

    async def delete(self, **kwargs) -> None:
        # handle kwargs
        self._check_kwargs(object_id_required=True, **kwargs)
        collection_id = kwargs["collection_id"]

        # get collection
        collection = await self.get(collection_id=collection_id)

        # delete
        await db_collection.delete_collection(collection=collection)

        # pop collection redis
        await self.redis.pop(collection)


collection_ops = CollectionModelOperator(
    postgres_pool=postgres_pool,
    entity_class=Collection,
    redis=RedisOperator(
        entity_class=Collection,
        redis_conn=redis_conn,
    ),
)
