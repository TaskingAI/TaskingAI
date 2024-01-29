from common.database.postgres.pool import postgres_db_pool
from common.models import Action


async def get_action(action_id: str):
    # 1. get from redis
    action: Action = await Action.get_redis(action_id)
    if action:
        return action

    # 2. get from db
    async with postgres_db_pool.get_db_connection() as conn:
        row = await conn.fetchrow(
            """
            SELECT * FROM action WHERE action_id = $1
        """,
            action_id,
        )

    # 3. write to redis and return
    if row:
        action = Action.build(row)
        await action.set_redis()
        return action

    return None
