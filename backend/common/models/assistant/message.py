from pydantic import BaseModel, Field
from enum import Enum
from common.utils import generate_random_id, load_json_attr
from typing import Dict, Any
from common.models import SerializePurpose

__all__ = ["Message", "MessageRole", "MessageContent", "MessageGenerationLog"]


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"


class MessageGenerationLog(BaseModel):

    """
    MessageGenerationLog is a log object to describe the message generation process.
    """

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
    event_step: str = Field(..., description="The current step of the event.")
    timestamp: int = Field(..., ge=0, description="The timestamp when the log was created.", example=1700000000000)
    content: Dict[str, Any] = Field(..., description="The log content.")


class MessageContent(BaseModel):

    """
    MessageContent is the content of a message. Currently only text content is supported.
    """

    text: str = Field(..., description="The text content of the message.", examples=["Hello!"])

    # todo: support more content type, i.e. file, image, etc.


class Message(BaseModel):
    message_id: str
    chat_id: str
    assistant_id: str
    role: MessageRole
    content: MessageContent
    metadata: Dict
    updated_timestamp: int
    created_timestamp: int

    @staticmethod
    def object_name():
        return "Message"

    @staticmethod
    def generate_random_id():
        return "Mah1" + generate_random_id(20)

    @classmethod
    def build(cls, row):
        return cls(
            message_id=row["message_id"],
            chat_id=row["chat_id"],
            assistant_id=row["assistant_id"],
            role=MessageRole(row["role"]),
            content=MessageContent(**load_json_attr(row, "content", {})),
            metadata=load_json_attr(row, "metadata", {}),
            updated_timestamp=row["updated_timestamp"],
            created_timestamp=row["created_timestamp"],
        )

    def to_dict(self, purpose: SerializePurpose):
        ret = {
            "object": self.object_name(),
            "message_id": self.message_id,
            "chat_id": self.chat_id,
            "assistant_id": self.assistant_id,
            "role": self.role.value,
            "content": self.content,
            "metadata": self.metadata,
            "updated_timestamp": self.updated_timestamp,
            "created_timestamp": self.created_timestamp,
        }
        return ret
