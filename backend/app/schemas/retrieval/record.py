from typing import Optional
from pydantic import BaseModel, Field, model_validator, field_validator, Extra
from typing import Dict
from ..utils import validate_metadata, validate_list_cursors, check_update_keys
from common.models import SortOrderEnum, RecordType
from common.models import TextSplitter, build_text_splitter


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

    class Config:
        extra = Extra.forbid

    # after and before cannot be used at the same time
    @model_validator(mode="before")
    def custom_validate(cls, data: Dict):
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

    text_splitter: TextSplitter = Field(
        ...,
        description="The text splitter indicating how to split records into chunks. "
        "It cannot change after creation.",
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

    @field_validator("text_splitter", mode="before")
    def validate_text_splitter(cls, text_splitter_dict: Dict):
        text_splitter = build_text_splitter(text_splitter_dict)
        if text_splitter is None:
            raise ValueError("Invalid text splitter.")
        return text_splitter

    class Config:
        extra = Extra.forbid

    @field_validator("metadata")
    def validate_metadata(cls, metadata: Dict):
        return validate_metadata(metadata)


# ----------------------------
# Update Record
# POST /collections/{collection_id}/records/{record_id}
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

    @field_validator("text_splitter", mode="before")
    def validate_text_splitter(cls, text_splitter_dict: Dict):
        text_splitter = build_text_splitter(text_splitter_dict)
        if text_splitter is None:
            raise ValueError("Invalid text splitter.")
        return text_splitter

    class Config:
        extra = Extra.forbid

    @field_validator("metadata")
    def validate_metadata(cls, metadata: Dict):
        return validate_metadata(metadata)

    @model_validator(mode="before")
    def custom_validate(cls, data: Dict):
        # check at least one field is not None
        check_update_keys(data, ["title", "content", "metadata"])

        if data.get("text_splitter") is not None and data.get("content") is None:
            raise ValueError("Cannot use text splitter without updating content.")

        if data.get("content") is not None and data.get("text_splitter") is None:
            raise ValueError("Cannot update content without specifying text splitter.")

        if data.get("type") is not None and data.get("content") is None:
            raise ValueError("Cannot update type without updating content.")

        return data
