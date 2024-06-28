from fastapi import APIRouter
from app.models import BaseSuccessDataResponse
from .schema import VerifyModelCredentialsSchema
from app.models import (
    ChatCompletionModelConfiguration,
    ChatCompletionModelProperties,
    ChatCompletionUserMessage,
    ChatCompletion,
    TextEmbeddingModelConfiguration,
    TextEmbeddingModelProperties,
    ModelType,
    validate_credentials,
    validate_model_info,
    ChatCompletionFunction,
    validate_chat_completion_model,
)
from app.error import ErrorCode, raise_http_error, TKHttpException, error_messages
from aiohttp import client_exceptions
import logging
from config import CONFIG

logger = logging.getLogger(__name__)


router = APIRouter()


@router.post(
    "/verify_credentials",
    response_model=BaseSuccessDataResponse,
    include_in_schema=False,
)
async def api_verify_credentials(
    data: VerifyModelCredentialsSchema,
):
    model_infos = [
        validate_model_info(
            model_schema_id=data.model_schema_id,
            provider_model_id=data.provider_model_id,
            properties_dict=data.properties,
            model_type=data.model_type,
        )
    ]

    # validate credentials
    provider_credentials = validate_credentials(
        model_infos=model_infos,
        credentials_dict=data.credentials,
        encrypted_credentials_dict=data.encrypted_credentials,
    )
    model_schema, provider_model_id, properties, model_type = model_infos[0]

    # check if proxy is blacklisted
    if data.proxy:
        for url in CONFIG.PROVIDER_URL_BLACK_LIST:
            if url in data.proxy:
                raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, f"Invalid provider url: {url}")

    try:
        if model_type == ModelType.CHAT_COMPLETION:
            from ..chat_completion.route import chat_completion, chat_completion_stream

            properties: ChatCompletionModelProperties
            error_message = "The model did not return a valid response to pass the verification."
            config = ChatCompletionModelConfiguration(**(data.configs if data.configs is not None else {}))
            validate_chat_completion_model(
                model_schema, properties.streaming, properties.function_call, properties.vision, config, verify=True
            )
            if model_schema.type == ModelType.WILDCARD or model_schema.provider_id == "custom_host":
                if not properties.function_call:
                    message = ChatCompletionUserMessage.model_validate(
                        {"role": "user", "content": "Only say your name"}
                    )
                    setattr(config, "max_tokens", 10)
                    if not properties.streaming:
                        response = await chat_completion(
                            model_infos=model_infos,
                            messages=[message],
                            credentials=provider_credentials,
                            configs=config,
                            proxy=data.proxy,
                            custom_headers=data.custom_headers,
                        )
                        if response.message.content is None:
                            raise_http_error(ErrorCode.CREDENTIALS_VALIDATION_ERROR, error_message)
                    else:
                        valid_response_received = False
                        async for response in chat_completion_stream(
                            model_infos=model_infos,
                            messages=[message],
                            credentials=provider_credentials,
                            configs=config,
                            proxy=data.proxy,
                            custom_headers=data.custom_headers,
                        ):
                            if isinstance(response, ChatCompletion) and response.message.content is not None:
                                valid_response_received = True
                        if not valid_response_received:
                            raise_http_error(ErrorCode.CREDENTIALS_VALIDATION_ERROR, error_message)
                else:
                    if hasattr(config, "max_tokens"):
                        delattr(config, "max_tokens")
                    function_dict = {
                        "name": "make_scatter_plot",
                        "description": "Generate a scatter plot from the given data",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "x_values": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "description": "The x-axis values for the data points",
                                },
                                "y_values": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "description": "The y-axis values for the data points",
                                },
                            },
                            "required": ["x_values", "y_values"],
                        },
                    }
                    message = ChatCompletionUserMessage.model_validate(
                        {"role": "user", "content": "Make a scatter plot with x_values 1, 2 and y_values 3, 4"}
                    )
                    if not properties.streaming:
                        response = await chat_completion(
                            model_infos=model_infos,
                            messages=[message],
                            credentials=provider_credentials,
                            configs=config,
                            functions=[ChatCompletionFunction(**function_dict)],
                            proxy=data.proxy,
                            custom_headers=data.custom_headers,
                        )
                        if response.message.content is None and not response.message.function_calls:
                            raise_http_error(ErrorCode.CREDENTIALS_VALIDATION_ERROR, error_message)
                    else:
                        valid_response_received = False
                        async for response in chat_completion_stream(
                            model_infos=model_infos,
                            messages=[message],
                            credentials=provider_credentials,
                            configs=config,
                            functions=[ChatCompletionFunction(**function_dict)],
                            proxy=data.proxy,
                            custom_headers=data.custom_headers,
                        ):
                            if isinstance(response, ChatCompletion) and (
                                response.message.content is not None or response.message.function_calls
                            ):
                                valid_response_received = True
                        if not valid_response_received:
                            raise_http_error(ErrorCode.CREDENTIALS_VALIDATION_ERROR, error_message)
            else:
                message = ChatCompletionUserMessage.model_validate({"role": "user", "content": "Only say your name"})
                setattr(config, "max_tokens", 10)
                response = await chat_completion(
                    model_infos=model_infos,
                    messages=[message],
                    credentials=provider_credentials,
                    configs=config,
                    proxy=data.proxy,
                    custom_headers=data.custom_headers,
                )
                if response.message.content is None:
                    raise_http_error(ErrorCode.CREDENTIALS_VALIDATION_ERROR, error_message)
        elif model_type == ModelType.TEXT_EMBEDDING:
            from ..text_embedding.route import embed_text

            properties: TextEmbeddingModelProperties
            response = await embed_text(
                provider_id=model_schema.provider_id,
                provider_model_id=provider_model_id,
                input=["Hello"],
                credentials=provider_credentials,
                properties=properties,
                configs=TextEmbeddingModelConfiguration(),
                input_type=None,
                proxy=data.proxy,
                custom_headers=data.custom_headers,
            )
            actual_embedding_size = len(response.data[0].embedding)
            if not actual_embedding_size == properties.embedding_size:
                raise_http_error(
                    ErrorCode.CREDENTIALS_VALIDATION_ERROR,
                    f"The actual embedding size {actual_embedding_size} is not {properties.embedding_size}",
                )

        elif model_type == ModelType.RERANK:
            from app.cache import get_rerank_model

            model = get_rerank_model(provider_id=model_schema.provider_id)
            response = await model.rerank(
                provider_model_id=provider_model_id,
                query="skin",
                documents=[
                    "Organic cotton baby clothes for sensitive skin",
                ],
                top_n=3,
                credentials=provider_credentials,
                proxy=data.proxy,
                custom_headers=data.custom_headers,
            )
        else:
            raise_http_error(
                ErrorCode.REQUEST_VALIDATION_ERROR,
                message=f"model_type {model_type} is not valid",
            )

    except TKHttpException as e:
        if isinstance(getattr(e, "detail"), dict):
            message = e.detail.get("message")
            if message:
                message = " " + message
            e.detail["message"] = f"Model credentials validation failed.{message}"
        raise e
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
        raise_http_error(
            ErrorCode.CREDENTIALS_VALIDATION_ERROR,
            message="Model credentials validation has failed. Please check whether your credentials are correct "
            "and if you have enough quota with the provider. " + "More details: " + str(e),
        )

    provider_credentials.encrypt()
    return BaseSuccessDataResponse(
        data={
            "provider_id": model_schema.provider_id,
            "model_schema_id": model_schema.model_schema_id,
            "provider_model_id": data.provider_model_id,
            "properties": properties,
            "model_type": model_type,
            "encrypted_credentials": provider_credentials.credentials,
        }
    )
