from common.database.postgres.pool import postgres_db_pool
from .get import get_apikey
from common.models import Apikey
from typing import Dict
from common.database_ops.utils import update_object


async def update_apikey(apikey: Apikey, update_dict: Dict):
    # 1. Pop from redis
    await apikey.pop_redis()

    # 2. Update database
    async with postgres_db_pool.get_db_connection() as conn:
        await update_object(
            conn, update_dict, update_time=True, table_name="apikey", equal_filters={"apikey_id": apikey.apikey_id}
        )

    # 3. get the new object and cache
    apikey = await get_apikey(apikey.apikey_id)

    return apikey
