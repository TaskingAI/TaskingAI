from typing import List, Optional
from pydantic import BaseModel, Field, Extra
from app.models import Chunk

__all__ = [
    "ChunkQueryRequest",
    "ChunkQueryResponse",
]


# ----------------------------
# Query Chunks
# GET /collections/{collection_id}/chunks/params
# Request Params: None
# Request JSON Body: ChunkQueryRequest
# Response: ChunkQueryResponse
class ChunkQueryRequest(BaseModel):
    top_k: int = Field(..., ge=1, le=20, description="The number of most relevant chunks to return.", example=3)
    max_tokens: Optional[int] = Field(None, ge=1, description="The maximum number of tokens to return.", example=100)
    query_text: str = Field(
        ...,
        min_length=1,
        max_length=32768,
        description="The query text. Retrieval service will find and return the most relevant chunks to this text.",
        examples=["What is machine learning?"],
    )
    score_threshold: Optional[float] = Field(
        None, ge=0.0, le=1.0, description="The minimum score threshold to return the chunks.", examples=[0.5]
    )

    class Config:
        extra = Extra.forbid


class ChunkQueryResponse(BaseModel):
    status: str = Field(..., description="The response status.", examples=["success"])
    data: List[Chunk] = Field(..., description="The response chunk list data.")
    fetched_count: int = Field(..., ge=0, description="The number of chunks returned in the response.", example=3)
