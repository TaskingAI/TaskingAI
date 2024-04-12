from typing import Optional, Any, Dict, List
from pydantic import BaseModel, Field


__all__ = [
    "ChatCompletionFunctionCall",
    "ChatCompletionFunctionParametersProperty",
    "ChatCompletionFunctionParameters",
    "ChatCompletionFunction",
]


class ChatCompletionFunctionCall(BaseModel):
    id: str = Field(
        ...,
        description="The id of the function call.",
        examples=["call_abc123"],
    )
    arguments: Dict[str, Any] = Field(
        ...,
        description="The arguments of the function call.",
        examples=[{"a": 1, "b": 2}],
    )
    name: str = Field(
        ...,
        description="The name of the function.",
        examples=["plus_a_and_b"],
    )

class ChatCompletionFunctionParametersPropertyItems(BaseModel):
    type: str = Field(
        ...,
        pattern="^(string|number|integer|boolean)$",
        description="The type of the item.",
    )

class ChatCompletionFunctionParametersProperty(BaseModel):
    # type in ["string", "number", "integer", "boolean"]
    type: str = Field(
        ...,
        pattern="^(string|number|integer|boolean|array|object)$",
        description="The type of the parameter.",
    )

    # items only used in array
    items: Optional[ChatCompletionFunctionParametersPropertyItems] = Field(
        None,
        description="The items of the parameter. Which is only allowed when type is 'array'.",
    )

    # description should not more than MAXIMUM_PARAMETER_DESCRIPTION_LENGTH characters
    description: str = Field("", max_length=512, description="The description of the parameter.")

    # optional enum
    enum: Optional[List[str]] = Field(
        None,
        description="The enum list of the parameter. Which is only allowed when type is 'string'.",
    )


class ChatCompletionFunctionParameters(BaseModel):
    type: str = Field(
        "object",
        Literal="object",
        description="The type of the parameters, which is always 'object'.",
    )

    properties: Dict[str, ChatCompletionFunctionParametersProperty] = Field(
        ...,
        description="The properties of the parameters.",
    )

    required: List[str] = Field(
        [],
        description="The required parameters.",
    )


class ChatCompletionFunction(BaseModel):
    name: str = Field(
        ...,
        description="The name of the function.",
        examples=["plus_a_and_b"],
    )

    description: str = Field(
        ...,
        description="The description of the function.",
        examples=["Add two numbers"],
    )

    parameters: ChatCompletionFunctionParameters = Field(
        ...,
        description="The function's parameters are represented as an object in JSON Schema format.",
        examples=[
            {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "The first number"},
                    "b": {"type": "number", "description": "The second number"},
                },
                "required": ["a", "b"],
            }
        ],
    )
