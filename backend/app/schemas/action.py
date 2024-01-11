from typing import Optional
from pydantic import BaseModel, Field, model_validator, field_validator
from typing import Any, Dict
from .utils import check_update_keys, validate_openapi_schema, validate_list_position_condition
from enum import Enum
from .base import SortOrderEnum
from common.models import Authentication, AuthenticationType

# ----------------------------


class SortFieldEnum(str, Enum):
    created_timestamp = "created_timestamp"


# GET /projects/{project_id}/actions/list
class ActionListRequest(BaseModel):
    limit: int = Field(20, ge=1, le=100)

    sort_field: SortFieldEnum = Field(
        default=SortFieldEnum.created_timestamp, description="The field to sort records by."
    )
    order: SortOrderEnum = Field(default=SortOrderEnum.desc)

    after: Optional[str] = Field(None, min_length=20, max_length=30)
    before: Optional[str] = Field(None, min_length=20, max_length=30)
    offset: Optional[int] = Field(None, ge=0)

    id_search: Optional[str] = Field(None, min_length=1, max_length=256, description="The action ID to search for.")
    name_search: Optional[str] = Field(None, min_length=1, max_length=256, description="The action name to search for.")

    # after and before cannot be used at the same time
    @model_validator(mode="before")
    def validate_all_fields_at_the_same_time(cls, data: Any):
        return validate_list_position_condition(data)


class ActionBulkCreateRequest(BaseModel):
    schema: Dict = Field(
        ...,
        description="The action schema is compliant with the OpenAPI Specification. If there are multiple paths and methods in the schema, the service will create multiple actions whose schema only has exactly one path and one method",
    )
    authentication: Authentication = Field(
        Authentication(type=AuthenticationType.none), description="The action API authentication."
    )
    max_count: int = Field(..., description="The maximum number of actions can be created in the project.")

    @field_validator("schema")
    def validate_schema(cls, schema: Dict):
        validated_schema = validate_openapi_schema(schema, only_one_path_and_method=False)
        return validated_schema

    @model_validator(mode="after")
    def validate(cls, data: Any):
        data.authentication.encrypt()
        return data


class ActionUpdateRequest(BaseModel):
    schema: Optional[Dict] = Field(None)
    authentication: Optional[Authentication] = Field(None)

    @model_validator(mode="before")
    def validate_all_fields_at_the_same_time(cls, data: Any):
        keys = ["schema", "authentication"]
        check_update_keys(data, keys)
        return data

    @field_validator("schema")
    def validate_schema(cls, schema: Dict):
        return validate_openapi_schema(schema, only_one_path_and_method=True)

    @model_validator(mode="after")
    def validate(cls, data: Any):
        if data.authentication:
            data.authentication.encrypt()
        return data


class ActionRunRequest(BaseModel):
    parameters: Optional[Dict[str, Any]] = Field(None)
    extra_headers: Optional[Dict[str, Any]] = Field(None)
