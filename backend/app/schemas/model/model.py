from pydantic import BaseModel, Field, model_validator, field_validator
from typing import Optional, Any, Dict
from ..utils import check_update_keys
from common.models import ModelType
from common.services.model.model_schema import get_provider
from ..base import BaseListRequest

# ----------------------------
# List Models
# GET /models


class ModelListRequest(BaseListRequest):
    # filter
    type: Optional[ModelType] = Field(default=None, description="The type of the model.")
    provider_id: Optional[str] = Field(
        default=None, min_length=1, max_length=50, description="The provider_id of the model."
    )

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
    properties: Optional[Dict] = Field(default=None, description="The properties of the model.")


# ----------------------------
# Update Model
# POST /models/{model_id}


class ModelUpdateRequest(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=255, description="The name of the model.")
    credentials: Optional[Dict] = Field(default=None, description="The credentials of the model.")
    properties: Optional[Dict] = Field(default=None, description="The properties of the model.")

    @model_validator(mode="before")
    def custom_validate(cls, data: Any):
        check_update_keys(data, ["name", "credentials"])
        return data
