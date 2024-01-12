from pydantic import BaseModel, Field, Extra


# ----------------------------
# Query Chunks
# GET /collections/{collection_id}/chunks/query
class ChunkQueryRequest(BaseModel):
    top_k: int = Field(..., ge=1, le=20, description="The number of most relevant chunks to return.", example=3)

    query_text: str = Field(
        ...,
        min_length=1,
        max_length=32768,
        description="The query text. Retrieval service will find and return the most relevant chunks to this text.",
        example="This is a query text.",
    )

    class Config:
        extra = Extra.forbid
