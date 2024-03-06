from typing import Optional, List, Union
from pydantic import BaseModel, Field, Extra
from app.models import TextEmbeddingInputType, TextEmbeddingOutput

__all__ = [
    "TextEmbeddingRequest",
    "TextEmbeddingResponse",
]


# Text Embedding
# POST /v1/text_embedding
# Request Params: None
# Request: TextEmbeddingRequest
# Response: ChatCompletionResponse
class TextEmbeddingRequest(BaseModel):
    model_id: str = Field(
        ..., min_length=8, max_length=8, description="The text embedding model id.", examples=["abcdefgh"]
    )
    input: Union[str, List[str]] = Field(
        ..., description="The input text or a list of input texts.", examples=["Hello!", ["Hello!", "How are you?"]]
    )
    input_type: Optional[TextEmbeddingInputType] = Field(None, description="The input type.", examples=["text"])

    class Config:
        extra = Extra.forbid


class TextEmbeddingResponse(BaseModel):
    status: str = Field("success", Literal="success", description="The response status.", examples=["success"])
    data: List[TextEmbeddingOutput] = Field(..., description="The text embedding response data.")
