from app.database.connection import postgres_pool
from app.models import Admin
from app.database_ops.utils import current_timestamp_int_milliseconds
from app.operators import admin_ops


async def logout_admin(admin: Admin):
    # 1. remove token
    async with postgres_pool.get_db_connection() as conn:
        await conn.execute(
            """
            UPDATE app_admin SET token = NULL, updated_timestamp = $1
            WHERE admin_id = $2
        """,
            current_timestamp_int_milliseconds(),
            admin.admin_id,
        )
    admin.token = None

    # 2. remove from redis
    await admin_ops.redis.pop(admin)

    return admin
