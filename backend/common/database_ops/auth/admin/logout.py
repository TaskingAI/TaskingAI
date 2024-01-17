from common.database.postgres.pool import postgres_db_pool
from common.models import Admin
from common.database_ops.utils import current_timestamp_int_milliseconds


async def logout_admin(admin: Admin):
    # 1. remove token
    async with postgres_db_pool.get_db_connection() as conn:
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
    await admin.pop_redis()

    return admin
