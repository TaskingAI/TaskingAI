from ..utils import auth_info_required
from fastapi import APIRouter, Depends, Request
from common.database.postgres.pool import postgres_db_pool
from common.services.assistant.message import *
from app.schemas.assistant.message import *
from app.schemas.base import BaseSuccessDataResponse, BaseSuccessListResponse
from common.models import Message, SerializePurpose
from typing import Dict

router = APIRouter()


@router.get(
    "/assistants/{assistant_id}/chats/{chat_id}/messages",
    tags=["Assistant"],
    summary="List Messages",
    operation_id="list_messages",
    response_model=BaseSuccessListResponse,
)
async def api_list_messages(
    request: Request,
    assistant_id: str,
    chat_id: str,
    data: MessageListRequest = Depends(),
    auth_info: Dict = Depends(auth_info_required),
    postgres_conn=Depends(postgres_db_pool.get_db_connection),
):
    messages, total, has_more = await list_messages(
        postgres_conn,
        assistant_id=assistant_id,
        chat_id=chat_id,
        limit=data.limit,
        order=data.order,
        after=data.after,
        before=data.before,
    )
    return BaseSuccessListResponse(
        data=[message.to_dict(purpose=SerializePurpose.RESPONSE) for message in messages],
        fetched_count=len(messages),
        total_count=total,
        has_more=has_more,
    )


@router.get(
    "/assistants/{assistant_id}/chats/{chat_id}/messages/{message_id}",
    tags=["Assistant"],
    summary="Get Message",
    operation_id="get_message",
    response_model=BaseSuccessDataResponse,
)
async def api_get_message(
    message_id: str,
    request: Request,
    assistant_id: str,
    chat_id: str,
    auth_info: Dict = Depends(auth_info_required),
    postgres_conn=Depends(postgres_db_pool.get_db_connection),
):
    message: Message = await get_message(
        postgres_conn=postgres_conn,
        assistant_id=assistant_id,
        chat_id=chat_id,
        message_id=message_id,
    )
    return BaseSuccessDataResponse(data=message.to_dict(purpose=SerializePurpose.RESPONSE))


@router.post(
    "/assistants/{assistant_id}/chats/{chat_id}/messages",
    tags=["Assistant"],
    summary="Bulk create message",
    operation_id="bulk_create_message",
    response_model=BaseSuccessDataResponse,
)
async def api_create_messages(
    request: Request,
    data: MessageCreateRequest,
    assistant_id: str,
    chat_id: str,
    auth_info: Dict = Depends(auth_info_required),
    postgres_conn=Depends(postgres_db_pool.get_db_connection),
):
    message: Message = await create_message(
        postgres_conn=postgres_conn,
        assistant_id=assistant_id,
        chat_id=chat_id,
        role=data.role,
        content=data.content,
        metadata=data.metadata,
    )
    return BaseSuccessDataResponse(
        data=message.to_dict(
            purpose=SerializePurpose.RESPONSE,
        )
    )


@router.post(
    "/assistants/{assistant_id}/chats/{chat_id}/messages/{message_id}",
    tags=["Assistant"],
    summary="Update Message",
    operation_id="update_message",
    response_model=BaseSuccessDataResponse,
)
async def api_update_message(
    message_id: str,
    request: Request,
    data: MessageUpdateRequest,
    assistant_id: str,
    chat_id: str,
    auth_info: Dict = Depends(auth_info_required),
    postgres_conn=Depends(postgres_db_pool.get_db_connection),
):
    message: Message = await update_message(
        postgres_conn=postgres_conn,
        assistant_id=assistant_id,
        chat_id=chat_id,
        message_id=message_id,
        metadata=data.metadata,
    )
    return BaseSuccessDataResponse(data=message.to_dict(purpose=SerializePurpose.RESPONSE))
