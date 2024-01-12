from typing import Dict
from enum import Enum
from pydantic import BaseModel
from common.utils import generate_random_id, load_json_attr
from common.models import Status, SerializePurpose

__all__ = [
    "RecordType",
    "Record",
]


class RecordType(str, Enum):
    TEXT = "text"
    FILE = "file"


class Record(BaseModel):
    record_id: str
    title: str
    collection_id: str
    status: Status
    num_chunks: int
    type: RecordType
    content: str
    metadata: Dict
    updated_timestamp: int
    created_timestamp: int

    @staticmethod
    def generate_random_id():
        return "qpEa" + generate_random_id(20)

    @staticmethod
    def object_name():
        return "Record"

    @classmethod
    def build(cls, row: Dict):
        return cls(
            record_id=row["record_id"],
            title=row["title"],
            collection_id=row["collection_id"],
            status=Status(row["status"]),
            num_chunks=row["num_chunks"],
            type=RecordType(row["type"]),
            content=load_json_attr(row, "content", {}),
            metadata=load_json_attr(row, "metadata", {}),
            updated_timestamp=row["updated_timestamp"],
            created_timestamp=row["created_timestamp"],
        )

    def to_dict(self, purpose: SerializePurpose):
        ret = {
            "object": self.object_name(),
            "record_id": self.record_id,
            "title": self.title,
            "collection_id": self.collection_id,
            "status": self.status.value,
            "num_chunks": self.num_chunks,
            "type": self.type.value,
            "content": self.content,
            "metadata": self.metadata,
            "updated_timestamp": self.updated_timestamp,
            "created_timestamp": self.created_timestamp,
        }
        return ret
