from typing import Dict, Optional, Any, List
from pydantic import BaseModel, Field, model_validator
import json

MAXIMUM_PARAMETER_DESCRIPTION_LENGTH = 300
allowed_param_type = ["string", "number", "integer", "boolean", "array"]

__all__ = [
    "ChatCompletionFunctionCall",
    "ChatCompletionFunctionParametersProperty",
    "ChatCompletionFunctionParameters",
    "ChatCompletionFunction",
    "function_call_is_function_name",
    "validate_function_call_and_functions",
]


class ChatCompletionFunctionCall(BaseModel):
    id: str = Field(...)
    name: str = Field(...)
    arguments: Dict[str, Any] = Field(...)

    @model_validator(mode="before")
    def validate_arguments(cls, data: Any):
        if isinstance(data["arguments"], str):
            try:
                data["arguments"] = json.loads(data["arguments"])
            except json.decoder.JSONDecodeError:
                raise ValueError("arguments should be a valid JSON or JSON string.")
        return data


class ChatCompletionFunctionParametersPropertyItems(BaseModel):
    type: str = Field(
        ...,
        pattern="^(string|number|integer|boolean)$",
        description="The type of the item.",
    )


class ChatCompletionFunctionParametersProperty(BaseModel):
    # type in ["string", "number", "integer", "boolean", "array"]
    type: str = Field(
        ...,
        pattern="^(string|number|integer|boolean|array)$",
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

    @model_validator(mode="before")
    def custom_validate(cls, data: Any):
        if data.get("type") != "string" and data.get("enum"):
            raise ValueError("enum is only allowed when type is 'string'")
        if data.get("type") == "array" and not data.get("items"):
            raise ValueError("items is required when type is 'array'")
        return data


class ChatCompletionFunctionParameters(BaseModel):

    properties: Dict[str, ChatCompletionFunctionParametersProperty] = Field(
        ...,
        description="The properties of the parameters.",
    )

    type: str = Field(
        "object",
        Literal="object",
        description="The type of the parameters, which is always 'object'.",
    )

    required: List[str] = Field(
        [],
        description="The required parameters.",
    )

    # check all params in "required" are in properties' keys
    @model_validator(mode="before")
    def validate_required(cls, data: Any):
        if "required" not in data:
            data["required"] = []
        for param in data["required"]:
            if param not in data["properties"]:
                raise ValueError(f"parameter {param} is in required but not in properties")
        return data

    def model_dump(self, **kwargs: Any):
        properties_dict = {
            param_name: param.model_dump(exclude_none=True, **kwargs) for param_name, param in self.properties.items()
        }
        return {
            "type": self.type,
            "properties": properties_dict,
            "required": self.required,
        }


class ChatCompletionFunction(BaseModel):
    name: str = Field(
        ...,
        description="The name of the function.",
    )
    description: str = Field(
        ...,
        description="The description of the function.",
    )
    parameters: ChatCompletionFunctionParameters = Field(
        ...,
        description="The parameters of the function.",
    )

    def model_dump(self, **kwargs: Any):
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters.model_dump(**kwargs),
        }


def function_call_is_function_name(function_call: Optional[str]):
    return function_call is not None and (function_call != "none" and function_call != "auto")


def validate_function_call_and_functions(function_call: Optional[str], functions: Optional[List[Dict]]):
    if function_call == "none":
        if functions:
            functions = None

    elif function_call == "auto":
        if functions is None:
            function_call = "none"

    elif function_call_is_function_name(function_call):
        if functions is None:
            raise ValueError(f"function call is not allowed when functions is not provided")

        function_names = [f.get("name") for f in functions]
        if function_call not in function_names:
            raise ValueError(f"{function_call} is not a function name")

        functions = [f for f in functions if f.get("name") == function_call]

    return function_call, functions
