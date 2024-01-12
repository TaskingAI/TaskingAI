from enum import Enum
from pydantic import BaseModel
from typing import Dict
from common.utils import load_json_attr, load_normal_attr
from .base import SerializePurpose

__all__ = ["ModelType", "ModelSchema"]


class ModelType(str, Enum):
    CHAT_COMPLETION = "chat_completion"
    TEXT_EMBEDDING = "text_embedding"


class ModelSchema(BaseModel):
    model_schema_id: str
    name: str
    description: str

    provider_id: str
    provider_model_id: str

    type: ModelType
    properties: Dict

    @staticmethod
    def object_name():
        return "ModelSchema"

    @classmethod
    def build(cls, row: Dict):
        return cls(
            model_schema_id=row["model_schema_id"],
            name=row["name"] or "",
            description=load_normal_attr(row, "description", ""),
            provider_id=row["provider_id"],
            provider_model_id=row["provider_model_id"],
            type=row["type"],
            properties=load_json_attr(row, "properties", {}),
        )

    def to_dict(
        self,
        purpose: SerializePurpose = None,
    ):
        ret = {
            "object": self.object_name(),
            "model_schema_id": self.model_schema_id,
            "name": self.name,
            "description": self.description,
            "provider_id": self.provider_id,
            "provider_model_id": self.provider_model_id,
            "type": self.type.value,
            "properties": self.properties,
        }

        return ret
