# -*- coding: utf-8 -*-

# record.py

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

from app.operators import record_ops as ops
from app.schemas import *

__all__ = ["auto_add_record_routes"]


def auto_add_record_routes(router: APIRouter):
    @router.get(
        path="/collections/{collection_id}/records/{record_id}",
        tags=["Retrieval - Record"],
        summary="Get Record",
        operation_id="get_record",
        response_model=RecordGetResponse,
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
        return RecordGetResponse(
            data=entity.to_response_dict(),
        )

    @router.get(
        path="/collections/{collection_id}/records",
        tags=["Retrieval - Record"],
        summary="List Records",
        operation_id="list_record",
        response_model=RecordListResponse,
        responses={422: {"description": "Unprocessable Entity"}},
    )
    async def api_list(
        request: Request,
        data: RecordListRequest = Depends(),
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
        return RecordListResponse(
            data=[entity.to_response_dict() for entity in entities],
            fetched_count=len(entities),
            has_more=has_more,
        )

    @router.post(
        path="/collections/{collection_id}/records",
        tags=["Retrieval - Record"],
        summary="Create Record",
        operation_id="create_record",
        response_model=RecordCreateResponse,
        responses={422: {"description": "Unprocessable Entity"}},
    )
    async def api_create(
        request: Request,
        data: RecordCreateRequest,
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
        return RecordCreateResponse(
            data=entity.to_response_dict(),
        )

    @router.post(
        path="/collections/{collection_id}/records/{record_id}",
        tags=["Retrieval - Record"],
        summary="Update Record",
        operation_id="update_record",
        response_model=RecordUpdateResponse,
        responses={422: {"description": "Unprocessable Entity"}},
    )
    async def api_update(
        request: Request,
        data: RecordUpdateRequest,
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
        return RecordUpdateResponse(
            data=entity.to_response_dict(),
        )

    @router.delete(
        path="/collections/{collection_id}/records/{record_id}",
        tags=["Retrieval - Record"],
        summary="Delete Record",
        operation_id="delete_record",
        response_model=RecordDeleteResponse,
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
        return RecordDeleteResponse()
