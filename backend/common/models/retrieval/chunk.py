from typing import Dict, Optional
from pydantic import BaseModel
from common.utils import generate_random_id, load_json_attr
from common.models import SerializePurpose

__all__ = [
    "Chunk",
]


class Chunk(BaseModel):
    chunk_id: str
    record_id: str
    collection_id: str
    content: str  # todo: text content
    metadata: Dict
    updated_timestamp: int
    created_timestamp: int

    score: Optional[float] = None

    @staticmethod
    def generate_random_id():
        return "LmK0" + generate_random_id(20)

    @staticmethod
    def object_name():
        return "Chunk"

    @classmethod
    def build(cls, row: Dict):
        return cls(
            chunk_id=row["chunk_id"],
            record_id=row["record_id"],
            collection_id=row["collection_id"],
            content=row["content"],
            metadata=load_json_attr(row, "metadata", {}),
            score=row.get("score"),
            updated_timestamp=row["updated_timestamp"],
            created_timestamp=row["created_timestamp"],
        )

    def to_dict(self, purpose: SerializePurpose):
        ret = {
            "object": self.object_name(),
            "chunk_id": self.chunk_id,
            "record_id": self.record_id,
            "collection_id": self.collection_id,
            "content": self.content,
            "metadata": self.metadata,
            "updated_timestamp": self.updated_timestamp,
            "created_timestamp": self.created_timestamp,
        }

        if purpose == SerializePurpose.RESPONSE:
            if self.score is not None:
                ret["score"] = self.score

        return ret
