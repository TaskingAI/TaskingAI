from typing import Dict, List, Optional
from pydantic import BaseModel, Field, Extra, field_validator, model_validator
from app.models.chat_completion import *
import logging

logger = logging.getLogger(__name__)

__all__ = [
    "ChatCompletionRequest",
    "ChatCompletionResponse",
    "has_multimodal_user_message",
]


def has_multimodal_user_message(messages: List[ChatCompletionMessage]):
    for message in messages:
        if isinstance(message, ChatCompletionUserMessage) and isinstance(message.content, List):
            return True
    return False


class ChatCompletionFallback(BaseModel):
    model_schema_id: str = Field(
        ...,
        min_length=1,
        max_length=127,
        description="The ID of the model schema.",
        examples=["openai/gpt-4"],
    )

    provider_model_id: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="The provider's model ID.",
    )


class ChatCompletionRequest(BaseModel):
    model_schema_id: str = Field(
        ...,
        min_length=1,
        max_length=127,
        description="The ID of the model schema.",
        examples=["openai/gpt-4"],
    )

    provider_model_id: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="The provider's model ID.",
    )

    messages: List[ChatCompletionMessage] = Field(
        ...,
        description="The messages to be sent to the model.",
        examples=[
            {
                "role": "user",
                "content": "What is the weather like in San Francisco?",
            },
        ],
    )

    stream: bool = Field(
        False,
        description="Indicates whether the response should be streamed. "
        "If set to True, the response will be streamed using Server-Sent Events (SSE).",
        examples=[False],
    )

    credentials: Optional[Dict] = Field(
        None,
        description="The credentials of the model provider. "
        "Only one of credentials or encrypted_credentials is required.",
        examples=[{"OPENAI_API_KEY": "YOUR_OPENAI_API_KEY"}],
    )

    encrypted_credentials: Optional[Dict] = Field(
        None,
        description="The encrypted credentials of the model provider.",
        examples=[None],
    )

    properties: Optional[Dict] = Field(
        None,
        description="The custom chat completion model properties.",
        examples=[None],
    )

    configs: ChatCompletionModelConfiguration = Field(
        ChatCompletionModelConfiguration(),
        description="Additional configuration to make the chat completion inference.",
        examples=[
            {
                "temperature": 0.7,
            }
        ],
    )

    proxy: Optional[str] = Field(None, description="The proxy of the model.")

    custom_headers: Optional[Dict[str, str]] = Field(
        None,
        min_items=0,
        max_items=16,
        description="The custom headers can store up to 16 key-value pairs where each key's "
        "length is less than 64 and value's length is less than 512.",
        examples=[{"key1": "value1"}, {"key2": "value2"}],
    )

    fallbacks: Optional[List[ChatCompletionFallback]] = Field(
        None,
        description="A list of fallback completions to use if the model fails to generate a response.",
        examples=[None],
    )

    function_call: Optional[str] = Field(
        "auto",
        description="Controls whether a specific function is invoked by the model. "
        "If set to 'none', the model will generate a message without calling a function. "
        "If set to 'auto', the model can choose between generating a message or calling a function. "
        "Specify a function name to instruct the model to call that particular function. "
        "By default, 'none' is selected when there are no chat_completion_functions available, "
        "and 'auto' is selected when one or more chat_completion_functions are present.",
    )

    functions: Optional[List[ChatCompletionFunction]] = Field(
        None,
        description="A list of functions that can be called by the chat completion model.",
        examples=[
            [
                {
                    "name": "get_weather_forecast",
                    "description": "Get the weather forecast for a city.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "A city name, e.g. San Francisco, CA",
                            },
                            "days": {"type": "number", "description": "The number of days to forecast."},
                            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                        },
                    },
                    "required": ["location", "days"],
                }
            ]
        ],
    )

    class Config:
        extra = Extra.forbid

    @field_validator("configs", mode="before")
    def validate_configs(cls, configs: Dict):
        if configs is None:
            return ChatCompletionModelConfiguration()
        return configs

    @field_validator("messages", mode="before")
    def validate_message(cls, messages: List[Dict]):
        # check each message is dict
        if not all(isinstance(m, Dict) for m in messages):
            raise ValueError("messages must be a list of dictionaries.")
        new_messages = [cls._convert_message(m) for m in messages]
        # remove None
        new_messages = [m for m in new_messages if m is not None]
        return new_messages

    @staticmethod
    def _convert_message(message_data: Dict):
        role = message_data.get("role")
        function_calls = message_data.get("function_calls")
        content = message_data.get("content")
        if role == "assistant":
            if not function_calls and not content:
                return None
        else:
            if not content:
                return None

        if role == "system":
            return ChatCompletionSystemMessage(**message_data)
        elif role == "user":
            return ChatCompletionUserMessage(**message_data)
        elif role == "assistant":
            return ChatCompletionAssistantMessage(**message_data)
        elif role == "function":
            return ChatCompletionFunctionMessage(**message_data)
        else:
            raise ValueError(f"invalid message role: {role}")

    @staticmethod
    def _is_assistant_function_calls_message(message: ChatCompletionMessage):
        return isinstance(message, ChatCompletionAssistantMessage) and message.function_calls is not None

    @field_validator("messages", mode="after")
    def validate_messages(cls, messages: List[ChatCompletionMessage]):
        if not messages:
            raise ValueError("messages cannot be empty.")

        system_count = len([msg for msg in messages if msg.role == ChatCompletionRole.system])
        if system_count > 1:
            raise ValueError("more than one system message found.")
        if system_count == 1 and messages[0].role != ChatCompletionRole.system:
            raise ValueError("system message is not at the first position.")

        function_calls_ids = []
        functions_ids = set()

        for i, msg in enumerate(messages):
            if cls._is_assistant_function_calls_message(msg):
                # Collect the ids of all new function_calls
                unmatched_function_calls = [fc_id for fc_id in function_calls_ids if fc_id not in functions_ids]
                if unmatched_function_calls:
                    raise ValueError(
                        f"Function_calls with ids {unmatched_function_calls} do not have a "
                        f"corresponding function message before the next function_call."
                    )

                function_calls_ids.extend([fc.id for fc in msg.function_calls])

                # Check all previous function_calls for corresponding functions

            elif msg.role == ChatCompletionRole.function:
                if msg.id in functions_ids:
                    raise ValueError(f"function with id {msg.id} appears more than once.")

                functions_ids.add(msg.id)
                if msg.id not in function_calls_ids:
                    raise ValueError(
                        f"function message with id {msg.id} appears without a preceding " f"function_call."
                    )

            elif msg.role in [ChatCompletionRole.user, ChatCompletionRole.assistant]:
                if function_calls_ids:
                    raise ValueError(
                        "user and assistant roles are not allowed after function role until all "
                        "function_calls have corresponding functions."
                    )

        # Finally check if there are any unmatched function_calls
        unmatched_function_calls = [fc_id for fc_id in function_calls_ids if fc_id not in functions_ids]
        if unmatched_function_calls:
            raise ValueError(
                f"Function_calls with ids {unmatched_function_calls} do not have a corresponding " f"function message."
            )

        # User and assistant role must appear alternately. If they appear consecutively, they can
        # be merged into one.
        prev_role = None
        new_messages = []
        merge_message = None
        for i, msg in enumerate(messages):
            if msg.role != ChatCompletionRole.user and (
                msg.role != ChatCompletionRole.assistant or is_assistant_function_calls_message(msg)
            ):
                if merge_message is not None:
                    new_messages.append(merge_message)
                new_messages.append(msg)
                merge_message = None
                continue
            if msg.role == prev_role:
                merge_message.content += "\n\n" + msg.content
            else:
                if merge_message is not None:
                    new_messages.append(merge_message)
                merge_message = msg
                prev_role = msg.role

        # Add the last merge_message if it's not None
        if merge_message is not None:
            new_messages.append(merge_message)

        logger.debug("Validation successful. Messages are in correct format.")
        logger.debug(f"new_messages = {new_messages}")
        logger.debug("------------------------------------------------------------")
        return new_messages

    @model_validator(mode="before")
    def validate_before(cls, data: Dict):
        # validate function
        function_call, functions = validate_function_call_and_functions(
            function_call=data.get("function_call"), functions=data.get("functions")
        )
        data["function_call"] = function_call
        data["functions"] = functions

        return data


class ChatCompletionResponse(BaseModel):
    status: str = Field(
        "success",
        Literal="success",
        description="The status of the response.",
    )
    data: ChatCompletion = Field(
        ...,
        description="The chat completion response data.",
        examples=[
            {
                "object": "ChatCompletion",
                "finish_reason": "function_calls",
                "message": {
                    "role": "assistant",
                    "function_calls": [
                        {
                            "id": "call_123",
                            "name": "get_weather_forecast",
                            "parameters": {"location": "San Francisco, CA", "days": 3, "unit": "fahrenheit"},
                        }
                    ],
                },
                "created_timestamp": 1632016815000,
            }
        ],
    )
