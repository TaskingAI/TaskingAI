from ..utils import auth_info_required
from fastapi import APIRouter, Depends, Request
from common.services.assistant.chat import *
from app.schemas.assistant.chat import *
from app.schemas.base import BaseSuccessEmptyResponse, BaseSuccessDataResponse, BaseSuccessListResponse, BaseListRequest
from common.models import Chat, SerializePurpose

router = APIRouter()


@router.get(
    "/assistants/{assistant_id}/chats",
    tags=["Assistant"],
    summary="List Chats",
    operation_id="list_chats",
    response_model=BaseSuccessListResponse,
)
async def api_list_chats(
    request: Request,
    assistant_id: str,
    data: BaseListRequest = Depends(),
    auth_info: Dict = Depends(auth_info_required),
):
    chats, total, has_more = await list_chats(
        assistant_id=assistant_id,
        limit=data.limit,
        order=data.order,
        after=data.after,
        before=data.before,
        offset=data.offset,
        id_search=data.id_search,
        name_search=data.name_search,
    )
    return BaseSuccessListResponse(
        data=[chat.to_dict(purpose=SerializePurpose.RESPONSE) for chat in chats],
        fetched_count=len(chats),
        total_count=total,
        has_more=has_more,
    )


@router.get(
    "/assistants/{assistant_id}/chats/{chat_id}",
    tags=["Assistant"],
    summary="Get Chat",
    operation_id="get_chat",
    response_model=BaseSuccessDataResponse,
)
async def api_get_chat(
    chat_id: str,
    request: Request,
    assistant_id: str,
    auth_info: Dict = Depends(auth_info_required),
):
    chat: Chat = await get_chat(
        assistant_id=assistant_id,
        chat_id=chat_id,
    )
    return BaseSuccessDataResponse(data=chat.to_dict(purpose=SerializePurpose.RESPONSE))


@router.post(
    "/assistants/{assistant_id}/chats",
    tags=["Assistant"],
    summary="Bulk create chat",
    operation_id="bulk_create_chat",
    response_model=BaseSuccessDataResponse,
)
async def api_create_chats(
    request: Request,
    data: ChatCreateRequest,
    assistant_id: str,
    auth_info: Dict = Depends(auth_info_required),
):
    chat: Chat = await create_chat(
        assistant_id=assistant_id,
        metadata=data.metadata,
    )
    return BaseSuccessDataResponse(
        data=chat.to_dict(
            purpose=SerializePurpose.RESPONSE,
        )
    )


@router.post(
    "/assistants/{assistant_id}/chats/{chat_id}",
    tags=["Assistant"],
    summary="Update Chat",
    operation_id="update_chat",
    response_model=BaseSuccessDataResponse,
)
async def api_update_chat(
    chat_id: str,
    request: Request,
    data: ChatUpdateRequest,
    assistant_id: str,
    auth_info: Dict = Depends(auth_info_required),
):
    chat: Chat = await update_chat(
        assistant_id=assistant_id,
        chat_id=chat_id,
        metadata=data.metadata,
    )
    return BaseSuccessDataResponse(data=chat.to_dict(purpose=SerializePurpose.RESPONSE))


@router.delete(
    "/assistants/{assistant_id}/chats/{chat_id}",
    tags=["Chat"],
    summary="Delete Chat",
    operation_id="delete_chat",
    response_model=BaseSuccessEmptyResponse,
)
async def api_delete_chat(
    chat_id: str,
    request: Request,
    assistant_id: str,
    auth_info: Dict = Depends(auth_info_required),
):
    await delete_chat(
        assistant_id=assistant_id,
        chat_id=chat_id,
    )
    return BaseSuccessEmptyResponse()
