from enum import Enum
from pydantic import BaseModel
from typing import Dict, Optional, List

__all__ = ["ModelType", "ModelSchema"]


class ModelType(str, Enum):
    CHAT_COMPLETION = "chat_completion"
    TEXT_EMBEDDING = "text_embedding"
    WILDCARD = "wildcard"


class ModelSchema(BaseModel):
    model_schema_id: str
    name: str
    description: str

    provider_id: str
    provider_model_id: Optional[str]

    type: ModelType
    properties: Optional[Dict]
    allowed_configs: List[str]
    pricing: Optional[Dict]

    @staticmethod
    def object_name():
        return "ModelSchema"

    @classmethod
    def build(cls, row: Dict):
        return cls(
            model_schema_id=row["model_schema_id"],
            name=row["name"] or "",
            description=row.get("description", ""),
            provider_id=row["provider_id"],
            provider_model_id=row["provider_model_id"],
            type=row["type"],
            properties=row.get("properties"),
            allowed_configs=row.get("allowed_configs") or [],
            pricing=row.get("pricing"),
        )

    def to_dict(self, lang: str):
        from app.services.model import i18n_text

        return {
            "object": self.object_name(),
            "model_schema_id": self.model_schema_id,
            "name": i18n_text(self.provider_id, self.name, lang),
            "description": i18n_text(self.provider_id, self.description, lang),
            "provider_id": self.provider_id,
            "provider_model_id": self.provider_model_id,
            "type": self.type.value,
            "properties": self.properties,
            "allowed_configs": self.allowed_configs,
            "pricing": self.pricing,
        }
