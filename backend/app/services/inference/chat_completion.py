import aiohttp
from typing import List, Dict, Optional
from tkhelper.utils import check_http_error, ResponseWrapper, sse_stream_dict_generate
from tkhelper.error import raise_http_error, ErrorCode
from app.config import CONFIG
from app.models import ModelSchema, ModelType, Model
import logging

logger = logging.getLogger(__name__)


__all__ = [
    "chat_completion",
    "stream_chat_completion",
]


async def __validate_model(model: Model):
    """
    Validate the model and make sure it is a chat completion model
    :param model: the model object
    :return: the provider model id and properties
    """
    if not model.is_chat_completion():
        raise_http_error(
            ErrorCode.REQUEST_VALIDATION_ERROR,
            message=f"Model {model.model_id} is not a chat completion model.",
        )

    model_schema: ModelSchema = model.model_schema()
    if model_schema is None or model_schema.type == ModelType.WILDCARD:
        provider_model_id = model.provider_model_id
        properties = model.properties
    elif model.is_custom_host():
        provider_model_id = model_schema.provider_model_id
        properties = model.properties
    else:
        provider_model_id = model_schema.provider_model_id
        properties = model_schema.properties

    return provider_model_id, properties


async def chat_completion(
    model: Model,
    messages: List[Dict],
    configs: Dict,
    function_call: Optional[str] = None,
    functions: Optional[List[Dict]] = None,
) -> Dict:
    """
    Perform chat completion
    :param model: the model object
    :param messages: a list of chat completion messages
    :param configs: the model configurations
    :param function_call: the function call parameter
    :param functions: the list of functions
    :return: the chat completion data
    """

    model_schema_id = model.model_schema_id
    provider_model_id, properties = await __validate_model(model)
    request_url = f"{CONFIG.TASKINGAI_INFERENCE_URL}/v1/chat_completion"
    payload = {
        "model_schema_id": model_schema_id,
        "provider_model_id": provider_model_id,
        "messages": messages,  # List of message dicts
        "encrypted_credentials": model.encrypted_credentials,
        "properties": properties,
        "configs": configs,
        "function_call": function_call,
        "functions": functions,
        "stream": False,
    }

    async with aiohttp.ClientSession() as session:
        response = await session.post(request_url, json=payload)
        response_wrapper = ResponseWrapper(response.status, await response.json())
        check_http_error(response_wrapper)
        return response_wrapper.json()["data"]


async def stream_chat_completion(
    model: Model,
    messages: List[Dict],
    configs: Dict,
    function_call: Optional[str] = None,
    functions: Optional[List[Dict]] = None,
    chunk_handler: Optional[callable] = None,
):
    """
    Perform chat completion
    :param model: the model object
    :param messages: a list of chat completion messages
    :param configs: the model configurations
    :param function_call: the function call parameter
    :param functions: the list of functions
    :param chunk_handler: the handler to process each chunk
    :return: a generator of chat completion chunks
    """

    model_schema_id = model.model_schema_id
    provider_model_id, properties = await __validate_model(model)
    request_url = f"{CONFIG.TASKINGAI_INFERENCE_URL}/v1/chat_completion"
    payload = {
        "model_schema_id": model_schema_id,
        "provider_model_id": provider_model_id,
        "messages": messages,  # List of message dicts
        "encrypted_credentials": model.encrypted_credentials,
        "properties": properties,
        "configs": configs,
        "function_call": function_call,
        "functions": functions,
        "stream": True,
    }

    return await sse_stream_dict_generate(request_url, payload, chunk_handler)
