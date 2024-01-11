from common.models import Admin
from .redis import pop_redis_admin
from ..utils import current_timestamp_int_milliseconds


async def logout_admin(conn, admin: Admin):
    # 1. remove token
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
    await pop_redis_admin(admin)

    return admin
