from ..utils import auth_info_required
from fastapi import APIRouter, Depends, Request
from common.database.postgres.pool import postgres_db_pool
from common.services.tool.action import *
from app.schemas.tool.action import *
from app.schemas.base import BaseSuccessEmptyResponse, BaseSuccessDataResponse, BaseSuccessListResponse
from common.models import Action, SerializePurpose

router = APIRouter()


@router.get(
    "/actions",
    tags=["Action"],
    summary="List Actions",
    operation_id="list_actions",
    response_model=BaseSuccessListResponse,
)
async def api_list_actions(
    request: Request,
    data: ListActionRequest = Depends(),
    auth_info: Dict = Depends(auth_info_required),
    postgres_conn=Depends(postgres_db_pool.get_db_connection),
):
    actions, total, has_more = await list_actions(
        postgres_conn,
        limit=data.limit,
        order=data.order,
        after=data.after,
        before=data.before,
        offset=data.offset,
        id_search=data.id_search,
        name_search=data.name_search,
    )
    return BaseSuccessListResponse(
        data=[action.to_dict(purpose=SerializePurpose.RESPONSE) for action in actions],
        fetched_count=len(actions),
        total_count=total,
        has_more=has_more,
    )


@router.get(
    "/actions/{action_id}",
    tags=["Action"],
    summary="Get Action",
    operation_id="get_action",
    response_model=BaseSuccessDataResponse,
)
async def api_get_action(
    action_id: str,
    request: Request,
    auth_info: Dict = Depends(auth_info_required),
    postgres_conn=Depends(postgres_db_pool.get_db_connection),
):
    action: Action = await get_action(
        postgres_conn=postgres_conn,
        action_id=action_id,
    )
    return BaseSuccessDataResponse(data=action.to_dict(purpose=SerializePurpose.RESPONSE))


@router.post(
    "/actions/bulk_create",
    tags=["Action"],
    summary="Bulk create action",
    operation_id="bulk_create_action",
    response_model=BaseSuccessDataResponse,
)
async def api_bulk_create_actions(
    request: Request,
    data: BulkCreateActionRequest,
    auth_info: Dict = Depends(auth_info_required),
    postgres_conn=Depends(postgres_db_pool.get_db_connection),
):
    actions: List[Action] = await create_action(
        postgres_conn=postgres_conn,
        openapi_schema=data.openapi_schema,
        authentication=data.authentication,
    )
    results = [action.to_dict(purpose=SerializePurpose.RESPONSE) for action in actions]
    return BaseSuccessDataResponse(data=results)


@router.post(
    "/actions/{action_id}",
    tags=["Action"],
    summary="Update Action",
    operation_id="update_action",
    response_model=BaseSuccessDataResponse,
)
async def api_update_action(
    action_id: str,
    request: Request,
    data: UpdateActionRequest,
    auth_info: Dict = Depends(auth_info_required),
    postgres_conn=Depends(postgres_db_pool.get_db_connection),
):
    action: Action = await update_action(
        postgres_conn=postgres_conn,
        action_id=action_id,
        openapi_schema=data.openapi_schema,
        authentication=data.authentication,
    )
    return BaseSuccessDataResponse(data=action.to_dict(purpose=SerializePurpose.RESPONSE))


@router.delete(
    "/actions/{action_id}",
    tags=["Action"],
    summary="Delete Action",
    operation_id="delete_action",
    response_model=BaseSuccessEmptyResponse,
)
async def api_delete_action(
    action_id: str,
    request: Request,
    auth_info: Dict = Depends(auth_info_required),
    postgres_conn=Depends(postgres_db_pool.get_db_connection),
):
    await delete_action(
        postgres_conn=postgres_conn,
        action_id=action_id,
    )
    return BaseSuccessEmptyResponse()


@router.post(
    "/actions/{action_id}/run",
    tags=["Action"],
    summary="Run Action",
    operation_id="run_action",
    response_model=BaseSuccessDataResponse,
)
async def api_run_action(
    action_id: str,
    request: Request,
    data: RunActionRequest,
    auth_info: Dict = Depends(auth_info_required),
    postgres_conn=Depends(postgres_db_pool.get_db_connection),
):
    response: Dict = await run_action(
        postgres_conn=postgres_conn,
        action_id=action_id,
        parameters=data.parameters,
        headers=data.headers,
    )
    return BaseSuccessDataResponse(data=response)
