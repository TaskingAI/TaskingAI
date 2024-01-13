from typing import Optional
from pydantic import BaseModel, Field, model_validator, field_validator, Extra
from typing import Any, Dict
from ..utils import validate_metadata, validate_list_cursors
from common.models import SortOrderEnum, RecordType


# ----------------------------
# List Record
# GET /collections/{collection_id}/records
class RecordListRequest(BaseModel):
    limit: int = Field(20, ge=1, le=100, description="The maximum number of records to return.", examples=[20])

    # todo: add different sort field options
    order: Optional[SortOrderEnum] = Field(
        SortOrderEnum.DESC,
        description="The order of records to return, `asc` for ascending and `desc` for descending.",
        examples=["desc"],
    )

    after: Optional[str] = Field(
        None,
        min_length=24,
        max_length=24,
        description="The cursor represented by a record_id to fetch the next page of records.",
    )
    before: Optional[str] = Field(
        None,
        min_length=24,
        max_length=24,
        description="The cursor represented by a record_id to fetch the previous page of records.",
    )
    offset: Optional[int] = Field(
        None,
        ge=0,
        description="The offset of records to return. "
        "Only one in `offset`, `after` and `before` can be used at the same time.",
    )

    id_search: Optional[str] = Field(None, min_length=1, max_length=256, description="The record ID to search for.")
    name_search: Optional[str] = Field(None, min_length=1, max_length=256, description="The record name to search for.")

    class Config:
        extra = Extra.forbid

    # after and before cannot be used at the same time
    @model_validator(mode="before")
    def custom_validate(cls, data: Any):
        return validate_list_cursors(data)


# ----------------------------
# Create Record
# POST /collections/{collection_id}/records
class RecordCreateRequest(BaseModel):
    type: RecordType = Field(
        RecordType.TEXT,
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

    metadata: Dict[str, str] = Field(
        {},
        min_items=0,
        max_items=16,
        description="The record metadata. "
        "It can store up to 16 key-value pairs where each key's length is less than 64 "
        "and value's length is less than 512.",
        examples=[{}],
    )

    class Config:
        extra = Extra.forbid

    @field_validator("metadata")
    def validate_metadata(cls, metadata: Dict):
        return validate_metadata(metadata)


# ----------------------------
# Update Record
# POST /collections/{collection_id}/records/{record_id}
class RecordUpdateRequest(BaseModel):
    metadata: Dict[str, str] = Field(
        ...,
        min_items=0,
        max_items=16,
        description="The record metadata. "
        "It can store up to 16 key-value pairs where each key's length is less than 64 "
        "and value's length is less than 512.",
        examples=[{}],
    )

    class Config:
        extra = Extra.forbid

    @field_validator("metadata")
    def validate_metadata(cls, metadata: Dict):
        return validate_metadata(metadata)
