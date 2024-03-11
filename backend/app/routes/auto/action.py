# -*- coding: utf-8 -*-

# action.py

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

from app.operators import action_ops as ops
from app.schemas import *

__all__ = ["auto_add_action_routes"]


def auto_add_action_routes(router: APIRouter):
    @router.get(
        path="/actions/{action_id}",
        tags=["Tool - Action"],
        summary="Get Action",
        operation_id="get_action",
        response_model=ActionGetResponse,
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
        return ActionGetResponse(
            data=entity.to_response_dict(),
        )

    @router.get(
        path="/actions",
        tags=["Tool - Action"],
        summary="List Actions",
        operation_id="list_action",
        response_model=ActionListResponse,
        responses={422: {"description": "Unprocessable Entity"}},
    )
    async def api_list(
        request: Request,
        data: ActionListRequest = Depends(),
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
        return ActionListResponse(
            data=[entity.to_response_dict() for entity in entities],
            fetched_count=len(entities),
            has_more=has_more,
        )

    @router.delete(
        path="/actions/{action_id}",
        tags=["Tool - Action"],
        summary="Delete Action",
        operation_id="delete_action",
        response_model=ActionDeleteResponse,
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
        return ActionDeleteResponse()
