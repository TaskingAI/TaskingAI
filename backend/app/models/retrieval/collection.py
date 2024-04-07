from pydantic import Field
from typing import Dict, List

from tkhelper.models import Status, ModelEntity
from tkhelper.utils import generate_random_id, load_json_attr
from tkhelper.schemas.field import *


__all__ = ["Collection"]


class Collection(ModelEntity):
    # basic info
    object: str = "Collection"
    collection_id: str = id_field("collection", length_range=(1, 50))
    name: str = name_field()
    description: str = description_field()
    num_records: int = Field(..., description="Number of records in the collection", examples=[10])
    num_chunks: int = Field(..., description="Number of chunks in the collection", examples=[20])
    capacity: int = Field(..., ge=0, description="The maximum number of chunks the collection can hold", examples=[100])
    embedding_model_id: str = Field(
        ..., min_length=8, max_length=8, description="The id of the embedding model", example="model123"
    )
    embedding_size: int = Field(..., ge=0, description="The size of the embedding vector", examples=[768])
    status: Status = Field(..., description="The status of the collection", examples=["ready"])
    metadata: Dict = metadata_field()
    updated_timestamp: int = updated_timestamp_field()
    created_timestamp: int = created_timestamp_field()

    def has_available_capacity(self, capacity: int):
        return (self.capacity - self.num_chunks) >= capacity

    def rest_capacity(self):
        return self.capacity - self.num_chunks

    @staticmethod
    def get_chunk_table_name(collection_id: str):
        """
        Get the chunk table name in postgres database
        :param collection_id:
        :return: the chunk table name
        """

        return f"c1_{collection_id}"

    @staticmethod
    def build(row: Dict):
        return Collection(
            collection_id=row["collection_id"],
            name=row["name"],
            description=row["description"],
            num_records=row["num_records"],
            num_chunks=row["num_chunks"],
            capacity=row["capacity"],
            embedding_model_id=row["embedding_model_id"],
            embedding_size=row["embedding_size"],
            status=Status(row["status"]),
            metadata=load_json_attr(row, "metadata", {}),
            updated_timestamp=row["updated_timestamp"],
            created_timestamp=row["created_timestamp"],
        )

    @staticmethod
    def object_name():
        return "collection"

    @staticmethod
    def object_plural_name() -> str:
        return "collections"

    @staticmethod
    def table_name() -> str:
        return "collection"

    @staticmethod
    def id_field_name() -> str:
        return "collection_id"

    @staticmethod
    def primary_key_fields() -> List[str]:
        return ["collection_id"]

    @staticmethod
    def generate_random_id():
        return "DbgY" + generate_random_id(20).lower()

    @staticmethod
    def list_prefix_filter_fields() -> List[str]:
        return ["collection_id", "name"]

    @staticmethod
    def parent_models() -> List:
        return []

    @staticmethod
    def parent_operator() -> List:
        return []

    @staticmethod
    def create_fields() -> List[str]:
        return ["name", "description", "capacity", "embedding_model_id", "metadata"]

    @staticmethod
    def update_fields() -> List[str]:
        return ["name", "description", "metadata"]

    @staticmethod
    def fields_exclude_in_response():
        return []
