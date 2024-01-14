from common.database.postgres.pool import postgres_db_pool
from common.models import Assistant
from common.database.redis import redis_object_pop


async def delete_assistant(assistant: Assistant):
    # 1. pop from redis
    await redis_object_pop(Assistant, assistant.assistant_id)

    async with postgres_db_pool.get_db_connection() as conn:
        async with conn.transaction():
            # 2. delete from assistant table
            await conn.execute("DELETE FROM assistant WHERE assistant_id=$1;", assistant.assistant_id)
