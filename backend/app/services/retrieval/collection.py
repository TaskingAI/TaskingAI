from typing import Dict
from tkhelper.error import ErrorCode, raise_http_error

from app.models import Collection, ModelType
from app.operators import collection_ops
from app.database_ops.retrieval import collection as db_collection
from app.services.model import get_model

__all__ = [
    "get_collection",
    "create_collection",
    "delete_collection",
]


async def get_collection(collection_id: str) -> Collection:
    """
    Get collection
    :param collection_id: the collection id
    :return: the collection
    """
    collection: Collection = await collection_ops.get(collection_id=collection_id)
    return collection


async def create_collection(
    name: str,
    description: str,
    capacity: int,
    embedding_model_id: str,
    metadata: Dict[str, str],
) -> Collection:
    """
    Create collection
    :param name: the collection name
    :param description: the collection description
    :param capacity: the collection capacity
    :param embedding_model_id: the embedding model id
    :param metadata: the collection metadata
    :return: the created collection
    """

    # validate embedding model
    embedding_model = await get_model(embedding_model_id)
    model_schema = embedding_model.model_schema()
    if not model_schema.type == ModelType.TEXT_EMBEDDING:
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

    # create collection
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
    collection = await get_collection(collection_id=new_collection_id)
    return collection


async def delete_collection(collection_id: str) -> None:
    """
    Delete collection
    :param collection_id: the collection id
    """

    collection = await get_collection(collection_id)
    await db_collection.delete_collection(collection)
