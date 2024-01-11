from common.models import Admin
from .redis import set_redis_admin
from ..utils import current_timestamp_int_milliseconds
import jwt
from datetime import datetime, timedelta
from config import CONFIG


def generate_token(user_id: str, user_permissions):
    secret_key = CONFIG.JWT_SECRET_KEY
    payload = {
        "sub": user_id,
        "permissions": user_permissions,
        "exp": datetime.utcnow() + timedelta(hours=24 * 7),  # expire in 7 days
    }
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token


async def refresh_admin_token(conn, admin: Admin):
    # 1. generate new token
    current_timestamp = current_timestamp_int_milliseconds()
    token = generate_token(admin.admin_id, [])

    # 2. update token
    await conn.execute(
        """
        UPDATE app_admin SET token = $1, updated_timestamp = $2
        WHERE admin_id = $3
    """,
        token,
        current_timestamp,
        admin.admin_id,
    )

    admin.token = token
    admin.updated_timestamp = current_timestamp

    # 3. write to redis and return
    await set_redis_admin(admin)

    return admin
