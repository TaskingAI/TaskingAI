from typing import Optional, Any, Dict
from pydantic import BaseModel, Field, model_validator
from app.models import ModelType, ModelFallbackConfig
from ..utils import check_update_keys

__all__ = [
    "ModelCreateRequest",
    "ModelUpdateRequest",
]


# POST /projects/{project_id}/models
class ModelCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=256, description="The name of the model.")
    model_schema_id: str = Field(..., min_length=1, max_length=127, description="The provider_model_id of the model.")
    provider_model_id: Optional[str] = Field(
        None, min_length=1, max_length=255, description="The provider_model_id of the model."
    )
    configs: Optional[Dict[str, Any]] = Field({}, description="The model configurations.")
    type: Optional[ModelType] = Field(None, description="The type of the model.", examples=["text_embedding"])
    credentials: Dict = Field(..., description="The credentials of the model.")
    properties: Optional[Dict] = Field(None, description="The custom model properties.")
    fallbacks: Optional[ModelFallbackConfig] = Field(None, description="The fallback models.")


# POST /projects/{project_id}/models/{model_id}
class ModelUpdateRequest(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=255, description="The name of the model.")
    model_schema_id: Optional[str] = Field(
        None, min_length=1, max_length=127, description="The provider_model_id of the model."
    )
    provider_model_id: Optional[str] = Field(
        None, min_length=1, max_length=255, description="The provider_model_id of the model."
    )
    configs: Optional[Dict[str, Any]] = Field(None, description="The model configurations.")
    type: Optional[ModelType] = Field(None, description="The type of the model.", examples=["text_embedding"])
    credentials: Optional[Dict] = Field(None, description="The credentials of the model.")
    properties: Optional[Dict] = Field(None, description="The custom model properties.")
    fallbacks: Optional[ModelFallbackConfig] = Field(None, description="The fallback models.")

    @model_validator(mode="before")
    def before_custom_validate(cls, data: Any):
        check_update_keys(
            data, ["name", "credentials", "properties", "model_schema_id", "provider_model_id", "type", "configs"]
        )
        return data
