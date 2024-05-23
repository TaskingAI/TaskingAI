from typing import Optional, Dict
from pydantic import BaseModel, Field
from app.models import ModelType


class VerifyModelCredentialsSchema(BaseModel):

    model_schema_id: str = Field(
        ...,
        min_length=1,
        max_length=127,
        description="The ID of the model schema.",
        examples=["openai/gpt-4"],
    )

    provider_model_id: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="The provider's model ID.",
    )

    properties: Optional[Dict] = Field(
        None,
        description="The custom model properties.",
    )

    configs: Optional[Dict] = Field(
        None,
        description="The model configurations.",
    )

    model_type: Optional[ModelType] = Field(
        None,
        description="The type of the model.",
        examples=["chat_completion"],
    )

    credentials: Optional[Dict] = Field(
        None,
        description="The credentials of the model provider to be verified. "
        "Only one of credentials or encrypted_credentials is required.",
    )

    encrypted_credentials: Optional[Dict] = Field(
        None,
        description="The encrypted credentials of the model provider to be verified.",
        examples=[None],
    )
