from typing import Dict, List, Optional
from enum import Enum
from pydantic import BaseModel
from tkhelper.models import ModelEntity
from tkhelper.utils import generate_random_id, load_json_attr

from .authentication import ActionAuthentication, ActionAuthenticationType
from ..inference.chat_completion_function import ChatCompletionFunction

__all__ = ["Action", "ActionMethod", "ActionBodyType", "ActionStruct", "ActionParam", "EXAMPLE_OPENAPI_SCHEMA"]

EXAMPLE_OPENAPI_SCHEMA = {
    "openapi": "3.1.0",
    "servers": [{"url": "https://www.example.com"}],
    "info": {"title": "My Action", "description": "This is an action."},
    "paths": {
        "/": {
            "get": {
                "operationId": "get_data",
                "description": "The action to get data.",
                "responses": {"200": {"description": "OK"}},
            }
        }
    },
}


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


class Action(ModelEntity):
    action_id: str

    name: str
    operation_id: str
    description: str
    url: str
    method: ActionMethod
    path_param_schema: Optional[Dict[str, ActionParam]]
    query_param_schema: Optional[Dict[str, ActionParam]]
    body_type: ActionBodyType
    body_param_schema: Optional[Dict[str, ActionParam]]

    # function definition for LLM function call
    function_def: ChatCompletionFunction

    openapi_schema: Dict
    authentication: ActionAuthentication

    updated_timestamp: int
    created_timestamp: int

    @staticmethod
    def build(row):
        authentication_dict = load_json_attr(row, "authentication", default_value={})
        if authentication_dict:
            authentication = ActionAuthentication(**authentication_dict)
            authentication.decrypt()
        else:
            authentication = ActionAuthentication(type=ActionAuthenticationType.none).model_dump()

        method = row["method"]
        if not method:
            method = ActionMethod.NONE

        body_type = row["body_type"]
        if not body_type:
            body_type = ActionBodyType.NONE

        return Action(
            action_id=row["action_id"],
            name=row["name"],
            operation_id=row["operation_id"],
            description=row["description"],
            url=row["url"],
            method=method,
            path_param_schema=load_json_attr(row, "path_param_schema", None),
            query_param_schema=load_json_attr(row, "query_param_schema", None),
            body_param_schema=load_json_attr(row, "body_param_schema", None),
            body_type=body_type,
            function_def=load_json_attr(row, "function_def", {}),
            openapi_schema=load_json_attr(row, "openapi_schema", {}),
            authentication=authentication,
            updated_timestamp=row["updated_timestamp"],
            created_timestamp=row["created_timestamp"],
        )

    def to_response_dict(self) -> Dict:
        ret = {
            "object": "Action",
            "action_id": self.action_id,
            "name": self.name,
            "operation_id": self.operation_id,
            "description": self.description,
            "url": self.url,
            "method": self.method.value,
            "path_param_schema": self.path_param_schema,
            "query_param_schema": self.query_param_schema,
            "body_param_schema": self.body_param_schema,
            "body_type": self.body_type,
            "function_def": self.function_def,
            "openapi_schema": self.openapi_schema,
            "authentication": self.authentication.to_display_dict(),
            "updated_timestamp": self.updated_timestamp,
            "created_timestamp": self.created_timestamp,
        }

        return ret

    @staticmethod
    def object_name() -> str:
        return "action"

    @staticmethod
    def object_plural_name() -> str:
        return "actions"

    @staticmethod
    def table_name() -> str:
        return "action"

    @staticmethod
    def id_field_name() -> str:
        return "action_id"

    @staticmethod
    def primary_key_fields() -> List[str]:
        return ["action_id"]

    @staticmethod
    def generate_random_id() -> str:
        return "bFBd" + generate_random_id(20)

    @staticmethod
    def list_prefix_filter_fields() -> List[str]:
        return ["action_id", "name"]

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
        return ["openapi_schema", "authentication"]

    @staticmethod
    def fields_exclude_in_response():
        return []
