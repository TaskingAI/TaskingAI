from pydantic import BaseModel, Field
from app.models import BaseModelProperties, BaseModelPricing

__all__ = [
    "TextEmbeddingModelConfiguration",
    "validate_model_configuration",
    "TextEmbeddingModelProperties",
    "TextEmbeddingModelPricing",
]


class TextEmbeddingModelConfiguration(BaseModel):
    pass
    # todo: add model configuration fields here if needed in the future


def validate_model_configuration(
    provider_id: str,
    provider_model_id: str,
    configs: TextEmbeddingModelConfiguration,
):
    pass


class TextEmbeddingModelProperties(BaseModelProperties):

    embedding_size: int = Field(
        ...,
        ge=1,
        le=2000,
        description="The dimensions of the output embedding vectors. Currently, only dimensions under 2000 are supported.",
    )

    input_token_limit: int = Field(
        512,
        ge=1,
        description="The maximum number of tokens for each text chunk allowed in the input.",
    )

    max_batch_size: int = Field(
        512,
        ge=1,
        description="The maximum number of text chunks that a provider's API can process in one call.",
    )


class TextEmbeddingModelPricing(BaseModelPricing):

    input_token: float = Field(
        ...,
        description="The input token unit price.",
    )

    unit: int = Field(
        ...,
        description="The token number of the unit price.",
    )
