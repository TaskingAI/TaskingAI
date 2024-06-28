from fastapi import APIRouter
from starlette.responses import StreamingResponse
from aiohttp import client_exceptions
from typing import List, Optional, Tuple, Dict
import json
import logging
from app.cache import get_chat_completion_model
from app.error import raise_http_error, ErrorCode, TKHttpException, error_message, error_messages
from app.models import (
    ProviderCredentials,
    ChatCompletionMessage,
    ChatCompletionModelConfiguration,
    ChatCompletionFunction,
    ChatCompletion,
    validate_credentials,
    validate_model_info,
    validate_chat_completion_model,
    ModelType,
    ModelSchema,
    BaseModelProperties,
)
from config import CONFIG
from .schema import *

router = APIRouter()
logger = logging.getLogger(__name__)


async def chat_completion(
    model_infos: List[Tuple[ModelSchema, str, BaseModelProperties, ModelType]],
    messages: List[ChatCompletionMessage],
    credentials: ProviderCredentials,
    configs: ChatCompletionModelConfiguration,
    function_call: Optional[str] = None,
    functions: Optional[List[ChatCompletionFunction]] = None,
    proxy: Optional[str] = None,
    custom_headers: Optional[Dict[str, str]] = None,
) -> ChatCompletion:
    if not model_infos:
        raise_http_error(ErrorCode.INTERNAL_SERVER_ERROR, "No model info provided.")

    last_exception = None
    for i, (model_schema, provider_model_id, _, _) in enumerate(model_infos):
        model = get_chat_completion_model(model_schema.provider_id)
        if not model:
            error_str = f"Provider {model_schema.provider_id} is not supported through the chat_completion API."
            logger.error(error_str)
            last_exception = TKHttpException(
                status_code=error_messages[ErrorCode.REQUEST_VALIDATION_ERROR]["status_code"],
                detail={"error_code": ErrorCode.REQUEST_VALIDATION_ERROR, "message": error_str},
            )
            continue

        try:
            response = await model.chat_completion(
                provider_model_id=provider_model_id,
                messages=messages,
                credentials=credentials,
                configs=configs,
                function_call=function_call,
                functions=functions,
                proxy=proxy,
                custom_headers=custom_headers,
                model_schema=model_schema,
            )
            if i > 0:
                response.fallback_index = i - 1
            return response
        except TKHttpException as e:
            logger.error(f"chat_completion: provider {model_schema.provider_id} error = {e}")
            last_exception = e
        except client_exceptions.InvalidURL as e:
            logger.error(f"chat_completion: provider {model_schema.provider_id} error = {e}")
            last_exception = TKHttpException(
                status_code=error_messages[ErrorCode.REQUEST_VALIDATION_ERROR]["status_code"],
                detail={"error_code": ErrorCode.REQUEST_VALIDATION_ERROR, "message": str(e)},
            )
        except client_exceptions.ClientConnectionError as e:
            logger.error(f"chat_completion: provider {model_schema.provider_id} error = {e}")
            last_exception = TKHttpException(
                status_code=error_messages[ErrorCode.REQUEST_VALIDATION_ERROR]["status_code"],
                detail={"error_code": ErrorCode.REQUEST_VALIDATION_ERROR, "message": str(e)},
            )

        except Exception as e:
            logger.error(f"Unhandled exception for provider {model_schema.provider_id}: {str(e)}")
            logger.error(f"messages: {messages}")
            logger.error(f"configs: {configs}")
            logger.error(f"function_call: {function_call}")
            logger.error(f"functions: {functions}")
            last_exception = TKHttpException(
                status_code=error_messages[ErrorCode.INTERNAL_SERVER_ERROR]["status_code"],
                detail={"error_code": ErrorCode.INTERNAL_SERVER_ERROR, "message": str(e)},
            )

    if last_exception:
        raise last_exception  # Raise the last caught exception if all models fail

    # TODO: raise_http_error(ErrorCode.PROVIDER_SERVICE_UNAVAILABLE, "All providers' services are unavailable.")


async def chat_completion_stream(
    model_infos: List[Tuple[ModelSchema, str, BaseModelProperties, ModelType]],
    messages: List[ChatCompletionMessage],
    credentials: ProviderCredentials,
    configs: ChatCompletionModelConfiguration,
    function_call: Optional[str] = None,
    functions: Optional[List[ChatCompletionFunction]] = None,
    proxy: Optional[str] = None,
    custom_headers: Optional[Dict[str, str]] = None,
):
    if not model_infos:
        raise_http_error(ErrorCode.INTERNAL_SERVER_ERROR, "No model info provided.")

    last_exception = None
    for i, (model_schema, provider_model_id, _, _) in enumerate(model_infos):
        model = get_chat_completion_model(model_schema.provider_id)
        if not model:
            error_str = f"Provider {model_schema.provider_id} is not supported through the chat_completion API."
            logger.error(error_str)
            last_exception = TKHttpException(
                status_code=error_messages[ErrorCode.REQUEST_VALIDATION_ERROR]["status_code"],
                detail={"error_code": ErrorCode.REQUEST_VALIDATION_ERROR, "message": error_str},
            )
            continue

        try:
            async for response in model.chat_completion_stream(
                provider_model_id=provider_model_id,
                messages=messages,
                credentials=credentials,
                configs=configs,
                function_call=function_call,
                functions=functions,
                proxy=proxy,
                custom_headers=custom_headers,
                model_schema=model_schema,
            ):
                if isinstance(response, ChatCompletion):
                    if i:
                        response.fallback_index = i - 1
                yield response
            return
        except TKHttpException as e:
            logger.error(f"chat_completion: provider {model_schema.provider_id} error = {e}")
            last_exception = e
        except Exception as e:
            logger.error(f"Unhandled exception for provider {model_schema.provider_id}: {str(e)}")
            last_exception = e

    if last_exception:
        raise last_exception  # Raise the last caught exception if all models fail

    # TODO: raise_http_error(ErrorCode.PROVIDER_SERVICE_UNAVAILABLE, "All providers' services are unavailable.")


# add new add_api_key
@router.post(
    "/chat_completion",
    operation_id="chat_completion",
    summary="Chat Completion",
    tags=["Inference"],
    responses={422: {"description": "Unprocessable Entity"}},
    response_model=ChatCompletionResponse,
)
async def api_chat_completion(
    data: ChatCompletionRequest,
):
    # validate model info
    model_infos = [
        validate_model_info(
            model_schema_id=data.model_schema_id,
            provider_model_id=data.provider_model_id,
            properties_dict=data.properties,
            model_type=ModelType.CHAT_COMPLETION,
        )
    ]

    # validate fallback model info
    if data.fallbacks:
        for fallback in data.fallbacks:
            model_infos.append(
                validate_model_info(
                    model_schema_id=fallback.model_schema_id,
                    provider_model_id=fallback.provider_model_id,
                    properties_dict=data.properties,
                    model_type=ModelType.CHAT_COMPLETION,
                )
            )

    # validate credentials
    provider_credentials = validate_credentials(
        model_infos=model_infos,
        credentials_dict=data.credentials,
        encrypted_credentials_dict=data.encrypted_credentials,
    )

    # validate model properties and configurations
    vision_input = has_multimodal_user_message(data.messages)
    for model_info in model_infos:
        validate_chat_completion_model(
            model_schema=model_info[0],
            stream=data.stream,
            function_call=bool(data.functions),
            vision_input=vision_input,
            configs=data.configs,
        )
        model_type = model_info[3]
        if model_type != ModelType.CHAT_COMPLETION and model_type != ModelType.WILDCARD:
            raise_http_error(
                ErrorCode.REQUEST_VALIDATION_ERROR, "Model type should be chat_completion, but got " + model_type
            )

    # check if proxy is blacklisted
    if data.proxy:
        for url in CONFIG.PROVIDER_URL_BLACK_LIST:
            if url in data.proxy:
                raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, f"Invalid provider url: {url}")

    if data.stream:

        async def generator():
            logger.debug("start stream")
            i = 0

            try:
                async for response in chat_completion_stream(
                    model_infos=model_infos,
                    messages=data.messages,
                    credentials=provider_credentials,
                    configs=data.configs,
                    function_call=data.function_call,
                    functions=data.functions,
                    proxy=data.proxy,
                    custom_headers=data.custom_headers,
                ):
                    yield f"data: {response.model_dump_json()}\n\n"
                    i += 1
            except TKHttpException as e:
                err_dict = error_message(e.detail["message"], ErrorCode.PROVIDER_ERROR)
                yield f"data: {json.dumps(err_dict)}\n\n"
            except Exception as e:
                err_dict = error_message(str(e), ErrorCode.UNKNOWN_ERROR)
                yield f"data: {json.dumps(err_dict)}\n\n"

            yield f"data: [DONE]\n\n"

        return StreamingResponse(generator(), media_type="text/event-stream")

    else:
        # generate none stream response
        response: ChatCompletion = await chat_completion(
            model_infos=model_infos,
            messages=data.messages,
            credentials=provider_credentials,
            configs=data.configs,
            function_call=data.function_call,
            functions=data.functions,
            proxy=data.proxy,
            custom_headers=data.custom_headers,
        )

        if response:
            return ChatCompletionResponse(data=response)
        else:
            raise_http_error(ErrorCode.UNKNOWN_ERROR, "unknown error")
