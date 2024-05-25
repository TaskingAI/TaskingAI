from fastapi import APIRouter, Depends, Request
from typing import Dict
from starlette.responses import StreamingResponse

from tkhelper.schemas.base import BaseDataResponse

from app.services.assistant import get_assistant_and_chat, StatefulNormalSession, StatefulStreamSession
from app.schemas.assistant.generate import MessageGenerateRequest

from ..utils import auth_info_required

import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/assistants/{assistant_id}/chats/{chat_id}/generate",
    summary="Generate message",
    operation_id="generate_message",
    tags=["Assistant - Message"],
    responses={422: {"description": "Unprocessable Entity"}},
    description="Generate a new message with the role of 'assistant'.",
    response_model=BaseDataResponse,
)
async def api_chat_generate(
    request: Request,
    assistant_id: str,
    chat_id: str,
    payload: MessageGenerateRequest,
    auth_info: Dict = Depends(auth_info_required),
):
    system_prompt_variables = payload.system_prompt_variables

    assistant, chat = await get_assistant_and_chat(assistant_id, chat_id)

    if payload.stream or payload.debug:
        session = StatefulStreamSession(
            assistant=assistant,
            chat=chat,
            stream=payload.stream,
            debug=payload.debug,
            save_logs=False,  # todo: save_logs
        )
        return StreamingResponse(
            session.stream_generate(system_prompt_variables),
            media_type="text/event-stream",
        )

    else:
        session = StatefulNormalSession(
            assistant=assistant,
            chat=chat,
            save_logs=False,  # todo: save_logs
        )
        return await session.generate(system_prompt_variables)
