from fastapi import APIRouter, Depends, Request
from typing import List, Dict

from app.schemas import *
from tkhelper.schemas.base import BaseDataResponse
from app.models import Action
from app.services.tool import bulk_create_actions, update_action, run_action

from ..utils import auth_info_required

router = APIRouter()


@router.post(
    "/actions/bulk_create",
    tags=["Tool"],
    summary="Bulk Create Action",
    operation_id="bulk_create_action",
    response_model=BaseDataResponse,
)
async def api_bulk_create_actions(
    request: Request,
    data: ActionBulkCreateRequest,
    auth_info: Dict = Depends(auth_info_required),
):
    actions: List[Action] = await bulk_create_actions(
        openapi_schema=data.openapi_schema,
        authentication=data.authentication,
    )
    results = [action.to_response_dict() for action in actions]
    return BaseDataResponse(data=results)


@router.post(
    "/actions/{action_id}",
    tags=["Tool"],
    summary="Update Action",
    operation_id="update_action",
    response_model=BaseDataResponse,
)
async def api_update_action(
    action_id: str,
    request: Request,
    data: ActionUpdateRequest,
    auth_info: Dict = Depends(auth_info_required),
):
    action: Action = await update_action(
        action_id=action_id,
        openapi_schema=data.openapi_schema,
        authentication=data.authentication,
    )
    return BaseDataResponse(data=action.to_response_dict())


@router.post(
    "/actions/{action_id}/run",
    tags=["Tool"],
    summary="Run Action",
    operation_id="run_action",
    response_model=BaseDataResponse,
)
async def api_run_action(
    action_id: str,
    request: Request,
    data: ActionRunRequest,
    auth_info: Dict = Depends(auth_info_required),
):
    response: Dict = await run_action(
        action_id=action_id,
        parameters=data.parameters,
    )
    return BaseDataResponse(data=response)
