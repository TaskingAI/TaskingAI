import jwt
from datetime import datetime, timedelta

from app.database.connection import postgres_pool
from app.models import Admin
from app.database_ops.utils import current_timestamp_int_milliseconds
from app.config import CONFIG
from app.operators import admin_ops


def generate_token(user_id: str, user_permissions):
    secret_key = CONFIG.JWT_SECRET_KEY
    payload = {
        "sub": user_id,
        "permissions": user_permissions,
        "exp": datetime.utcnow() + timedelta(hours=24 * 7),  # expire in 7 days
    }
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token


async def refresh_admin_token(admin: Admin):
    # 1. generate new token
    current_timestamp = current_timestamp_int_milliseconds()
    token = generate_token(admin.admin_id, [])

    async with postgres_pool.get_db_connection() as conn:
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
    await admin_ops.redis.set(admin)

    return admin
