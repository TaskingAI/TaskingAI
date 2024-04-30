from fastapi import APIRouter, Depends, Request
from typing import Dict
from tkhelper.utils import check_http_error, sse_stream_response
from tkhelper.error import raise_request_validation_error
from tkhelper.schemas.base import BaseDataResponse

from app.schemas.model.chat_completion import ChatCompletionRequest
from app.services.inference.chat_completion import chat_completion, chat_completion_stream
from app.services.model.model import get_model
from app.models import Model

from ..utils import auth_info_required

router = APIRouter()


def error_message(code, message: str):
    return {
        "object": "Error",
        "code": code,
        "message": message,
    }


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

    # prepare request
    message_dicts = [message.model_dump() for message in data.messages]
    if data.functions is not None:
        functions = [function.model_dump() for function in data.functions]
    else:
        functions = None

    if functions and not model.allow_function_call():
        raise_request_validation_error(f"Model {model.model_id} does not support function calls.")

    if data.stream:
        if not model.allow_streaming():
            raise_request_validation_error(f"Model {model.model_id} does not support streaming.")

        response = await sse_stream_response(
            chat_completion_stream(
                model=model,
                messages=message_dicts,
                encrypted_credentials=model.encrypted_credentials,
                configs=data.configs,
                function_call=data.function_call,
                functions=functions,
            )
        )

        return response

    else:
        # generate none stream response
        response = await chat_completion(
            model=model,
            messages=message_dicts,
            encrypted_credentials=model.encrypted_credentials,
            configs=data.configs,
            function_call=data.function_call,
            functions=functions,
        )
        check_http_error(response)
        return BaseDataResponse(data=response.json()["data"])
