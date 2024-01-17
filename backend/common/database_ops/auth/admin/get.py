from common.database.postgres.pool import postgres_db_pool
from common.models import Admin
import logging

logger = logging.getLogger(__name__)


async def get_admin_by_id(
    admin_id: str,
):
    # 1. get from redis
    admin: Admin = await Admin.get_redis_by_id(admin_id)
    if admin:
        return admin

    # 2. get from database
    async with postgres_db_pool.get_db_connection() as conn:
        row = await conn.fetchrow(
            """
            SELECT * FROM app_admin WHERE admin_id = $1
        """,
            admin_id,
        )

    # 3. write to redis and return
    if row:
        admin = Admin.build(row)
        await admin.set_redis()
        return admin

    return None


async def get_admin_by_username(
    username: str,
):
    # 1. get from redis
    admin: Admin = await Admin.get_redis_by_username(username)
    if admin:
        return admin

    # 2. get from database
    async with postgres_db_pool.get_db_connection() as conn:
        row = await conn.fetchrow(
            """
            SELECT * FROM app_admin WHERE username = $1
        """,
            username,
        )

    # 3. write to redis and return
    if row:
        admin = Admin.build(row)
        await admin.set_redis()
        return admin

    return None
