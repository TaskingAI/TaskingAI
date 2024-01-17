from pydantic import BaseModel
from typing import Dict
from .authentication import Authentication, AuthenticationType
from common.utils import generate_random_id
from common.utils import load_json_attr
from common.models import SerializePurpose
from common.database.redis import redis_object_pop, redis_object_set_object, redis_object_get_object

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
        authentication_dict = load_json_attr(row, "authentication", default_value={})
        if authentication_dict:
            authentication = Authentication(**authentication_dict)
            authentication.decrypt()
        else:
            authentication = Authentication(type=AuthenticationType.none).model_dump()

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
        authentication_dict = self.authentication.model_dump(exclude_none=True)
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

    @classmethod
    async def get_redis(cls, action_id: str):
        return await redis_object_get_object(Action, action_id)

    async def set_redis(self):
        await redis_object_set_object(
            Action,
            key=self.action_id,
            value=self.to_dict(purpose=SerializePurpose.REDIS),
        )

    async def pop_redis(self):
        await redis_object_pop(
            Action,
            key=self.action_id,
        )
