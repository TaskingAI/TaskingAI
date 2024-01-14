from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator, model_validator, Extra
from ..utils import validate_metadata, validate_list_cursors
from enum import Enum
from common.models import SortOrderEnum, MessageContent


class MessageRole(str, Enum):
    user = "user"
    assistant = "assistant"


class ChatLogType(str, Enum):
    retrieval = "retrieval"
    tool_call = "tool_call"
    tool_result = "tool_result"


class MessageGenerationLog(BaseModel):
    object: str = Field(
        "MessageGenerationLog",
        Literal="MessageGenerationLog",
        description="The object type, which is always `MessageGenerationLog`.",
    )
    session_id: str = Field(
        ..., min_length=24, max_length=24, description="The session ID from which the log is generated."
    )
    event: str = Field(..., description="The log event.")
    event_id: str = Field(..., min_length=24, max_length=24, description="The event ID.")
    event_step: str = Field(..., description="The step of the event.")
    timestamp: int = Field(..., ge=0, description="The timestamp when the log was created.", example=1700000000000)
    content: Dict[str, Any] = Field(..., description="The log content.")


# ----------------------------
# List Messages
# GET /assistants/{assistant_id}/chats/{chat_id}/messages
class MessageListRequest(BaseModel):
    limit: int = Field(20, ge=1, le=100, description="The maximum number of messages to return.", examples=[20])

    order: Optional[SortOrderEnum] = Field(
        default=SortOrderEnum.DESC,
        description="The order of messages to return, `asc` for ascending and `desc` for descending.",
        examples=["desc"],
    )

    after: Optional[str] = Field(
        None,
        min_length=24,
        max_length=24,
        description="The cursor represented by a message_id to fetch the next page of messages.",
        examples=["message_1"],
    )

    before: Optional[str] = Field(
        None,
        min_length=24,
        max_length=24,
        description="The cursor represented by a message_id to fetch the previous page of messages.",
    )

    class Config:
        extra = Extra.forbid

    @model_validator(mode="before")
    def validate_data(cls, data: Any):
        return validate_list_cursors(data)


# ----------------------------
# Create Message
# POST /assistants/{assistant_id}/chats/{chat_id}/messages


class MessageCreateRequest(BaseModel):
    role: MessageRole = Field(
        MessageRole.user,
        Literal=MessageRole.user,
        description="The role of the message. Currently only `user` is supported.",
        examples=["user"],
    )

    content: MessageContent = Field(..., description="The message content.")

    metadata: Dict[str, str] = Field(
        {},
        min_items=0,
        max_items=16,
        escription="The message metadata. It can store up to 16 key-value pairs "
        "where each key's length is less than 64 and value's length is less than 512.",
        examples=[{}],
    )

    class Config:
        extra = Extra.forbid

    @field_validator("role")
    def validate_role(cls, role: MessageRole):
        if role != MessageRole.user:
            raise ValueError("Currently only `user` is supported.")
        return role

    @field_validator("metadata")
    def validate_metadata(cls, metadata: Dict):
        return validate_metadata(metadata)


# ----------------------------
# Update Message
# POST /assistants/{assistant_id}/chats/{chat_id}/messages/{message_id}


class MessageUpdateRequest(BaseModel):
    metadata: Dict[str, str] = Field(
        None,
        min_items=0,
        max_items=16,
        description="The message metadata. It can store up to 16 key-value pairs "
        "where each key's length is less than 64 and value's length is less than 512.",
        examples=[{}],
    )

    class Config:
        extra = Extra.forbid

    @field_validator("metadata")
    def validate_metadata(cls, metadata: Dict):
        return validate_metadata(metadata)


# ----------------------------
# Generate Assistant Message
# POST /assistants/{assistant_id}/chats/{chat_id}/messages/generate


class MessageGenerateRequest(BaseModel):
    system_prompt_variables: Dict = Field(
        {},
        min_items=0,
        max_items=16,
        description="The variables that fit the system prompt template.",
        examples=[{"langauge": "English"}],
    )

    stream: bool = Field(
        False,
        description="Whether to return the assistant message in stream format. "
        "When this option is turned on, the response data will be returned in SSE format.",
        examples=[False],
    )

    debug: bool = Field(
        False,
        description="Whether to include the debug information in the response. "
        "When this option is turned on, the response data will be returned in SSE format.",
        examples=[False],
    )

    class Config:
        extra = Extra.forbid
