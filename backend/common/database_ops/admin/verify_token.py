from config import CONFIG
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from common.error import raise_http_error, ErrorCode
import jwt
from .get import get_admin_by_id


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


async def verify_admin_token(conn, token: str):
    admin_id, user_permissions = decode_jwt(token)
    admin = await get_admin_by_id(conn, admin_id)
    if admin and admin.token == token:
        return admin
    return None
