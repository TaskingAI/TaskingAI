from common.database.postgres.pool import postgres_db_pool
from common.models import Action
from typing import Dict
from common.database_ops.utils import update_object
from .get import get_action


async def update_action(action: Action, update_dict: Dict):
    # 1. pop from redis
    await action.pop_redis()

    # 2. Update action in database
    async with postgres_db_pool.get_db_connection() as conn:
        await update_object(
            conn,
            update_dict=update_dict,
            update_time=True,
            table_name="action",
            equal_filters={"action_id": action.action_id},
        )

    # 3. Get updated action
    action = await get_action(action.action_id)

    return action
