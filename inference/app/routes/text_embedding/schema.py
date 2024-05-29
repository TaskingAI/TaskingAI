from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field
from app.models.text_embedding import *


class TextEmbeddingFallback(BaseModel):
    model_schema_id: str = Field(
        ...,
        min_length=1,
        max_length=127,
        description="The ID of the model schema.",
        examples=["openai/text-embedding-ada-002"],
    )

    provider_model_id: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="The provider's model ID.",
    )


class TextEmbeddingRequest(BaseModel):
    model_schema_id: str = Field(
        ...,
        min_length=1,
        max_length=127,
        description="The id of the model schema.",
        examples=["openai/gpt-4"],
    )

    provider_model_id: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="The provider's model ID.",
    )

    fallbacks: Optional[List[TextEmbeddingFallback]] = Field(
        None,
        description="A list of fallback completions to use if the model fails to generate a response.",
        examples=[None],
    )

    input: Union[str, List[str]] = Field(
        ...,
        description="An input text or a list of input text.",
        examples=[
            "This is a text to be embedded.",
            [
                "This is a text to be embedded.",
                "This is another text to be embedded.",
            ],
        ],
    )

    proxy: Optional[str] = Field(None, description="The proxy of the model.")

    custom_headers: Optional[Dict[str, str]] = Field(
        None,
        min_items=0,
        max_items=16,
        description="The custom headers can store up to 16 key-value pairs where each key's "
        "length is less than 64 and value's length is less than 512.",
        examples=[{"key1": "value1"}, {"key2": "value2"}],
    )

    credentials: Optional[Dict] = Field(
        None,
        description="The credentials of the model provider. "
        "Only one of credentials or encrypted_credentials is required.",
        examples=[{"OPENAI_API_KEY": "YOUR_OPENAI_API_KEY"}],
    )

    encrypted_credentials: Optional[Dict] = Field(
        None,
        description="The encrypted credentials of the model provider.",
        examples=[None],
    )

    properties: Optional[Dict] = Field(
        None,
        description="The custom text embedding model properties.",
        examples=[None],
    )

    configs: TextEmbeddingModelConfiguration = Field(
        TextEmbeddingModelConfiguration(),
        description="Additional configuration to make the chat completion inference.",
        examples=[{}],
    )

    input_type: Optional[TextEmbeddingInputType] = Field(
        None,
        examples=["document", "query"],
    )


class TextEmbeddingResponse(BaseModel):
    status: str = Field(
        "success",
        Literal="success",
        description="The status of the response.",
    )

    data: List[TextEmbeddingOutput] = Field(
        ...,
        description="The data of the response.",
        examples=[
            [
                {
                    "index": 0,
                    "embedding": [
                        0.123,
                        0.456,
                        0.789,
                    ],
                },
                {
                    "index": 1,
                    "embedding": [
                        0.123,
                        0.456,
                        0.789,
                    ],
                },
            ]
        ],
    )

    usage: Optional[TextEmbeddingUsage] = Field(
        ...,
        description="The token usage of the response.",
    )

    fallback_index: Optional[int] = Field(
        None,
        description="The index of the fallback model used.",
    )
