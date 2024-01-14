from ..utils import auth_info_required
from fastapi import APIRouter, Depends, Request
from typing import Dict
from common.services.auth.admin import *
from app.schemas.auth.admin import *
from app.schemas.base import BaseSuccessEmptyResponse, BaseSuccessDataResponse
from common.models import Admin, SerializePurpose

router = APIRouter()


@router.post(
    "/admins/login",
    tags=["Admin"],
    summary="Login Admin",
    operation_id="login_admin",
    response_model=BaseSuccessDataResponse,
)
async def api_login_admin(
    request: Request,
    data: AdminLoginRequest,
):
    admin: Admin = await login_admin(
        username=data.username,
        password=data.password,
    )
    return BaseSuccessDataResponse(
        data=admin.to_dict(purpose=SerializePurpose.RESPONSE),
    )


@router.post(
    "/admins/logout",
    tags=["Admin"],
    summary="Logout Admin",
    operation_id="logout_admin",
    response_model=BaseSuccessEmptyResponse,
)
async def api_logout_admin(
    request: Request,
    auth_info: Dict = Depends(auth_info_required),
):
    await logout_admin(
        admin_id=auth_info["admin_id"],
    )
    return BaseSuccessEmptyResponse()


@router.post(
    "/admins/verify_token",
    tags=["Admin"],
    summary="Verify Admin Token",
    operation_id="verify_admin_token",
    response_model=BaseSuccessEmptyResponse,
)
async def api_verify_admin_token(
    request: Request,
    auth_info: Dict = Depends(auth_info_required),
):
    return BaseSuccessEmptyResponse()


@router.post(
    "/admins/refresh_token",
    tags=["Admin"],
    summary="Refresh Admin Token",
    operation_id="refresh_admin_token",
    response_model=BaseSuccessDataResponse,
)
async def api_refresh_admin_token(
    request: Request,
    auth_info: Dict = Depends(auth_info_required),
):
    admin = await refresh_admin_token(
        admin_id=auth_info["admin_id"],
    )
    return BaseSuccessDataResponse(
        data=admin.to_dict(purpose=SerializePurpose.RESPONSE),
    )
