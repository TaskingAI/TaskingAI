from common.models import Assistant
from common.database.redis import redis_object_pop


async def delete_assistant(postgres_conn, assistant: Assistant):
    # 1. pop from redis
    await redis_object_pop(Assistant, assistant.assistant_id)

    async with postgres_conn.transaction():
        # 2. delete from assistant table
        await postgres_conn.execute("DELETE FROM assistant WHERE assistant_id=$1;", assistant.assistant_id)
