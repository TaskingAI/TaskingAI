from common.models import Admin
from .redis import set_redis_admin, get_redis_admin_by_id, get_redis_admin_by_username
import logging

logger = logging.getLogger(__name__)


async def get_admin_by_id(
    conn,
    admin_id: str,
):
    # 1. get from redis
    redis_admin: Admin = await get_redis_admin_by_id(admin_id)
    if redis_admin:
        return redis_admin

    # 2. get from database
    row = await conn.fetchrow(
        """
        SELECT * FROM app_admin WHERE admin_id = $1
    """,
        admin_id,
    )

    # 3. write to redis and return
    if row:
        admin = Admin.build(row)
        await set_redis_admin(admin)
        return admin

    return None


async def get_admin_by_username(
    conn,
    username: str,
):
    # 1. get from redis
    admin: Admin = await get_redis_admin_by_username(username)
    if admin:
        return admin

    # 2. get from database
    row = await conn.fetchrow(
        """
        SELECT * FROM app_admin WHERE username = $1
    """,
        username,
    )

    # 3. write to redis and return
    if row:
        admin = Admin.build(row)
        await set_redis_admin(admin)
        return admin

    return None
