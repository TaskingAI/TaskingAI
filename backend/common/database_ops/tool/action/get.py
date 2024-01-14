from common.models import Action, SerializePurpose
from common.database.redis import redis_object_get_object, redis_object_set_object


async def get_action(conn, action_id: str):
    # 1. get from redis
    action: Action = await redis_object_get_object(Action, key=action_id)
    if action:
        return action

    # 2. get from db
    row = await conn.fetchrow(
        """
        SELECT * FROM action WHERE action_id = $1
    """,
        action_id,
    )

    # 3. write to redis and return
    if row:
        action = Action.build(row)
        await redis_object_set_object(Action, key=action_id, value=action.to_dict(purpose=SerializePurpose.REDIS))
        return action

    return None
