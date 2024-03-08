from pydantic import BaseModel
from typing import Dict, List
from tkhelper.utils import load_json_attr
from .model_schema import ModelType

__all__ = ["Provider"]


class Provider(BaseModel):
    provider_id: str
    name: str
    description: str
    credentials_schema: Dict
    icon_svg_url: str
    num_model_schemas: int
    model_types: List[str]
    resources: Dict[str, str]
    updated_timestamp: int

    def has_model_type(self, model_type: ModelType):
        return (model_type.value in self.model_types) or (ModelType.WILDCARD.value in self.model_types)

    @staticmethod
    def object_name():
        return "Provider"

    @classmethod
    def build(cls, row: Dict, num_model_schemas: int, model_types: List[str]):
        return cls(
            provider_id=row["provider_id"],
            credentials_schema=load_json_attr(row, "credentials_schema", {}),
            name=row["name"],
            description=row["description"],
            icon_svg_url=row["icon_svg_url"],
            num_model_schemas=num_model_schemas,
            model_types=model_types,
            resources=load_json_attr(row, "resources", {}),
            updated_timestamp=row["updated_timestamp"],
        )

    def to_dict(self, lang: str):
        from app.services.model import i18n_text

        properties_dict = self.credentials_schema.get("properties", {})
        credentials_schema_dict = {
            "type": "object",
            "properties": {
                k: {
                    "type": v["type"],
                    "description": i18n_text(self.provider_id, v["description"], lang),
                    "secret": v.get("secret", False),
                }
                for k, v in properties_dict.items()
            },
            "required": self.credentials_schema.get("required", []),
        }
        return {
            "object": self.object_name(),
            "provider_id": self.provider_id,
            "name": i18n_text(self.provider_id, self.name, lang),
            "description": i18n_text(self.provider_id, self.description, lang),
            "credentials_schema": credentials_schema_dict,
            "icon_svg_url": self.icon_svg_url,
            "num_model_schemas": self.num_model_schemas,
            "model_types": self.model_types,
            "resources": self.resources,
            "updated_timestamp": self.updated_timestamp,
        }
