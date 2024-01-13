from pydantic import BaseModel, Field, model_validator, field_validator
from typing import Optional, Any, Dict
from ..utils import validate_list_cursors, check_update_keys
from common.models import ModelType, SortOrderEnum
from common.services.model.model_schema import get_provider

# ----------------------------
# List Models
# GET /models


class ModelListRequest(BaseModel):
    limit: int = Field(20, ge=1, le=100, description="The maximum number of models to return.", examples=[20])

    # todo: add different sort field options

    order: SortOrderEnum = Field(SortOrderEnum.DESC, description="The order to return. It can be `asc` or `desc`.")

    after: Optional[str] = Field(
        None, min_length=8, max_length=8, description="The cursor represented by a model_id to fetch the next page."
    )
    before: Optional[str] = Field(
        None, min_length=8, max_length=8, description="The cursor represented by a model_id to fetch the previous page."
    )
    offset: Optional[int] = Field(
        None,
        ge=0,
        description="The offset of models to return. "
        "Only one in `offset`, `after` and `before` can be used at the same time.",
    )

    id_search: Optional[str] = Field(None, min_length=1, max_length=256, description="The model ID to search for.")
    name_search: Optional[str] = Field(None, min_length=1, max_length=256, description="The record name to search for.")

    # filter
    type: Optional[ModelType] = Field(default=None, description="The type of the model.")
    provider_id: Optional[str] = Field(
        default=None, min_length=1, max_length=50, description="The provider_id of the model."
    )

    # after and before cannot be used at the same time
    @model_validator(mode="before")
    def custom_validate(cls, data: Any):
        return validate_list_cursors(data)

    @field_validator("provider_id")
    def validate_provider_id(cls, provider_id: str):
        if provider_id:
            if not get_provider(provider_id):
                raise ValueError(f"Provider {provider_id} does not exist.")
        return provider_id


# ----------------------------
# Create Model
# POST /models


class ModelCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=256, description="The name of the model.")
    model_schema_id: str = Field(..., min_length=1, max_length=50, description="The provider_model_id of the model.")
    credentials: Dict = Field(default=None, description="The credentials of the model.")


# ----------------------------
# Update Model
# POST /models/{model_id}


class ModelUpdateRequest(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=255, description="The name of the model.")
    credentials: Optional[Dict] = Field(default=None, description="The credentials of the model.")

    @model_validator(mode="before")
    def custom_validate(cls, data: Any):
        check_update_keys(data, ["name", "credentials"])
        return data
