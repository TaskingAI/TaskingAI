import json
from pydantic import BaseModel
from typing import Dict
from .authentication import Authentication, AuthenticationType
from common.utils import generate_random_id
from common.utils import load_json_attr
from common.models import SerializePurpose

__all__ = ["Action"]


class Action(BaseModel):
    action_id: str
    name: str
    description: str
    openapi_schema: Dict
    authentication: Authentication
    updated_timestamp: int
    created_timestamp: int

    @staticmethod
    def object_name():
        return "Action"

    @staticmethod
    def generate_random_id():
        return "bFBd" + generate_random_id(20)

    @classmethod
    def build(cls, row: Dict):
        # laod authentication
        authentication_dict = (
            json.loads(row["authentication"])
            if row["authentication"]
            else Authentication(type=AuthenticationType.none).model_dump()
        )

        authentication = None
        if authentication_dict:
            authentication = Authentication(**authentication_dict)
            authentication.decrypt()

        return cls(
            action_id=row["action_id"],
            name=row["name"],
            description=row["description"],
            openapi_schema=load_json_attr(row, "openapi_schema", default_value={}),
            authentication=authentication,
            updated_timestamp=row["updated_timestamp"],
            created_timestamp=row["created_timestamp"],
        )

    def to_dict(self, purpose: SerializePurpose):
        authentication_dict = self.authentication.model_dump()
        authentication_dict.pop("encrypted")

        ret = {
            "object": self.object_name(),
            "action_id": self.action_id,
            "name": self.name,
            "description": self.description,
            "authentication": authentication_dict,
            "openapi_schema": self.openapi_schema,
            "updated_timestamp": self.updated_timestamp,
            "created_timestamp": self.created_timestamp,
        }

        return ret
