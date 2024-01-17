from common.utils import generate_random_id
from pydantic import BaseModel
from typing import Dict
from common.models import SerializePurpose
from common.utils import load_json_attr


__all__ = ["Model"]


class Model(BaseModel):
    model_id: str
    model_schema_id: str

    provider_id: str
    provider_model_id: str

    name: str
    type: str
    properties: Dict
    encrypted_credentials: Dict
    display_credentials: Dict
    updated_timestamp: int
    created_timestamp: int

    def model_schema(self):
        from common.services.model.model_schema import get_model_schema

        return get_model_schema(self.model_schema_id)

    def provider(self):
        from common.services.model.model_schema import get_provider

        return get_provider(self.provider_id)

    @staticmethod
    def object_name():
        return "Model"

    @staticmethod
    def generate_random_id():
        return "Tp" + generate_random_id(6)

    @staticmethod
    def generate_random_apikey(apikey_id):
        return apikey_id + generate_random_id(24)

    @classmethod
    def build(cls, row: Dict):
        from common.services.model.model_schema import get_model_schema

        model_schema_id = row["model_schema_id"]
        model_schema = get_model_schema(model_schema_id)
        properties = {}
        if model_schema:
            properties = model_schema.properties
        return cls(
            model_id=row["model_id"],
            model_schema_id=row["model_schema_id"],
            provider_id=row["provider_id"],
            provider_model_id=row["provider_model_id"],
            name=row["name"],
            type=row["type"],
            properties=properties,
            encrypted_credentials=load_json_attr(row, "encrypted_credentials", {}),
            display_credentials=load_json_attr(row, "display_credentials", {}),
            updated_timestamp=row["updated_timestamp"],
            created_timestamp=row["created_timestamp"],
        )

    def to_dict(
        self,
        purpose: SerializePurpose = None,
    ):
        ret = {
            "object": self.object_name(),
            "model_id": self.model_id,
            "model_schema_id": self.model_schema_id,
            "provider_id": self.provider_id,
            "provider_model_id": self.provider_model_id,
            "name": self.name,
            "type": self.type,
            "updated_timestamp": self.updated_timestamp,
            "created_timestamp": self.created_timestamp,
        }

        if purpose == SerializePurpose.REDIS:
            ret["encrypted_credentials"] = self.encrypted_credentials
            ret["display_credentials"] = self.display_credentials

        elif purpose == SerializePurpose.RESPONSE:
            ret["display_credentials"] = self.display_credentials
            ret["properties"] = self.model_schema().properties

        return ret
