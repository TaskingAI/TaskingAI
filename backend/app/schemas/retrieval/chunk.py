from pydantic import BaseModel, Field, Extra, field_validator, model_validator
from typing import Dict, Optional
from ..utils import validate_metadata, check_update_keys


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


# ----------------------------
# Create Chunk
# POST /collections/{collection_id}/chunks
class ChunkCreateRequest(BaseModel):
    content: str = Field(
        ...,
        min_length=1,
        max_length=4096,
        description="The record content.",
        examples=["Record content"],
    )

    metadata: Dict[str, str] = Field(
        {},
        min_items=0,
        max_items=16,
        description="The record metadata. "
        "It can store up to 16 key-value pairs where each key's length is less than 64 "
        "and value's length is less than 512.",
        examples=[{}],
    )

    @field_validator("metadata")
    def validate_metadata(cls, metadata: Dict):
        return validate_metadata(metadata)


# ----------------------------
# Update Chunk
# POST /collections/{collection_id}/chunks/{chunk_id}
class ChunkUpdateRequest(BaseModel):
    content: Optional[str] = Field(
        None,
        min_length=1,
        max_length=4096,
        description="The record content.",
        examples=["Record content"],
    )

    metadata: Optional[Dict[str, str]] = Field(
        None,
        min_items=0,
        max_items=16,
        description="The record metadata. "
        "It can store up to 16 key-value pairs where each key's length is less than 64 "
        "and value's length is less than 512.",
        examples=[{}],
    )

    @field_validator("metadata")
    def validate_metadata(cls, metadata: Dict):
        return validate_metadata(metadata)

    @model_validator(mode="before")
    def custom_validate(cls, data: Dict):
        # check at least one field is not None
        check_update_keys(data, ["content", "metadata"])
        return data
