from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from app.models.rerank import *


class RerankRequest(BaseModel):
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

    query: str = Field(
        ...,
        description="The query text for reranking.",
        examples=["Organic skincare products for sensitive skin"],
    )

    documents: List[str] = Field(
        ...,
        description="A list of documents to be reranked.",
        examples=[
            "Eco-friendly kitchenware for modern homes",
            "Biodegradable cleaning supplies for eco-conscious consumers",
            "Organic cotton baby clothes for sensitive skin",
        ],
    )

    top_n: int = Field(
        ...,
        description="The number of top results to return.",
        examples=[3],
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


class RerankResponse(BaseModel):
    status: str = Field(
        "success",
        Literal="success",
        description="The status of the response.",
    )

    data: RerankResult = Field(
        ...,
        description="The data of the response.",
        examples=[
            {
                "results": [
                    {
                        "index": 3,
                        "document": {"text": "Natural organic skincare range for sensitive skin"},
                        "relevance_score": 0.8292155861854553,
                    },
                    {
                        "index": 2,
                        "document": {"text": "Organic cotton baby clothes for sensitive skin"},
                        "relevance_score": 0.14426936209201813,
                    },
                    {
                        "index": 6,
                        "document": {"text": "Sensitive skin-friendly facial cleansers and toners"},
                        "relevance_score": 0.13857832551002502,
                    },
                ]
            }
        ],
    )

    usage: Optional[RerankUsage] = Field(
        ...,
        description="The usage details of the rerank model.",
    )
