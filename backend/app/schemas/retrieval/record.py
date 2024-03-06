from typing import Optional, Any

from pydantic import BaseModel, Extra, Field
from typing import Dict
from app.models import RecordType, TextSplitter

__all__ = [
    "RecordCreateRequest",
    "RecordUpdateRequest",
]


# ----------------------------
# Create Record
# POST /collections/{collection_id}/records
# Request Params: None
# Request JSON Body: RecordCreateRequest
# Response: RecordCreateResponse
class RecordCreateRequest(BaseModel):
    type: RecordType = Field(
        "text",
        escription="The record type. Currently only `text` is supported.",
    )

    title: str = Field(
        "",
        min_length=0,
        max_length=256,
        description="The record title.",
        examples=["Record title"],
    )

    content: str = Field(
        ...,
        min_length=1,
        max_length=32768,
        description="The record content.",
        examples=["Record content"],
    )

    text_splitter: TextSplitter = Field(
        ...,
        description="The text splitter indicating how to split records into chunks. "
        "It cannot change after creation.",
        examples=[{"type": "token", "chunk_size": 200, "overlap_size": 20}],
    )

    metadata: Dict[str, str] = Field(
        {},
        min_length=0,
        max_length=16,
        description="The record metadata. "
        "It can store up to 16 key-value pairs where each key's length is less than 64 "
        "and value's length is less than 512.",
        examples=[{}],
    )

    class Config:
        extra = Extra.forbid

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        d = super().model_dump(**kwargs)
        d["text_splitter"] = self.text_splitter.model_dump()
        return d


# ----------------------------
# Update Record
# POST /collections/{collection_id}/records/{record_id}
# Request Params: None
# Request JSON Body: RecordUpdateRequest
# Response: RecordUpdateResponse
class RecordUpdateRequest(BaseModel):
    type: Optional[RecordType] = Field(
        None,
        escription="The record type. Currently only `text` is supported.",
    )

    title: Optional[str] = Field(
        None,
        min_length=0,
        max_length=256,
        description="The record title.",
        examples=["Record title"],
    )

    content: Optional[str] = Field(
        None,
        min_length=1,
        max_length=32768,
        description="The record content.",
        examples=["Record content"],
    )

    text_splitter: Optional[TextSplitter] = Field(
        None,
        description="The text splitter indicating how to split records into chunks. "
        "It cannot change after creation.",
        examples=[{"type": "token", "chunk_size": 200, "overlap_size": 20}],
    )

    metadata: Optional[Dict[str, str]] = Field(
        None,
        min_length=0,
        max_length=16,
        description="The record metadata. "
        "It can store up to 16 key-value pairs where each key's length is less than 64 "
        "and value's length is less than 512.",
        examples=[{}],
    )

    class Config:
        extra = Extra.forbid
