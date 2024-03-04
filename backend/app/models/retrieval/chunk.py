from typing import Dict, Optional, List
from pydantic import Field

from tkhelper.models import ModelEntity
from tkhelper.models.operator.postgres_operator import PostgresModelOperator
from tkhelper.utils import generate_random_id, load_json_attr
from tkhelper.schemas.field import *

from app.database import postgres_pool
from .collection import Collection, collection_ops


__all__ = [
    "Chunk",
    "chunk_ops",
]


class Chunk(ModelEntity):
    object: str = "Chunk"
    chunk_id: str = id_field("chunk", length_range=(1, 50))
    record_id: Optional[str] = id_field("record", length_range=(1, 50))
    collection_id: str = id_field("collection", length_range=(1, 50))
    content: str = Field(..., description="The content of the chunk")
    num_tokens: int = Field(..., ge=0, description="The number of tokens in the chunk", examples=[100])
    metadata: Dict = metadata_field()
    updated_timestamp: int = updated_timestamp_field()
    created_timestamp: int = created_timestamp_field()

    score: Optional[float] = Field(None, description="The score of the chunk", examples=[0.8])

    @staticmethod
    def build(row: Dict):
        return Chunk(
            chunk_id=row["chunk_id"],
            record_id=row.get("record_id"),
            collection_id=row["collection_id"],
            content=row["content"],
            num_tokens=row["num_tokens"],
            metadata=load_json_attr(row, "metadata", {}),
            score=row.get("score"),
            updated_timestamp=row["updated_timestamp"],
            created_timestamp=row["created_timestamp"],
        )

    @staticmethod
    def object_name():
        return "chunk"

    @staticmethod
    def object_plural_name() -> str:
        return "chunks"

    @staticmethod
    def table_name() -> str:
        return "chunk"

    @staticmethod
    def id_field_name() -> str:
        return "chunk_id"

    @staticmethod
    def primary_key_fields() -> List[str]:
        return ["chunk_id"]

    @staticmethod
    def generate_random_id():
        return "LmK0" + generate_random_id(20)

    @staticmethod
    def list_prefix_filter_fields() -> List[str]:
        return ["chunk_id"]

    @staticmethod
    def parent_models() -> List:
        return [Collection]

    @staticmethod
    def parent_operator() -> List:
        return [collection_ops]

    @staticmethod
    def create_fields() -> List[str]:
        return ["content", "metadata"]

    @staticmethod
    def update_fields() -> List[str]:
        return ["content", "metadata"]

    @staticmethod
    def fields_exclude_in_response():
        return ["score"]


chunk_ops = PostgresModelOperator(
    postgres_pool=postgres_pool,
    entity_class=Chunk,
    redis=None,
)
