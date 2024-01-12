from pydantic import BaseModel
from typing import Dict
from common.utils import load_json_attr
from .base import SerializePurpose

__all__ = ["Provider"]


class Provider(BaseModel):
    provider_id: str
    name: str
    credentials_schema: Dict
    # todo: add icon_svg_url

    @staticmethod
    def object_name():
        return "Provider"

    @classmethod
    def build(cls, row: Dict):
        return cls(
            provider_id=row["provider_id"],
            credentials_schema=load_json_attr(row, "credentials_schema", {}),
            name=row["name"],
        )

    def to_dict(
        self,
        purpose: SerializePurpose = None,
    ):
        return {
            "object": self.object_name(),
            "provider_id": self.provider_id,
            "credentials_schema": self.credentials_schema,
            "name": self.name,
        }
