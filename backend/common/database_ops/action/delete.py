from common.models.action import Action
from common.database.redis import redis_object_pop


async def delete_action(postgres_conn, action: Action):
    # 1. pop from redis
    await redis_object_pop(Action, action.action_id)

    # 2. delete from db
    await postgres_conn.execute("DELETE FROM action WHERE action_id=$1;", action.action_id)
