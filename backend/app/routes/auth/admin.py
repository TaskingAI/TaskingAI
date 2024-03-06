from ..utils import auth_info_required
from fastapi import APIRouter, Depends, Request
from typing import Dict
from app.schemas.auth.admin import *
from tkhelper.schemas.base import BaseEmptyResponse, BaseDataResponse
from app.services.auth.admin import *
from app.models import Admin


router = APIRouter()


@router.post(
    "/admins/login",
    tags=["Admin"],
    summary="Login Admin",
    operation_id="login_admin",
    response_model=BaseDataResponse,
)
async def api_login_admin(
    request: Request,
    data: AdminLoginRequest,
):
    admin: Admin = await login_admin(
        username=data.username,
        password=data.password,
    )
    return BaseDataResponse(
        data=admin.to_response_dict(),
    )


@router.post(
    "/admins/logout",
    tags=["Admin"],
    summary="Logout Admin",
    operation_id="logout_admin",
    response_model=BaseEmptyResponse,
)
async def api_logout_admin(
    request: Request,
    auth_info: Dict = Depends(auth_info_required),
):
    await logout_admin(
        admin_id=auth_info["admin_id"],
    )
    return BaseEmptyResponse()


@router.post(
    "/admins/verify_token",
    tags=["Admin"],
    summary="Verify Admin Token",
    operation_id="verify_admin_token",
    response_model=BaseEmptyResponse,
)
async def api_verify_admin_token(
    request: Request,
    auth_info: Dict = Depends(auth_info_required),
):
    return BaseEmptyResponse()


@router.post(
    "/admins/refresh_token",
    tags=["Admin"],
    summary="Refresh Admin Token",
    operation_id="refresh_admin_token",
    response_model=BaseDataResponse,
)
async def api_refresh_admin_token(
    request: Request,
    auth_info: Dict = Depends(auth_info_required),
):
    admin = await refresh_admin_token(
        admin_id=auth_info["admin_id"],
    )
    return BaseDataResponse(
        data=admin.to_response_dict(),
    )
