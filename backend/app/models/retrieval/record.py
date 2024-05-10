from typing import Dict, List, Optional
from enum import Enum
from pydantic import Field
import json

from tkhelper.models import Status, ModelEntity
from tkhelper.utils import generate_random_id, load_json_attr
from tkhelper.schemas.field import *

from .collection import Collection


__all__ = [
    "RecordType",
    "Record",
]


class RecordType(str, Enum):
    TEXT = "text"
    FILE = "file"
    WEB = "web"


class Record(ModelEntity):
    object: str = "Record"
    record_id: str = id_field("record", length_range=(1, 50))
    collection_id: str = id_field("collection", length_range=(1, 50))
    title: str = Field("", description="The title of the record", examples=["Record 1"])
    status: Status = Field(..., description="The status of the record", examples=["ready"])
    num_chunks: int = Field(..., ge=0, description="Number of chunks in the record", examples=[20])
    type: RecordType = Field(..., description="The type of the record", examples=["text"])
    content: str = Field(..., description="The content of the record")
    metadata: Dict = metadata_field()
    updated_timestamp: int = updated_timestamp_field()
    created_timestamp: int = created_timestamp_field()

    def file_id(self) -> Optional[str]:
        try:
            content_dict = json.loads(self.content)
            return content_dict.get("file_id")
        except Exception:
            return None

    def url(self) -> Optional[str]:
        try:
            content_dict = json.loads(self.content)
            return content_dict.get("url")
        except Exception:
            return None

    @staticmethod
    def build(row: Dict):
        return Record(
            record_id=row["record_id"],
            title=row["title"],
            collection_id=row["collection_id"],
            status=Status(row["status"]),
            num_chunks=row["num_chunks"],
            type=RecordType(row["type"]),
            content=row["content"],
            metadata=load_json_attr(row, "metadata", {}),
            updated_timestamp=row["updated_timestamp"],
            created_timestamp=row["created_timestamp"],
        )

    @staticmethod
    def object_name():
        return "record"

    @staticmethod
    def object_plural_name() -> str:
        return "records"

    @staticmethod
    def table_name() -> str:
        return "record"

    @staticmethod
    def id_field_name() -> str:
        return "record_id"

    @staticmethod
    def primary_key_fields() -> List[str]:
        return ["collection_id", "record_id"]

    @staticmethod
    def generate_random_id():
        return "qpEa" + generate_random_id(20)

    @staticmethod
    def list_prefix_filter_fields() -> List[str]:
        return ["record_id"]

    @staticmethod
    def parent_models() -> List:
        return [Collection]

    @staticmethod
    def parent_operator() -> List:
        from app.operators import collection_ops

        return [collection_ops]

    @staticmethod
    def create_fields() -> List[str]:
        raise NotImplementedError

    @staticmethod
    def update_fields() -> List[str]:
        raise NotImplementedError

    @staticmethod
    def fields_exclude_in_response():
        return []
