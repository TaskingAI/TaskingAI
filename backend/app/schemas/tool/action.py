from typing import Optional, Any, Dict, List

import openapi_spec_validator
from pydantic import BaseModel, Field, field_validator, model_validator
from app.models import Action, ActionAuthentication, EXAMPLE_OPENAPI_SCHEMA, validate_authentication_data, \
    ActionAuthenticationType

import re

__all__ = [
    "ActionBulkCreateRequest",
    "ActionBulkCreateResponse",
    "ActionUpdateRequest",
    "ActionRunRequest",
    "ActionRunResponse",
]

from tkhelper.error import raise_http_error, ErrorCode


def validate_openapi_schema(schema: Dict, only_one_path_and_method: bool):
    try:
        openapi_spec_validator.validate(schema)
        # check exactly one server in the schema
    except Exception as e:
        if hasattr(e, "message"):
            raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, message=f"Invalid openapi schema: {e.message}")
        else:
            raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, message=f"Invalid openapi schema: {e}")

    if "servers" not in schema:
        raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, message="No server is found in action schema")

    if "paths" not in schema:
        raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, message="No paths is found in action schema")

    if len(schema["servers"]) != 1:
        raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, message="Exactly one server is allowed in action schema")

    if only_one_path_and_method:
        if len(schema["paths"]) != 1:
            raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, message="Only one path is allowed in action schema")
        path = list(schema["paths"].keys())[0]
        if len(schema["paths"][path]) != 1:
            raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, message="Only one method is allowed in action schema")

    # check each path method has a valid description and operationId
    for path, methods in schema["paths"].items():
        for method, details in methods.items():
            if not details.get("description") or not isinstance(details["description"], str):
                if details.get("summary") and isinstance(details["summary"], str):
                    # use summary as its description
                    details["description"] = details["summary"]
                else:
                    raise_http_error(
                        ErrorCode.REQUEST_VALIDATION_ERROR,
                        message=f"No description is found in {method} {path} in action schema",
                    )
            if len(details["description"]) > 512:
                raise_http_error(
                    ErrorCode.REQUEST_VALIDATION_ERROR,
                    message=f"Description cannot be longer than 512 characters in {method} {path} in action schema",
                )

            if not details.get("operationId") or not isinstance(details["operationId"], str):
                raise_http_error(
                    ErrorCode.REQUEST_VALIDATION_ERROR,
                    message=f"No operationId is found in {method} {path} in action schema",
                )
            if len(details["operationId"]) > 128:
                raise_http_error(
                    ErrorCode.REQUEST_VALIDATION_ERROR,
                    message=f"operationId cannot be longer than 128 characters in {method} {path} in action schema",
                )

            if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", details["operationId"]):
                raise_http_error(
                    ErrorCode.REQUEST_VALIDATION_ERROR,
                    message=f'Invalid operationId {details["operationId"]} in {method} {path} in action schema',
                )

    return schema


# ----------------------------
# Create Action
# POST /actions
# Request Params: None
# Request: ActionBulkCreateRequest
# Response: ActionBulkCreateResponse
class ActionBulkCreateRequest(BaseModel):
    openapi_schema: Dict = Field(
        ...,
        description="The action schema is compliant with the OpenAPI Specification. "
                    "If there are multiple paths and methods in the schema, "
                    "the server will create multiple actions whose schema only has exactly one path and one method",
    )

    authentication: ActionAuthentication = Field(
        ActionAuthentication(type=ActionAuthenticationType.none), description="The action API authentication."
    )

    @field_validator("authentication", mode="before")
    def validate_authentication(cls, data: Dict):
        return validate_authentication_data(data)

    @field_validator("openapi_schema")
    def validate_schema(cls, openapi_schema: Dict):
        return validate_openapi_schema(openapi_schema, only_one_path_and_method=False)

    @model_validator(mode="after")
    def validate(cls, data: Any):
        data.authentication.encrypt()
        return data


class ActionBulkCreateResponse(BaseModel):
    status: str = Field("success", Literal="success", description="The response status.", examples=["success"])
    data: List[Action] = Field(..., description="The created actions.")

class ActionUpdateRequest(BaseModel):
    openapi_schema: Optional[Dict] = Field(
        default=None,
        description="The action schema, which is compliant with the OpenAPI Specification. "
        "It should only have exactly one path and one method.",
    )
    authentication: Optional[ActionAuthentication] = Field(None, description="The action API authentication.")

    @field_validator("openapi_schema")
    def validate_schema(cls, schema: Dict):
        return validate_openapi_schema(schema, only_one_path_and_method=True)

    @field_validator("authentication", mode="before")
    def validate_authentication(cls, data: Dict):
        return validate_authentication_data(data)

    @model_validator(mode="after")
    def validate(cls, data: Any):
        if data.authentication is not None:
            data.authentication.encrypt()
        return data

# ----------------------------
# Run an Action
# POST /actions/{action_id}/run
# Request Params: None
# Request JSON Body: ActionRunRequest
# Response: ActionRunResponse


class ActionRunRequest(BaseModel):
    parameters: Optional[Dict[str, Any]] = Field(None)


class ActionRunResponse(BaseModel):
    status: str = Field("success", Literal="success", description="The response status.", examples=["success"])
    data: Dict = Field(..., description="The action API response data.")
