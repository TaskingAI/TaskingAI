from typing import Optional, List
from pydantic import BaseModel, Field
from app.models import RerankResult, RerankUsage

__all__ = [
    "RerankRequest",
    "RerankResponse",
]


# Text Embedding
# POST /v1/rerank
# Request Params: None
# Request: RerankRequest
# Response: ChatCompletionResponse
class RerankRequest(BaseModel):
    model_id: str = Field(..., min_length=8, max_length=8, description="The rerank model id.", examples=["abcdefgh"])
    query: str = Field(
        ..., description="The query text for reranking.", examples=["Organic skincare products for sensitive skin"]
    )
    documents: List[str] = Field(
        ..., description="A list of documents to be reranked.", examples=["Eco-friendly kitchenware for modern homes"]
    )
    top_n: int = Field(..., description="The number of top results to return.", examples=[3])


class RerankResponse(BaseModel):
    status: str = Field("success", Literal="success", description="The response status.", examples=["success"])
    data: RerankResult = Field(..., description="The rerank response data.")
    usage: Optional[RerankUsage] = Field(..., description="The rerank usage data.")
