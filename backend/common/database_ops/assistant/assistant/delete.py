from common.database.postgres.pool import postgres_db_pool
from common.models import Assistant


async def delete_assistant(assistant: Assistant):
    # 1. pop from redis
    await assistant.pop_redis()

    async with postgres_db_pool.get_db_connection() as conn:
        async with conn.transaction():
            # 2. delete from assistant table
            await conn.execute("DELETE FROM assistant WHERE assistant_id=$1;", assistant.assistant_id)
