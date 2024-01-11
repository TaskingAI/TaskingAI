from typing import Optional
from pydantic import BaseModel, Field, model_validator, field_validator
from typing import Any, List, Dict
from .utils import check_update_keys, validate_identifier, validate_list_position_condition
from enum import Enum
from .base import SortOrderEnum

# ----------------------------


class SortFieldEnum(str, Enum):
    created_timestamp = "created_timestamp"


# The Function Parameter Property
# class ParameterProperty(BaseModel):
#     type: str = Field(..., description="The object type, which should be one of `string`, `number`, `integer`, `boolean`, `array` and `object`.")
#     description: Optional[str] = Field(None, min_length=0, max_length=512, description="The function description")


# The Function Parameter Schema
class Parameters(BaseModel):
    type: str = Field("object", pattern="object", description="The object type, which is always `object`.")
    properties: Dict[str, Any] = Field({}, description="The properties of the function parameter schema.")
    required: List[str] = Field([], description="The required properties of the function parameter schema.")

    # todo: add validation for properties and required


# GET /projects/{project_id}/functions/list
class FunctionListRequest(BaseModel):
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


class FunctionCreateRequest(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=256,
        description='A meaningful function name, consists of letters, digits and underscore "_" and its first character cannot be a digit.',
    )
    description: str = Field(..., min_length=1, max_length=512, description="The function description.")
    parameters: Parameters = Field(..., description="The action parameter schema.")  # todo add learn more link
    max_count: int = Field(..., description="The maximum number of functions can be created in the project.")

    @field_validator("name")
    def validate_name(cls, name: str):
        return validate_identifier(name)


class FunctionUpdateRequest(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=256,
        description='A meaningful function name, consists of letters, digits and underscore "_" and its first character cannot be a digit.',
    )
    description: Optional[str] = Field(None, min_length=1, max_length=512, description="The function description.")
    parameters: Optional[Parameters] = Field(
        None, description="The action parameter schema."
    )  # todo add learn more link

    @model_validator(mode="before")
    def validate_all_fields_at_the_same_time(cls, data: Any):
        keys = ["name", "description", "parameters"]
        check_update_keys(data, keys)
        return data

    @field_validator("name")
    def validate_name(cls, name: str):
        return validate_identifier(name)
