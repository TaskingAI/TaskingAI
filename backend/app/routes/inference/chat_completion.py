from fastapi import APIRouter, Depends, Request
from typing import Dict
from starlette.responses import StreamingResponse
import json

from tkhelper.utils import SSE_DONE_MSG
from tkhelper.error import raise_request_validation_error
from tkhelper.schemas.base import BaseDataResponse

from app.schemas.model.chat_completion import ChatCompletionRequest
from app.services.inference.chat_completion import chat_completion, stream_chat_completion
from app.services.assistant.generation import StatelessNormalSession, StatelessStreamSession
from app.operators import model_ops, assistant_ops
from app.models import Model, Assistant

from ..utils import auth_info_required, is_model_id, is_assistant_id

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
    if is_model_id(model_id=data.model_id):
        # validate model
        model: Model = await model_ops.get(model_id=data.model_id)

        # check function call ability
        functions = [function.model_dump() for function in data.functions] if data.functions is not None else None
        if functions and not model.allow_function_call():
            raise_request_validation_error(f"Model {model.model_id} does not support function calls.")

        # prepare messages
        messages = [message.model_dump() for message in data.messages]

        # perform chat completion with model
        if data.stream:
            if not model.allow_streaming():
                raise_request_validation_error(f"Model {model.model_id} does not support streaming.")

            async def generator():
                async for chunk_dict in await stream_chat_completion(
                    model=model,
                    messages=messages,
                    configs=data.configs,
                    function_call=data.function_call,
                    functions=functions,
                ):
                    yield f"data: {json.dumps(chunk_dict)}\n\n"
                yield SSE_DONE_MSG

            return StreamingResponse(
                generator(),
                media_type="text/event-stream",
            )

        else:
            # generate none stream response
            response_data = await chat_completion(
                model=model,
                messages=messages,
                configs=data.configs,
                function_call=data.function_call,
                functions=functions,
            )
            return BaseDataResponse(data=response_data)

    elif is_assistant_id(assistant_id=data.model_id):
        # validate assistant
        assistant: Assistant = await assistant_ops.get(assistant_id=data.model_id)

        # perform chat completion with assistant
        if data.stream:
            session = StatelessStreamSession(
                assistant=assistant,
                save_logs=False,  # todo: enable save_logs
            )
            return StreamingResponse(
                session.stream_generate(data.messages, data.functions),
                media_type="text/event-stream",
            )
        else:
            session = StatelessNormalSession(
                assistant=assistant,
                save_logs=False,  # todo: enable save_logs
            )
            return await session.generate(data.messages, data.functions)
