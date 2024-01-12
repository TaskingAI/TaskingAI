from pydantic import BaseModel
from typing import Dict
from .base import Status
from common.utils import generate_random_id, load_json_attr
from .text_splitter import TextSplitter, build_text_splitter
from .base import SerializePurpose

__all__ = [
    "Collection",
]


class Collection(BaseModel):
    # basic info
    collection_id: str
    name: str
    description: str
    num_records: int
    num_chunks: int
    capacity: int
    embedding_model_id: str
    embedding_size: int
    text_splitter: TextSplitter
    status: Status
    metadata: Dict
    updated_timestamp: int
    created_timestamp: int

    @staticmethod
    def object_name():
        return "Collection"

    def has_available_capacity(self, capacity: int):
        return (self.capacity - self.num_chunks) >= capacity

    @staticmethod
    def generate_random_id():
        return generate_random_id(24).lower()

    @classmethod
    def build(cls, row: Dict):
        text_splitter_dict = load_json_attr(row, "text_splitter", {"type": "token"})
        text_splitter = build_text_splitter(text_splitter_dict)

        return cls(
            collection_id=row["collection_id"],
            name=row["name"],
            description=row["description"],
            num_records=row["num_records"],
            num_chunks=row["num_chunks"],
            capacity=row["capacity"],
            embedding_model_id=row["embedding_model_id"],
            embedding_size=row["embedding_size"],
            text_splitter=text_splitter,
            metadata=load_json_attr(row, "metadata", {}),
            updated_timestamp=row["updated_timestamp"],
            created_timestamp=row["created_timestamp"],
        )

    def to_dict(self, purpose: SerializePurpose):
        return {
            "object": self.object_name(),
            "collection_id": self.collection_id,
            "name": self.name,
            "description": self.description,
            "num_records": self.num_records,
            "num_chunks": self.num_chunks,
            "capacity": self.capacity,
            "embedding_model_id": self.embedding_model_id,
            "embedding_size": self.embedding_size,
            "status": self.status.value,
            "text_splitter": self.text_splitter.model_dump(),
            "metadata": self.metadata,
            "updated_timestamp": self.updated_timestamp,
            "created_timestamp": self.created_timestamp,
        }
