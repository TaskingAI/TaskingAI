from fastapi import APIRouter, Depends, Request
from common.database.postgres.pool import postgres_db_pool
import json
from typing import Dict
from starlette.responses import StreamingResponse
from ..utils import auth_info_required, check_http_error
from app.schemas.inference.chat_completion import ChatCompletionRequest, ChatCompletionResponse
from common.services.inference.chat_completion import chat_completion, chat_completion_stream
from common.services.model.model import get_model
from common.models import Model, ModelSchema, ModelType
from common.error import raise_http_error, ErrorCode

router = APIRouter()


@router.post(
    "/inference/chat_completion",
    summary="Chat Completion",
    operation_id="chat_completion",
    tags=["Inference"],
    responses={422: {"description": "Unprocessable Entity"}},
    description="Model inference for chat completion.",
    response_model=ChatCompletionResponse,
)
async def api_chat_completion(
    request: Request,
    data: ChatCompletionRequest,
    auth_info: Dict = Depends(auth_info_required),
    postgres_conn=Depends(postgres_db_pool.get_db_connection),
):
    # validate model
    model: Model = await get_model(
        postgres_conn=postgres_conn,
        model_id=data.model_id,
    )

    # validate model type
    model_schema: ModelSchema = model.model_schema()
    if not model_schema.type == ModelType.CHAT_COMPLETION:
        raise_http_error(
            error_code=ErrorCode.REQUEST_VALIDATION_ERROR,
            message=f"Model {model.model_id} is not a text embedding model",
        )

    # prepare request
    message_dicts = [message.model_dump() for message in data.messages]
    if data.functions is not None:
        functions = [function.model_dump() for function in data.functions]
    else:
        functions = None

    if data.stream:

        async def generator():
            i = 0
            async for response_dict in chat_completion_stream(
                provider_id=model_schema.provider_id,
                provider_model_id=model_schema.provider_model_id,
                messages=message_dicts,
                credentials=model.encrypted_credentials,  # todo: use decrypted_credentials
                configs=data.configs,
                function_call=data.function_call,
                functions=functions,
            ):
                yield f"data: {json.dumps(response_dict)}\n\n"
                i += 1
            yield f"data: [DONE]\n\n"

        return StreamingResponse(generator(), media_type="text/event-stream")

    else:
        # generate none stream response
        response = await chat_completion(
            provider_id=model_schema.provider_id,
            provider_model_id=model_schema.provider_model_id,
            messages=message_dicts,
            credentials=model.encrypted_credentials,  # todo: use decrypted_credentials
            configs=data.configs,
            function_call=data.function_call,
            functions=functions,
        )
        check_http_error(response)
        return ChatCompletionResponse(data=response.json()["data"])
