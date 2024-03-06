from typing import Optional, Any, Dict, List
from pydantic import BaseModel, Field
from app.models import Action, ActionAuthentication, EXAMPLE_OPENAPI_SCHEMA

__all__ = [
    "ActionBulkCreateRequest",
    "ActionBulkCreateResponse",
    "ActionRunRequest",
    "ActionRunResponse",
]


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
        "If there are multiple paths and methods in the schema, the service will create multiple actions whose schema only has exactly one path and one method",
        examples=[EXAMPLE_OPENAPI_SCHEMA],
    )
    authentication: ActionAuthentication = Field(..., description="The action API authentication.")


class ActionBulkCreateResponse(BaseModel):
    status: str = Field("success", Literal="success", description="The response status.", examples=["success"])
    data: List[Action] = Field(..., description="The created actions.")


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
