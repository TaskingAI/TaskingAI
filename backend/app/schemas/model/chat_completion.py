from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Extra, Field, field_validator
from app.models.inference import *

__all__ = [
    "ChatCompletionRequest",
    "ChatCompletionResponse",
]


# Chat Completion
# POST /v1/chat_completion
# Request Params: None
# Request: ChatCompletionRequest
# Response: ChatCompletionResponse
class ChatCompletionRequest(BaseModel):
    model_id: str = Field(
        ..., min_length=8, max_length=8, description="The chat completion model id.", examples=["abcdefgh"]
    )
    configs: Optional[Dict] = Field(None, description="The model configuration.", examples=[{"temperature": 0.5}])
    stream: bool = Field(
        False,
        description="Indicates whether the response should be streamed. "
        "If set to True, the response will be streamed using Server-Sent Events (SSE).",
        examples=[False],
    )
    messages: List[
        Union[
            ChatCompletionFunctionMessage,
            ChatCompletionAssistantMessage,
            ChatCompletionUserMessage,
            ChatCompletionSystemMessage,
        ]
    ] = Field(..., description="The messages to be sent to the model.")
    function_call: Optional[str] = Field(
        None,
        description="Controls whether a specific function is invoked by the model. "
        "If set to 'none', the model will generate a message without calling a function. "
        "If set to 'auto', the model can choose between generating a message or calling a function. "
        "Defining a specific function using {'name': 'my_function'} instructs the model to call that particular function. "
        "By default, 'none' is selected when there are no chat_completion_functions available, and 'auto' is selected when one or more chat_completion_functions are present.",
    )
    functions: Optional[List[ChatCompletionFunction]] = Field(None)

    class Config:
        extra = Extra.forbid

    @field_validator("messages", mode="before")
    def validate_message(cls, messages: List[Dict]):
        if not messages:
            raise ValueError("messages cannot be empty.")
        return [cls._convert_message(m) for m in messages]

    @staticmethod
    def _convert_message(message_data: Dict):
        role = message_data.get("role")
        if role == "system":
            return ChatCompletionSystemMessage(**message_data)
        elif role == "user":
            return ChatCompletionUserMessage(**message_data)
        elif role == "assistant":
            return ChatCompletionAssistantMessage(**message_data)
        elif role == "function":
            return ChatCompletionFunctionMessage(**message_data)
        else:
            raise ValueError(f"Invalid message role: {role}")


class ChatCompletionResponse(BaseModel):
    status: str = Field("success", Literal="success", description="The response status.", examples=["success"])
    data: ChatCompletion = Field(..., description="The chat completion response data.")
