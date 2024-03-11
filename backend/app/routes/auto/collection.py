# -*- coding: utf-8 -*-

# collection.py

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

from app.operators import collection_ops as ops
from app.schemas import *

__all__ = ["auto_add_collection_routes"]


def auto_add_collection_routes(router: APIRouter):
    @router.get(
        path="/collections/{collection_id}",
        tags=["Retrieval - Collection"],
        summary="Get Collection",
        operation_id="get_collection",
        response_model=CollectionGetResponse,
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
        return CollectionGetResponse(
            data=entity.to_response_dict(),
        )

    @router.get(
        path="/collections",
        tags=["Retrieval - Collection"],
        summary="List Collections",
        operation_id="list_collection",
        response_model=CollectionListResponse,
        responses={422: {"description": "Unprocessable Entity"}},
    )
    async def api_list(
        request: Request,
        data: CollectionListRequest = Depends(),
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
        return CollectionListResponse(
            data=[entity.to_response_dict() for entity in entities],
            fetched_count=len(entities),
            has_more=has_more,
        )

    @router.post(
        path="/collections",
        tags=["Retrieval - Collection"],
        summary="Create Collection",
        operation_id="create_collection",
        response_model=CollectionCreateResponse,
        responses={422: {"description": "Unprocessable Entity"}},
    )
    async def api_create(
        request: Request,
        data: CollectionCreateRequest,
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
        return CollectionCreateResponse(
            data=entity.to_response_dict(),
        )

    @router.post(
        path="/collections/{collection_id}",
        tags=["Retrieval - Collection"],
        summary="Update Collection",
        operation_id="update_collection",
        response_model=CollectionUpdateResponse,
        responses={422: {"description": "Unprocessable Entity"}},
    )
    async def api_update(
        request: Request,
        data: CollectionUpdateRequest,
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
        return CollectionUpdateResponse(
            data=entity.to_response_dict(),
        )

    @router.delete(
        path="/collections/{collection_id}",
        tags=["Retrieval - Collection"],
        summary="Delete Collection",
        operation_id="delete_collection",
        response_model=CollectionDeleteResponse,
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
        return CollectionDeleteResponse()
