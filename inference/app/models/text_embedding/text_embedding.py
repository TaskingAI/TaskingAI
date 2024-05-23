from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum

__all__ = [
    "TextEmbeddingInputType",
    "TextEmbeddingOutput",
    "TextEmbeddingResult",
    "TextEmbeddingUsage",
]


class TextEmbeddingUsage(BaseModel):
    input_tokens: int = Field(
        ...,
        description="The number of tokens in the input.",
    )


class TextEmbeddingInputType(str, Enum):
    document = "document"
    query = "query"


class TextEmbeddingOutput(BaseModel):
    index: int
    embedding: List[float]


class TextEmbeddingResult(BaseModel):
    data: List[TextEmbeddingOutput]
    usage: Optional[TextEmbeddingUsage] = Field(
        None,
        description="The token usage of the response.",
    )
