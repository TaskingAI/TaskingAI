from common.models import Action
from typing import Dict
from common.database_ops.utils import update_object
from .get import get_action
from common.database.redis import redis_object_pop


async def update_action(conn, action: Action, update_dict: Dict):
    # 1. pop from redis
    await redis_object_pop(Action, action.action_id)

    # 2. Update action in database
    await update_object(
        conn,
        update_dict=update_dict,
        update_time=True,
        table_name="action",
        condition_fields={"action_id": action.action_id},
    )

    # 3. Get updated action
    action = await get_action(conn, action.action_id)

    return action
