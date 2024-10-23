from typing import List, Optional, Union

from pydantic import BaseModel, Field
from app.models import BaseModelProperties, BaseModelPricing, ModelSchema
from app.models.model_config import validate_config_value
from app.error import raise_http_error, ErrorCode

__all__ = [
    "ChatCompletionModelConfiguration",
    "ChatCompletionModelProperties",
    "ChatCompletionModelPricing",
    "validate_chat_completion_model",
]


class ChatCompletionModelConfiguration(BaseModel):
    temperature: Optional[float] = Field(None)
    top_p: Optional[float] = Field(None)
    top_k: Optional[int] = Field(None)
    max_tokens: Optional[int] = Field(None)
    stop: Optional[Union[str, List[str]]] = Field(None)
    presence_penalty: Optional[float] = Field(None)
    frequency_penalty: Optional[float] = Field(None)
    seed: Optional[int] = Field(None)
    response_format: Optional[str] = Field(None)


class ChatCompletionModelProperties(BaseModelProperties):

    function_call: bool = Field(
        False,
        description="Indicates if the model supports function call.",
    )
    streaming: bool = Field(
        False,
        description="Indicates if the model supports streaming of text chunks.",
    )
    vision: bool = Field(
        False,
        description="Indicates if the model accepts image as input.",
    )
    input_token_limit: Optional[int] = Field(
        None,
        description="The maximum number of tokens that can be included in the model's input.",
    )
    output_token_limit: Optional[int] = Field(
        None,
        description="The maximum number of tokens that the model can generate as output.",
    )


class ChatCompletionModelPricing(BaseModelPricing):

    input_token: float = Field(
        ...,
        description="The input token price.",
    )

    output_token: float = Field(
        ...,
        description="The output token price.",
    )

    unit: int = Field(
        ...,
        description="The unit of the price.",
    )


def validate_chat_completion_model(
    model_schema: ModelSchema,
    stream: bool,
    function_call: bool,
    vision_input: bool,
    configs: ChatCompletionModelConfiguration,
    verify: bool = False,
):
    """
    Validate chat completion model's properties and configurations
    :param model_schema: the model schema
    :param stream: whether the request requires streaming
    :param function_call: whether the request requires function call
    :param vision_input: whether the request requires vision input
    :param configs: the model configurations
    :param verify: whether to verify the model
    """
    model_schema_id = model_schema.model_schema_id
    if stream and not model_schema.allow_stream():
        raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, f"model {model_schema_id} does not support streaming.")

    # if function_call and not model_schema.allow_function_call():
    #     raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, f"model {model_schema_id} does not support function call.")

    if vision_input and not model_schema.allow_vision_input():
        raise_http_error(
            ErrorCode.REQUEST_VALIDATION_ERROR, f"model {model_schema_id} does not support vision message."
        )

    c_dict = configs.model_dump()
    constraints_dict = {config_schema["config_id"]: config_schema for config_schema in model_schema.config_schemas}
    for key, value in c_dict.items():
        if value is not None:
            if key not in constraints_dict.keys():
                if verify:
                    raise_http_error(
                        ErrorCode.REQUEST_VALIDATION_ERROR, f"{key} is not allowed for the model {model_schema_id}."
                    )
                else:
                    setattr(configs, key, None)
            elif not validate_config_value(value, constraints_dict[key]["schema"]):
                raise_http_error(
                    ErrorCode.REQUEST_VALIDATION_ERROR,
                    f"{key} does not conform to the required constraints: {constraints_dict[key]['schema']}.",
                )
