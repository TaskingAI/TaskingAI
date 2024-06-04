from typing import Dict, List, Optional
from pydantic import BaseModel
from tkhelper.models import ModelEntity
from tkhelper.utils import generate_random_id, load_json_attr

__all__ = ["Model", "ModelFallback", "ModelFallbackConfig"]


class ModelFallback(BaseModel):
    model_id: str


class ModelFallbackConfig(BaseModel):
    model_list: List[ModelFallback]


class Model(ModelEntity):
    model_id: str
    model_schema_id: str

    provider_id: str
    provider_model_id: str

    name: str
    type: str
    properties: Dict
    configs: Dict
    encrypted_credentials: Dict
    display_credentials: Dict
    updated_timestamp: int
    created_timestamp: int
    fallbacks: Optional[ModelFallbackConfig]

    def model_schema(self):
        from app.services.model import get_model_schema

        return get_model_schema(self.model_schema_id)

    def provider(self):
        from app.services.model import get_provider

        return get_provider(self.provider_id)

    def is_chat_completion(self):
        return self.type == "chat_completion"

    def is_text_embedding(self):
        return self.type == "text_embedding"

    def is_rerank(self):
        return self.type == "rerank"

    def is_custom_host(self):
        return self.provider_id == "custom_host"

    def allow_function_call(self):
        return self.type == "chat_completion" and self.properties.get("function_call", False)

    def allow_streaming(self):
        return self.type == "chat_completion" and self.properties.get("streaming", False)

    @classmethod
    def build(cls, row: Dict):
        from app.services.model import get_model_schema

        model_schema_id = row["model_schema_id"]
        model_schema = get_model_schema(model_schema_id)
        model_schema_properties = {}
        if model_schema:
            model_schema_properties = model_schema.properties or {}
        properties = model_schema_properties or load_json_attr(row, "properties", {})
        fallbacks_dict = load_json_attr(row, "fallbacks", {}) or {"model_list": []}
        fallbacks = ModelFallbackConfig(**fallbacks_dict)

        return cls(
            model_id=row["model_id"],
            model_schema_id=row["model_schema_id"],
            provider_id=row["provider_id"],
            provider_model_id=row["provider_model_id"],
            name=row["name"],
            type=row["type"],
            properties=properties,
            fallbacks=fallbacks,
            configs=load_json_attr(row, "configs", {}),
            encrypted_credentials=load_json_attr(row, "encrypted_credentials", {}),
            display_credentials=load_json_attr(row, "display_credentials", {}),
            updated_timestamp=row["updated_timestamp"],
            created_timestamp=row["created_timestamp"],
        )

    def to_response_dict(self) -> Dict:
        model_schema = self.model_schema()
        return {
            "object": "Model",
            "model_id": self.model_id,
            "model_schema_id": self.model_schema_id,
            "provider_id": model_schema.provider_id or self.provider_id,
            "provider_model_id": model_schema.provider_model_id or self.provider_model_id,
            "name": self.name,
            "type": self.type,
            "properties": model_schema.properties or self.properties,
            "fallbacks": self.fallbacks.model_dump() if self.fallbacks else None,
            "configs": self.configs,
            "display_credentials": self.display_credentials,
            "updated_timestamp": self.updated_timestamp,
            "created_timestamp": self.created_timestamp,
        }

    @staticmethod
    def object_name() -> str:
        return "model"

    @staticmethod
    def object_plural_name() -> str:
        return "models"

    @staticmethod
    def table_name() -> str:
        return "model"

    @staticmethod
    def id_field_name() -> str:
        return "model_id"

    @staticmethod
    def primary_key_fields() -> List[str]:
        return ["model_id"]

    @staticmethod
    def generate_random_id() -> str:
        return "Tp" + generate_random_id(6)

    @staticmethod
    def list_prefix_filter_fields() -> List[str]:
        return ["model_id", "name"]

    @staticmethod
    def list_equal_filter_fields() -> List[str]:
        return ["type"]

    @staticmethod
    def parent_models() -> List:
        return []

    @staticmethod
    def parent_operator() -> List:
        return []

    @staticmethod
    def create_fields() -> List[str]:
        raise NotImplementedError

    @staticmethod
    def update_fields() -> List[str]:
        raise NotImplementedError

    @staticmethod
    def fields_exclude_in_response():
        return ["encrypted_credentials"]
