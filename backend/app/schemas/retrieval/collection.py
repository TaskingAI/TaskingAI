from typing import Optional
from pydantic import BaseModel, Field, model_validator, field_validator, Extra
from typing import Any, Dict
from ..utils import check_update_keys, validate_metadata, validate_list_cursors
from common.models import SortOrderEnum, TextSplitter, build_text_splitter
from common.error import raise_http_error, ErrorCode


# ----------------------------
# List Collection
# GET /collections
class CollectionListRequest(BaseModel):
    limit: int = Field(20, ge=1, le=100, description="The maximum number of collections to return.", examples=[20])

    # todo: add different sort field options
    order: Optional[SortOrderEnum] = Field(
        SortOrderEnum.DESC,
        description="The order of collections to return, `asc` for ascending and `desc` for descending.",
        examples=["desc"],
    )

    after: Optional[str] = Field(
        None,
        min_length=24,
        max_length=24,
        description="The cursor represented by a collection_id to fetch the next page of collections.",
    )
    before: Optional[str] = Field(
        None,
        min_length=24,
        max_length=24,
        description="The cursor represented by a collection_id to fetch the previous page of collections.",
    )
    offset: Optional[int] = Field(
        None,
        ge=0,
        description="The offset of collections to return. "
        "Only one in `offset`, `after` and `before` can be used at the same time.",
    )

    id_search: Optional[str] = Field(None, min_length=1, max_length=256, description="The collection ID to search for.")
    name_search: Optional[str] = Field(
        None, min_length=1, max_length=256, description="The collection name to search for."
    )

    class Config:
        extra = Extra.forbid

    # after and before cannot be used at the same time
    @model_validator(mode="before")
    def custom_validate(cls, data: Any):
        return validate_list_cursors(data)


# ----------------------------
# Create Collection
# POST /collections
class CollectionCreateRequest(BaseModel):
    capacity: int = Field(
        1000,
        description="The collection capacity. "
        "Currently only 1000 is supported and we'll provide more options in the future.",
        examples=[1000],
    )
    embedding_model_id: str = Field(
        ...,
        min_length=8,
        max_length=8,
        description="The ID of an available text embedding model in your project.",
        examples=["abcdefgh"],
    )
    name: str = Field("", min_length=0, max_length=256, description="The collection name", example="My Collection")

    description: str = Field(
        "",
        min_length=0,
        max_length=512,
        description="The collection description",
        example="A collection of project documents.",
    )

    text_splitter: TextSplitter = Field(
        None,
        description="The text splitter indicating how to split records into chunks. "
        "It cannot change after creation.",
    )

    metadata: Dict[str, str] = Field(
        {},
        min_items=0,
        max_items=16,
        description="The collection metadata. "
        "It can store up to 16 key-value pairs where each key's length is less than 64 "
        "and value's length is less than 512.",
        examples=[{}],
    )

    @field_validator("metadata")
    def validate_metadata(cls, metadata):
        return validate_metadata(metadata)

    @field_validator("capacity")
    def validate_capacity(cls, capacity):
        if capacity not in [1000]:
            raise ValueError(
                "Currently only capacity of 1000 is supported " "and we will support more options in the future."
            )
        return capacity

    @field_validator("text_splitter", mode="before")
    def validate_text_splitter(cls, text_splitter_dict: Dict):
        text_splitter = build_text_splitter(text_splitter_dict)
        if text_splitter is None:
            raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, "Invalid text splitter.")
        return text_splitter

    class Config:
        extra = Extra.forbid


# ----------------------------
# Update Collection
# POST /collections/{collection_id}
class CollectionUpdateRequest(BaseModel):
    name: Optional[str] = Field(
        None, min_length=0, max_length=256, description="The collection name", example="My Collection"
    )

    description: Optional[str] = Field(
        None,
        min_length=0,
        max_length=512,
        description="The collection description",
        example="A collection of project documents.",
    )

    metadata: Optional[Dict[str, str]] = Field(
        None,
        min_items=0,
        max_items=16,
        description="The collection metadata. "
        "It can store up to 16 key-value pairs where each key's length is less than 64 "
        "and value's length is less than 512.",
        examples=[{}],
    )

    class Config:
        extra = Extra.forbid

    @field_validator("metadata")
    def validate_metadata(cls, metadata):
        return validate_metadata(metadata)

    @model_validator(mode="before")
    def validate_all_fields_at_the_same_time(cls, data: Any):
        check_update_keys(data, ["name", "description", "metadata"])
        return data
