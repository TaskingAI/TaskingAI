from pydantic import BaseModel, Field, model_validator
from typing import Dict, Optional, Any
from app.models import ModelType
from ..utils import check_update_keys

__all__ = [
    "ModelCreateRequest",
    "ModelUpdateRequest",
]


# POST /projects/{project_id}/models/create
class ModelCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=256, description="The name of the model.")
    model_schema_id: str = Field(..., min_length=1, max_length=127, description="The provider_model_id of the model.")
    provider_model_id: Optional[str] = Field(
        None, min_length=1, max_length=255, description="The provider_model_id of the model."
    )
    type: Optional[ModelType] = Field(None, description="The type of the model.", examples=["text_embedding"])
    credentials: Dict = Field(..., description="The credentials of the model.")
    properties: Optional[Dict] = Field(None, description="The custom model properties.")


# POST /projects/{project_id}/models/update
class ModelUpdateRequest(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=255, description="The name of the model.")

    model_schema_id: Optional[str] = Field(
        None, min_length=1, max_length=127, description="The provider_model_id of the model."
    )
    provider_model_id: Optional[str] = Field(
        None, min_length=1, max_length=255, description="The provider_model_id of the model."
    )
    type: Optional[ModelType] = Field(None, description="The type of the model.", examples=["text_embedding"])
    credentials: Optional[Dict] = Field(None, description="The credentials of the model.")
    properties: Optional[Dict] = Field(None, description="The custom model properties.")

    @model_validator(mode="before")
    def custom_validate(cls, data: Any):
        check_update_keys(data, ["name", "credentials"])

        model_schema_id_exist = data.get("model_schema_id") is not None
        provider_model_id_exist = data.get("provider_model_id") is not None
        model_type_exist = data.get("model_type") is not None
        credentials_exist = data.get("credentials") is not None
        properties_exist = data.get("properties") is not None

        if model_schema_id_exist and not credentials_exist:
            raise ValueError("model_schema_id and credentials must be updated together.")

        if provider_model_id_exist and not credentials_exist:
            raise ValueError("provider_model_id can only be updated with credentials.")

        if model_type_exist and not credentials_exist:
            raise ValueError("model_type can only be updated with credentials.")

        if properties_exist and not credentials_exist:
            raise ValueError("properties can only be updated with credentials.")

        return data
