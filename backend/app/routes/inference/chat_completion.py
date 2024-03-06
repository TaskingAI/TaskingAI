from fastapi import APIRouter, Depends, Request
import json
from typing import Dict
from starlette.responses import StreamingResponse
from ..utils import auth_info_required
from tkhelper.utils import check_http_error
from app.schemas.model.chat_completion import ChatCompletionRequest
from tkhelper.schemas.base import BaseDataResponse
from app.services.inference.chat_completion import chat_completion, chat_completion_stream
from app.services.model.model import get_model
from app.models import Model, ModelSchema, ModelType
from tkhelper.error import raise_http_error, ErrorCode

router = APIRouter()


@router.post(
    "/inference/chat_completion",
    summary="Chat Completion",
    operation_id="chat_completion",
    tags=["Inference"],
    responses={422: {"description": "Unprocessable Entity"}},
    description="Model inference for chat completion.",
    response_model=BaseDataResponse,
)
async def api_chat_completion(
    request: Request,
    data: ChatCompletionRequest,
    auth_info: Dict = Depends(auth_info_required),
):
    # validate model
    model: Model = await get_model(
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
                model_schema_id=model_schema.model_schema_id,
                provider_model_id=model_schema.provider_model_id,
                messages=message_dicts,
                encrypted_credentials=model.encrypted_credentials,
                properties=model.properties,
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
            model_schema_id=model_schema.model_schema_id,
            provider_model_id=model_schema.provider_model_id,
            messages=message_dicts,
            encrypted_credentials=model.encrypted_credentials,
            properties=model.properties,
            configs=data.configs,
            function_call=data.function_call,
            functions=functions,
        )
        check_http_error(response)
        return BaseDataResponse(data=response.json()["data"])
