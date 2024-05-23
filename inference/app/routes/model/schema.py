from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict
from app.models import ModelType
from app.cache import get_provider


# ----------------------------
# List providers
# GET /providers


class ProviderListResponse(BaseModel):
    status: str = Field(
        "success",
        Literal="success",
        description="The status of the response.",
    )
    data: List[Dict] = Field(
        ...,
        description="The list of providers.",
        examples=[
            [
                {
                    "object": "Provider",
                    "provider_id": "anthropic",
                    "credentials_schema": {
                        "type": "object",
                        "properties": {
                            "ANTHROPIC_API_KEY": {
                                "type": "string",
                                "description": "Your Anthropic API Key for authentication.",
                                "secret": True,
                            },
                            "ANTHROPIC_API_VERSION": {
                                "type": "string",
                                "description": "The version of the Anthropic API being used.",
                            },
                        },
                        "required": ["ANTHROPIC_API_KEY"],
                    },
                    "name": "Anthropic",
                }
            ]
        ],
    )
    lang: str = Field(
        "en",
        description="The language code of the response.",
        examples=["en"],
    )


# ----------------------------
# List Model Schemas
# GET /model_schemas
class ModelSchemaListRequest(BaseModel):

    # filter
    type: Optional[ModelType] = Field(
        None,
        min_length=1,
        max_length=50,
        description="The type of the model.",
        examples=["chat_completion", "text_embedding"],
    )
    provider_id: Optional[str] = Field(
        None,
        min_length=1,
        max_length=50,
        description="The model's provider id.",
        examples=["anthropic"],
    )
    lang: str = Field(
        "en",
        description="The language code of the response.",
        examples=["en"],
    )

    @field_validator("provider_id", mode="before")
    def validate_provider_id(cls, provider_id: str):
        if provider_id:
            if not get_provider(provider_id):
                raise ValueError(f"provider {provider_id} does not exist.")
        return provider_id


class ModelSchemaListResponse(BaseModel):
    status: str = Field(
        "success",
        Literal="success",
        description="The status of the response.",
    )
    data: List[Dict] = Field(
        ...,
        description="The list of model schemas.",
        examples=[
            [
                {
                    "object": "ModelSchema",
                    "model_schema_id": "anthropic/claude-2.0",
                    "name": "Claude 2.0",
                    "description": "",
                    "provider_id": "anthropic",
                    "provider_model_id": "claude-2.0",
                    "type": "chat_completion",
                    "properties": {
                        "function_call": False,
                        "streaming": True,
                    },
                }
            ]
        ],
    )


class ModelSchemaGetRequest(BaseModel):
    model_schema_id: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="The model schema ID.",
        examples=["openai/gpt-4"],
    )
    lang: str = Field(
        "en",
        description="The language code of the response.",
        examples=["en"],
    )


class ProviderListRequest(BaseModel):

    lang: str = Field(
        "en",
        description="The language code of the response.",
        examples=["en"],
    )


class ProviderGetRequest(BaseModel):
    provider_id: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="The provider ID.",
        examples=["openai"],
    )
    lang: str = Field(
        "en",
        description="The language code of the response.",
        examples=["en"],
    )
