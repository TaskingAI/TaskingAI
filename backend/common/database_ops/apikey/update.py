from .get import get_apikey
from common.models import Apikey
from typing import Dict
from .redis import redis_pop_apikey
from ..utils import prepare_and_execute_update


async def update_apikey(conn, apikey: Apikey, update_dict: Dict):
    # 1. Pop from redis
    await redis_pop_apikey(apikey=apikey)

    # 2. Update database
    await prepare_and_execute_update(
        conn, update_dict, update_time=True, table_name="apikey", condition_fields={"apikey_id": apikey.apikey_id}
    )

    # 3. get the new object and cache
    apikey = await get_apikey(conn, apikey.apikey_id)

    return apikey
