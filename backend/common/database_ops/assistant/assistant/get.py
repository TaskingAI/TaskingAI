from common.database.postgres.pool import postgres_db_pool
from common.models import Assistant


async def get_assistant(assistant_id: str):
    # 1. get from redis
    assistant: Assistant = await Assistant.get_redis(assistant_id)
    if assistant:
        return assistant

    # 2. get from db
    async with postgres_db_pool.get_db_connection() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM assistant WHERE assistant_id = $1",
            assistant_id,
        )

    # 3. write to redis and return
    if row:
        assistant = Assistant.build(row)
        await assistant.set_redis()
        return assistant

    return None
