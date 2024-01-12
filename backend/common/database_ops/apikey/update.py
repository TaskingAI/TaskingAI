from .get import get_apikey
from common.models import Apikey
from typing import Dict
from common.database.redis import redis_object_pop
from ..utils import update_object


async def update_apikey(conn, apikey: Apikey, update_dict: Dict):
    # 1. Pop from redis
    await redis_object_pop(Apikey, apikey.apikey_id)

    # 2. Update database
    await update_object(
        conn, update_dict, update_time=True, table_name="apikey", condition_fields={"apikey_id": apikey.apikey_id}
    )

    # 3. get the new object and cache
    apikey = await get_apikey(conn, apikey.apikey_id)

    return apikey
