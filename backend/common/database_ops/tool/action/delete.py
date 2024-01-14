from common.database.postgres.pool import postgres_db_pool
from common.models import Action
from common.database.redis import redis_object_pop


async def delete_action(action: Action):
    # 1. pop from redis
    await redis_object_pop(Action, action.action_id)

    # 2. delete from db
    async with postgres_db_pool.get_db_connection() as conn:
        await conn.execute("DELETE FROM action WHERE action_id=$1;", action.action_id)
