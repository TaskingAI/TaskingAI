# -*- coding: utf-8 -*-

# bundle_instance.py

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

from app.operators import bundle_instance_ops as ops
from app.schemas import *

__all__ = ["auto_add_bundle_instance_routes"]


def auto_add_bundle_instance_routes(router: APIRouter):
    @router.get(
        path="/bundle_instances/{bundle_instance_id}",
        tags=["Tool - Plugin"],
        summary="Get BundleInstance",
        operation_id="get_bundle_instance",
        response_model=BundleInstanceGetResponse,
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
        return BundleInstanceGetResponse(
            data=entity.to_response_dict(),
        )

    @router.get(
        path="/bundle_instances",
        tags=["Tool - Plugin"],
        summary="List Bundle Instances",
        operation_id="list_bundle_instance",
        response_model=BundleInstanceListResponse,
        responses={422: {"description": "Unprocessable Entity"}},
    )
    async def api_list(
        request: Request,
        data: BundleInstanceListRequest = Depends(),
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
        return BundleInstanceListResponse(
            data=[entity.to_response_dict() for entity in entities],
            fetched_count=len(entities),
            has_more=has_more,
        )

    @router.post(
        path="/bundle_instances",
        tags=["Tool - Plugin"],
        summary="Create BundleInstance",
        operation_id="create_bundle_instance",
        response_model=BundleInstanceCreateResponse,
        responses={422: {"description": "Unprocessable Entity"}},
    )
    async def api_create(
        request: Request,
        data: BundleInstanceCreateRequest,
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
        return BundleInstanceCreateResponse(
            data=entity.to_response_dict(),
        )

    @router.post(
        path="/bundle_instances/{bundle_instance_id}",
        tags=["Tool - Plugin"],
        summary="Update BundleInstance",
        operation_id="update_bundle_instance",
        response_model=BundleInstanceUpdateResponse,
        responses={422: {"description": "Unprocessable Entity"}},
    )
    async def api_update(
        request: Request,
        data: BundleInstanceUpdateRequest,
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
        return BundleInstanceUpdateResponse(
            data=entity.to_response_dict(),
        )

    @router.delete(
        path="/bundle_instances/{bundle_instance_id}",
        tags=["Tool - Plugin"],
        summary="Delete BundleInstance",
        operation_id="delete_bundle_instance",
        response_model=BundleInstanceDeleteResponse,
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
        return BundleInstanceDeleteResponse()
