from typing import Dict, List, Any
from pydantic import Field, BaseModel
from enum import Enum
import logging

logger = logging.getLogger(__name__)

from tkhelper.models import ModelEntity
from tkhelper.utils import load_json_attr, generate_random_id
from tkhelper.schemas.field import *

from .assistant import Assistant
from .chat import Chat

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


class Message(ModelEntity):
    object: str = "Message"
    assistant_id: str = id_field("assistant", length_range=(1, 50))
    chat_id: str = id_field("chat", length=24)
    message_id: str = id_field("message", length=24)

    role: MessageRole = Field(..., description="The role of the message")
    content: MessageContent = Field(..., description="The content of the message")
    num_tokens: int = Field(..., ge=0, description="The number of tokens in the message.")
    metadata: Dict = metadata_field()

    created_timestamp: int = created_timestamp_field()
    updated_timestamp: int = updated_timestamp_field()

    @staticmethod
    def build(row):
        return Message(
            assistant_id=row["assistant_id"],
            chat_id=row["chat_id"],
            message_id=row["message_id"],
            role=MessageRole(row["role"]),
            content=MessageContent(**load_json_attr(row, "content", {})),
            num_tokens=row["num_tokens"],
            metadata=load_json_attr(row, "metadata", {}),
            created_timestamp=row["created_timestamp"],
            updated_timestamp=row["updated_timestamp"],
        )

    def to_response_dict(self) -> Dict:
        return {
            "object": "Message",
            "assistant_id": self.assistant_id,
            "chat_id": self.chat_id,
            "message_id": self.message_id,
            "role": self.role,
            "content": self.content.model_dump(exclude_none=True),
            "num_tokens": self.num_tokens,
            "metadata": self.metadata,
            "created_timestamp": self.created_timestamp,
            "updated_timestamp": self.updated_timestamp,
        }

    @staticmethod
    def object_name() -> str:
        return "message"

    @staticmethod
    def object_plural_name() -> str:
        return "messages"

    @staticmethod
    def table_name() -> str:
        return "message"

    @staticmethod
    def id_field_name() -> str:
        return "message_id"

    @staticmethod
    def primary_key_fields() -> List[str]:
        return ["assistant_id", "chat_id", "message_id"]

    @staticmethod
    def generate_random_id() -> str:
        return "Mah1" + generate_random_id(20)

    @staticmethod
    def list_prefix_filter_fields() -> List[str]:
        return []

    @staticmethod
    def parent_models() -> List:
        return [Assistant, Chat]

    @staticmethod
    def parent_operator() -> List:
        from app.operators import assistant_ops, chat_ops

        return [assistant_ops, chat_ops]

    @staticmethod
    def create_fields() -> List[str]:
        return ["role", "content", "metadata"]

    @staticmethod
    def update_fields() -> List[str]:
        return ["metadata"]

    @staticmethod
    def fields_exclude_in_response():
        return []
