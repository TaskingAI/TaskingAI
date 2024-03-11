# -*- coding: utf-8 -*-

# message.py

"""
This script is automatically generated for TaskingAI Community server
Do not modify the file manually

Author: James Yao
Organization: TaskingAI
License: Apache 2.0
"""

from fastapi import APIRouter, Request, Depends
from typing import Dict

from ..utils import *

from app.operators import message_ops as ops
from app.schemas import *

__all__ = ["auto_add_message_routes"]


def auto_add_message_routes(router: APIRouter):
    @router.get(
        path="/assistants/{assistant_id}/chats/{chat_id}/messages/{message_id}",
        tags=["Assistant - Message"],
        summary="Get Message",
        operation_id="get_message",
        response_model=MessageGetResponse,
        responses={422: {"description": "Unprocessable Entity"}},
    )
    async def api_get(
        request: Request,
        path_params: Dict = Depends(path_params_required),
        auth_info: Dict = Depends(auth_info_required),
    ):
        check_path_params(
            model_operator=ops,
            object_id_required=True,
            path_params=path_params,
        )

        entity = await ops.get(**path_params)
        return MessageGetResponse(
            data=entity.to_response_dict(),
        )

    @router.get(
        path="/assistants/{assistant_id}/chats/{chat_id}/messages",
        tags=["Assistant - Message"],
        summary="List Messages",
        operation_id="list_message",
        response_model=MessageListResponse,
        responses={422: {"description": "Unprocessable Entity"}},
    )
    async def api_list(
        request: Request,
        data: MessageListRequest = Depends(),
        path_params: Dict = Depends(path_params_required),
        auth_info: Dict = Depends(auth_info_required),
    ):
        check_path_params(
            model_operator=ops,
            object_id_required=False,
            path_params=path_params,
        )

        data_prefix_filter = getattr(data, "prefix_filter", "")
        data_equal_filter = getattr(data, "equal_filter", "")
        prefix_filter_dict, equal_filter_dict = await validate_list_filter(
            model_operator=ops,
            path_params=path_params,
            prefix_filter=data_prefix_filter,
            equal_filter=data_equal_filter,
        )

        entities, has_more = await ops.list(
            limit=data.limit,
            order=data.order,
            after_id=data.after,
            before_id=data.before,
            prefix_filters=prefix_filter_dict,
            equal_filters=equal_filter_dict,
            **path_params,
        )
        return MessageListResponse(
            data=[entity.to_response_dict() for entity in entities],
            fetched_count=len(entities),
            has_more=has_more,
        )

    @router.post(
        path="/assistants/{assistant_id}/chats/{chat_id}/messages",
        tags=["Assistant - Message"],
        summary="Create Message",
        operation_id="create_message",
        response_model=MessageCreateResponse,
        responses={422: {"description": "Unprocessable Entity"}},
    )
    async def api_create(
        request: Request,
        data: MessageCreateRequest,
        path_params: Dict = Depends(path_params_required),
        auth_info: Dict = Depends(auth_info_required),
    ):
        check_path_params(
            model_operator=ops,
            object_id_required=False,
            path_params=path_params,
        )

        entity = await ops.create(
            create_dict=data.model_dump(),
            **path_params,
        )
        return MessageCreateResponse(
            data=entity.to_response_dict(),
        )

    @router.post(
        path="/assistants/{assistant_id}/chats/{chat_id}/messages/{message_id}",
        tags=["Assistant - Message"],
        summary="Update Message",
        operation_id="update_message",
        response_model=MessageUpdateResponse,
        responses={422: {"description": "Unprocessable Entity"}},
    )
    async def api_update(
        request: Request,
        data: MessageUpdateRequest,
        path_params: Dict = Depends(path_params_required),
        auth_info: Dict = Depends(auth_info_required),
    ):
        check_path_params(
            model_operator=ops,
            object_id_required=True,
            path_params=path_params,
        )

        entity = await ops.update(
            update_dict=data.model_dump(exclude_none=True),
            **path_params,
        )
        return MessageUpdateResponse(
            data=entity.to_response_dict(),
        )
