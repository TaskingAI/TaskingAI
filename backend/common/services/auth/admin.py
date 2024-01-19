from common.models import Admin
from common.database_ops.auth import admin as db_admin
from common.error import ErrorCode, raise_http_error
from config import CONFIG


__all__ = [
    "login_admin",
    "logout_admin",
    "verify_admin_token",
    "refresh_admin_token",
    "create_default_admin_if_needed",
]


async def validate_and_get_admin_by_id(admin_id: str) -> Admin:
    admin = await db_admin.get_admin_by_id(admin_id)
    if not admin:
        raise_http_error(ErrorCode.OBJECT_NOT_FOUND, message=f"Admin with admin_id={admin_id} not found.")
    return admin


async def validate_and_get_admin_by_username(username: str) -> Admin:
    admin = await db_admin.get_admin_by_username(username)
    if not admin:
        raise_http_error(ErrorCode.OBJECT_NOT_FOUND, message=f"Admin with username={username} not found.")
    return admin


async def login_admin(username: str, password: str) -> Admin:
    admin = await validate_and_get_admin_by_username(username)
    admin = await db_admin.login_admin(admin, password)
    return admin


async def logout_admin(admin_id: str) -> Admin:
    admin = await validate_and_get_admin_by_id(admin_id)
    admin = await db_admin.logout_admin(admin)
    return admin


async def verify_admin_token(token: str) -> Admin:
    admin: Admin = await db_admin.verify_admin_token(token)
    if not admin:
        raise_http_error(ErrorCode.TOKEN_VALIDATION_FAILED, message="Invalid token")
    return admin


async def refresh_admin_token(admin_id: str) -> Admin:
    admin: Admin = await validate_and_get_admin_by_id(admin_id)
    admin: Admin = await db_admin.refresh_admin_token(admin)
    return admin


async def create_default_admin_if_needed() -> Admin:
    admin = await db_admin.get_admin_by_username(CONFIG.DEFAULT_ADMIN_USERNAME)
    if not admin:
        admin = await db_admin.register_admin(CONFIG.DEFAULT_ADMIN_USERNAME, CONFIG.DEFAULT_ADMIN_PASSWORD)
    return admin
