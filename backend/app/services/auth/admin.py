import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from tkhelper.error import ErrorCode, raise_http_error

from app.models import Admin
from app.operators import admin_ops
from app.config import CONFIG
from app.database_ops.auth import admin as db_admin


__all__ = [
    "login_admin",
    "logout_admin",
    "verify_admin_token",
    "refresh_admin_token",
    "create_default_admin_if_needed",
]


def decode_jwt(token: str):
    try:
        payload = jwt.decode(token, CONFIG.JWT_SECRET_KEY, algorithms=["HS256"])

        user_id = payload["sub"]
        user_permissions = payload["permissions"]

        return user_id, user_permissions

    except ExpiredSignatureError:
        raise_http_error(ErrorCode.TOKEN_VALIDATION_FAILED, message="Token has expired")

    except InvalidTokenError:
        raise_http_error(ErrorCode.TOKEN_VALIDATION_FAILED, message="Invalid token")

    except Exception as e:
        raise_http_error(ErrorCode.TOKEN_VALIDATION_FAILED, message="Unknown token error")


async def validate_and_get_admin_by_id(admin_id: str) -> Admin:
    admin = await admin_ops.get(admin_id=admin_id)
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
    admin_id, user_permissions = decode_jwt(token)
    admin = await admin_ops.get(admin_id=admin_id)
    if admin and admin.token == token:
        return admin

    else:
        raise_http_error(ErrorCode.TOKEN_VALIDATION_FAILED, message="Invalid token")


async def refresh_admin_token(admin_id: str) -> Admin:
    admin: Admin = await validate_and_get_admin_by_id(admin_id)
    admin: Admin = await db_admin.refresh_admin_token(admin)
    return admin


async def create_default_admin_if_needed() -> Admin:
    admin = await db_admin.get_admin_by_username(CONFIG.DEFAULT_ADMIN_USERNAME)
    if not admin:
        admin = await db_admin.register_admin(CONFIG.DEFAULT_ADMIN_USERNAME, CONFIG.DEFAULT_ADMIN_PASSWORD)
    return admin
