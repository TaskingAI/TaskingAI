# -*- coding: utf-8 -*-

# assistant.py

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

from app.operators import assistant_ops as ops
from app.schemas import *

__all__ = ["auto_add_assistant_routes"]


def auto_add_assistant_routes(router: APIRouter):
    @router.get(
        path="/assistants/{assistant_id}",
        tags=["Assistant - Assistant"],
        summary="Get Assistant",
        operation_id="get_assistant",
        response_model=AssistantGetResponse,
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
        return AssistantGetResponse(
            data=entity.to_response_dict(),
        )

    @router.get(
        path="/assistants",
        tags=["Assistant - Assistant"],
        summary="List Assistants",
        operation_id="list_assistant",
        response_model=AssistantListResponse,
        responses={422: {"description": "Unprocessable Entity"}},
    )
    async def api_list(
        request: Request,
        data: AssistantListRequest = Depends(),
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
        return AssistantListResponse(
            data=[entity.to_response_dict() for entity in entities],
            fetched_count=len(entities),
            has_more=has_more,
        )

    @router.post(
        path="/assistants",
        tags=["Assistant - Assistant"],
        summary="Create Assistant",
        operation_id="create_assistant",
        response_model=AssistantCreateResponse,
        responses={422: {"description": "Unprocessable Entity"}},
    )
    async def api_create(
        request: Request,
        data: AssistantCreateRequest,
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
        return AssistantCreateResponse(
            data=entity.to_response_dict(),
        )

    @router.post(
        path="/assistants/{assistant_id}",
        tags=["Assistant - Assistant"],
        summary="Update Assistant",
        operation_id="update_assistant",
        response_model=AssistantUpdateResponse,
        responses={422: {"description": "Unprocessable Entity"}},
    )
    async def api_update(
        request: Request,
        data: AssistantUpdateRequest,
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
        return AssistantUpdateResponse(
            data=entity.to_response_dict(),
        )

    @router.delete(
        path="/assistants/{assistant_id}",
        tags=["Assistant - Assistant"],
        summary="Delete Assistant",
        operation_id="delete_assistant",
        response_model=AssistantDeleteResponse,
        responses={422: {"description": "Unprocessable Entity"}},
    )
    async def api_delete(
        request: Request,
        path_params: Dict = Depends(path_params_required),
        auth_info: Dict = Depends(auth_info_required),
    ):
        check_path_params(
            model_operator=ops,
            object_id_required=True,
            path_params=path_params,
        )

        await ops.delete(**path_params)
        return AssistantDeleteResponse()
