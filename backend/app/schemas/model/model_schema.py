from pydantic import BaseModel, Field, model_validator
from typing import Optional, Any
from ..utils import validate_list_cursors

# ----------------------------
# List Model Schemas
# GET /model_schemas


class ModelSchemaListRequest(BaseModel):
    limit: int = Field(20, ge=1, le=100, description="The maximum number of model schemas to return.", examples=[20])

    after: Optional[str] = Field(
        None,
        min_length=8,
        max_length=8,
        description="The cursor represented by a model_schema_id to fetch the next page.",
    )
    before: Optional[str] = Field(
        None,
        min_length=8,
        max_length=8,
        description="The cursor represented by a model_schema_id to fetch the previous page.",
    )
    offset: Optional[int] = Field(
        None,
        ge=0,
        description="The offset of model schemas to return. "
        "Only one in `offset`, `after` and `before` can be used at the same time.",
    )

    # filter
    type: Optional[str] = Field(default=None, min_length=1, max_length=50)
    provider_id: Optional[str] = Field(default=None, min_length=1, max_length=50)

    # after and before cannot be used at the same time
    @model_validator(mode="before")
    def custom_validate(cls, data: Any):
        return validate_list_cursors(data)
