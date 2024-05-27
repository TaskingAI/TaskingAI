from typing import Any, Dict, List, Optional, Tuple

from app.database import postgres_pool, redis_conn
from app.database_ops.retrieval import collection as db_collection
from app.models import Collection
from app.models.model.model import Model
from app.schemas import CollectionCreateRequest
from tkhelper.error import ErrorCode, raise_http_error
from tkhelper.models import ModelEntity, RedisOperator
from tkhelper.models.operator.postgres_operator import PostgresModelOperator
from tkhelper.models.type import SortOrderEnum

from ..model import model_ops

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
    async def _get_model_name_entity(self, collection: Collection) -> Dict[str, Any]:
        model: Model = await model_ops.get(model_id=collection.embedding_model_id)
        collection_dict = collection.to_response_dict()
        collection_dict["model_name"] = model.name
        return collection_dict

    async def ui_get(self, raise_not_found_error=True, **kwargs) -> Optional[Dict[str, Any]]:
        collection: Optional[Collection] = await super().get(raise_not_found_error, **kwargs)
        if collection:
            return await self._get_model_name_entity(collection)
        return collection

    async def ui_list(
        self,
        limit: int,
        order: SortOrderEnum,
        after_id: Optional[str] = None,
        before_id: Optional[str] = None,
        prefix_filters: Optional[Dict] = None,
        equal_filters: Optional[Dict] = None,
        **kwargs,
    ) -> Tuple[List[Dict[str, Any]], bool]:
        collections, has_more = await super().list(
            limit, order, after_id, before_id, prefix_filters, equal_filters, **kwargs
        )
        collection_dict_list = []
        for collection in collections:
            collection_dict_list.append(await self._get_model_name_entity(collection))
        return collection_dict_list, has_more

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
        allowed_capacity = [1000]
        if capacity not in allowed_capacity:
            raise_http_error(
                ErrorCode.REQUEST_VALIDATION_ERROR,
                message=f"Capacity must be one of {allowed_capacity}.",
            )

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
