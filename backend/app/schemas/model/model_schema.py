from pydantic import BaseModel, Field
from typing import Optional

# ----------------------------
# List Model Schemas
# GET /model_schemas


class ModelSchemaListRequest(BaseModel):
    limit: int = Field(20, ge=1, le=100, description="The maximum number of model schemas to return.", examples=[20])

    offset: int = Field(0, ge=0, description="The offset of model schemas to return. ")

    # filter
    type: Optional[str] = Field(default=None, min_length=1, max_length=50)
    provider_id: Optional[str] = Field(default=None, min_length=1, max_length=50)


class ModelSchemaGetRequest(BaseModel):
    model_schema_id: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="The model schema ID.",
        examples=["openai/gpt-4"],
    )


class ProviderGetRequest(BaseModel):
    provider_id: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="The provider ID.",
        examples=["openai"],
    )
