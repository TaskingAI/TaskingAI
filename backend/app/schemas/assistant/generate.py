from typing import Dict
from pydantic import BaseModel, Field
from app.models import Message

__all__ = [
    "MessageGenerateRequest",
    "MessageGenerateResponse",
]

# ----------------------------
# Generate Assistant Message
# POST /assistants/{assistant_id}/chats/{chat_id}/messages/generate
# Request Params: None
# Request: MessageGenerateRequest
# Response: MessageGenerateResponse


class MessageGenerateRequest(BaseModel):
    system_prompt_variables: Dict[str, str] = Field(
        {},
        min_length=0,
        max_length=16,
        description="The variables that fit the system prompt template.",
        examples=[{"language": "English"}],
    )
    stream: bool = Field(
        False,
        description="Whether to return the assistant message in stream format. When this option is turned on, the response data will be returned in SSE format.",
        examples=[False],
    )
    debug: bool = Field(
        False,
        description="Whether to include the debug information in the response. When this option is turned on, the response data will be returned in SSE format.",
        examples=[False],
    )


class MessageGenerateResponse(BaseModel):
    status: str = Field("success")
    data: Message = Field(...)
