from typing import Optional, Any, Dict
from pydantic import BaseModel, Field, field_validator, model_validator, Extra
from ..utils import validate_metadata, validate_list_cursors
from common.models import SortOrderEnum


# ----------------------------
# List Chat
# GET /assistants/{assistant_id}/chats
class ChatListRequestParamsSchema(BaseModel):
    limit: int = Field(20, ge=1, le=100, description="The maximum number of objects to return.", examples=[20])

    # todo: add different sort field options
    order: Optional[SortOrderEnum] = Field(
        SortOrderEnum.DESC,
        description="The order of objects to return, `asc` for ascending and `desc` for descending.",
        examples=["desc"],
    )

    after: Optional[str] = Field(
        None,
        min_length=24,
        max_length=24,
        description="The cursor represented by a object_id to fetch the next page of objects.",
    )

    before: Optional[str] = Field(
        None,
        min_length=24,
        max_length=24,
        description="The cursor represented by a object_id to fetch the previous page of objects.",
    )

    offset: Optional[int] = Field(
        None,
        ge=0,
        description="The offset of objects to return. "
        "Only one in `offset`, `after` and `before` can be used at the same time.",
    )

    id_search: Optional[str] = Field(None, min_length=1, max_length=256, description="The object ID to search for.")

    class Config:
        extra = Extra.forbid

    @model_validator(mode="before")
    def custom_validate(cls, data: Any):
        return validate_list_cursors(data)


# ----------------------------
# Create Chat
# POST /assistants/{assistant_id}/chats
class ChatCreateRequest(BaseModel):
    metadata: Dict[str, str] = Field(
        {},
        min_items=0,
        max_items=16,
        description="The chat metadata. It can store up to 16 key-value pairs "
        "where each key's length is less than 64 and value's length is less than 512.",
        examples=[{}],
    )

    class Config:
        extra = Extra.forbid

    @field_validator("metadata")
    def validate_metadata(cls, metadata):
        return validate_metadata(metadata)


# ----------------------------
# Update Chat
# POST /assistants/{assistant_id}/chats/{chat_id}
class ChatUpdateRequest(BaseModel):
    metadata: Dict[str, str] = Field(
        ...,
        min_items=0,
        max_items=16,
        description="The chat metadata. It can store up to 16 key-value pairs "
        "where each key's length is less than 64 and value's length is less than 512.",
        examples=[{}],
    )

    class Config:
        extra = Extra.forbid

    @field_validator("metadata")
    def validate_metadata(cls, metadata):
        return validate_metadata(metadata)
