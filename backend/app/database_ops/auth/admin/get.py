from app.database import postgres_pool
from app.models import Admin
import logging

logger = logging.getLogger(__name__)


async def get_admin_by_username(
    username: str,
):
    # 1. get from database
    async with postgres_pool.get_db_connection() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM app_admin WHERE username = $1",
            username,
        )

    # 2. write to redis and return
    if row:
        admin = Admin.build(row)
        return admin

    return None
