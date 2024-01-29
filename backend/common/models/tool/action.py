from pydantic import BaseModel
from typing import Dict, Optional, List
from .authentication import Authentication, AuthenticationType
from common.utils import generate_random_id
from common.utils import load_json_attr
from common.models import SerializePurpose, ChatCompletionFunction
from common.database.redis import redis_object_pop, redis_object_set_object, redis_object_get_object
from enum import Enum

__all__ = ["Action", "ActionMethod", "ActionParam", "ActionBodyType", "ActionStruct", "action_param_schema_to_dict"]


class ActionMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    # HEAD = "HEAD"
    # OPTIONS = "OPTIONS"
    # TRACE = "TRACE"
    NONE = "NONE"


class ActionBodyType(str, Enum):
    JSON = "JSON"
    FORM = "FORM"
    NONE = "NONE"


class ActionParam(BaseModel):
    type: str
    description: str
    enum: Optional[List[str]] = None
    required: bool

    def is_single_value_enum(self):
        return self.enum and len(self.enum) == 1


class ActionStruct(BaseModel):
    name: str
    description: str
    operation_id: str
    url: str
    method: ActionMethod
    path_param_schema: Optional[Dict[str, ActionParam]]
    query_param_schema: Optional[Dict[str, ActionParam]]
    body_param_schema: Optional[Dict[str, ActionParam]]
    body_type: ActionBodyType
    function_def: ChatCompletionFunction
    openapi_schema: Dict


def action_param_schema_to_dict(param_schema: Optional[Dict[str, ActionParam]]):
    if not param_schema:
        return None

    ret = {}
    for param_name, param in param_schema.items():
        ret[param_name] = param.model_dump(exclude_none=True)

    return ret


class Action(BaseModel):
    action_id: str

    name: str
    operation_id: str
    description: str
    url: str
    method: ActionMethod
    path_param_schema: Optional[Dict[str, ActionParam]]  # name: ActionParam
    query_param_schema: Optional[Dict[str, ActionParam]]
    body_type: ActionBodyType
    body_param_schema: Optional[Dict[str, ActionParam]]

    # function definition for LLM function call
    function_def: ChatCompletionFunction

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
        # load authentication
        authentication_dict = load_json_attr(row, "authentication", default_value={})
        if authentication_dict:
            authentication = Authentication(**authentication_dict)
            authentication.decrypt()
        else:
            authentication = Authentication(type=AuthenticationType.none).model_dump()

        method = row["method"]
        if not method:
            method = ActionMethod.NONE

        body_type = row["body_type"]
        if not body_type:
            body_type = ActionBodyType.NONE

        function_def = load_json_attr(row, "function_def", default_value={})
        if not function_def:
            function_def = {"name": "", "description": "", "parameters": {"properties": {}}}

        return cls(
            action_id=row["action_id"],
            name=row["name"],
            operation_id=row["operation_id"],
            description=row["description"],
            url=row["url"],
            method=method,
            path_param_schema=load_json_attr(row, "path_param_schema", {}),
            query_param_schema=load_json_attr(row, "query_param_schema", {}),
            body_param_schema=load_json_attr(row, "body_param_schema", {}),
            body_type=body_type,
            function_def=function_def,
            openapi_schema=load_json_attr(row, "openapi_schema", {}),
            authentication=authentication,
            updated_timestamp=row["updated_timestamp"],
            created_timestamp=row["created_timestamp"],
        )

    def to_dict(self, purpose: SerializePurpose):
        authentication_dict = self.authentication.model_dump(exclude_none=True)
        authentication_dict.pop("encrypted")

        # compatible with old db version
        method = self.method
        if method == ActionMethod.NONE:
            method = ""

        body_type = self.body_type
        if body_type == ActionBodyType.NONE:
            body_type = ""

        ret = {
            "object": self.object_name(),
            "action_id": self.action_id,
            "name": self.name,
            "operation_id": self.operation_id,
            "description": self.description,
            "url": self.url,
            "method": method,
            "path_param_schema": action_param_schema_to_dict(self.path_param_schema),
            "query_param_schema": action_param_schema_to_dict(self.query_param_schema),
            "body_param_schema": action_param_schema_to_dict(self.body_param_schema),
            "body_type": body_type,
            "function_def": self.function_def.model_dump(),
            "openapi_schema": self.openapi_schema,
            "authentication": authentication_dict,
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
