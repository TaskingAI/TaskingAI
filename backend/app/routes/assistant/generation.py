from fastapi import APIRouter, Depends, Request
from app.schemas.assistant.message import MessageGenerateRequest
from app.schemas.base import BaseSuccessDataResponse
from starlette.responses import StreamingResponse
from ..utils import auth_info_required
from typing import Dict
from common.services.assistant.generation import NormalSession, StreamSession
from common.services.assistant.chat import is_chat_locked
from common.error import ErrorCode, raise_http_error
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/assistants/{assistant_id}/chats/{chat_id}/generate",
    summary="Generate message",
    operation_id="generate_message",
    tags=["Assistant"],
    responses={422: {"description": "Unprocessable Entity"}},
    description="Generate a new message with the role of 'assistant'.",
    response_model=BaseSuccessDataResponse,
)
async def api_chat_generate(
    request: Request,
    assistant_id: str,
    chat_id: str,
    payload: MessageGenerateRequest,
    auth_info: Dict = Depends(auth_info_required),
):
    system_prompt_variables = payload.system_prompt_variables
    stream = payload.stream

    if await is_chat_locked(assistant_id, chat_id):
        raise_http_error(
            ErrorCode.OBJECT_LOCKED, message="Chat is locked by another generation process. Please try again later."
        )

    if payload.stream or payload.debug:
        session = StreamSession(
            assistant_id=assistant_id,
            chat_id=chat_id,
            stream=payload.stream,
            debug=payload.debug,
        )
        await session.prepare(stream, system_prompt_variables, retrival_log=payload.debug)
        # todo: await lock_chat(assistant_id, chat_id)
        return StreamingResponse(session.stream_generate(), media_type="text/event-stream")

    else:
        session = NormalSession(
            assistant_id=assistant_id,
            chat_id=chat_id,
        )
        await session.prepare(stream, system_prompt_variables, retrival_log=False)
        # await todo: lock_chat(assistant_id, chat_id)
        return await session.generate()
