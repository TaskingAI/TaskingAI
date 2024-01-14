from common.database.postgres.pool import postgres_db_pool
from common.models import Chat
from common.database.redis import redis_object_pop


async def delete_chat(chat: Chat):
    # 1. pop from redis
    await redis_object_pop(Chat, f"{chat.assistant_id}:{chat.chat_id}")

    async with postgres_db_pool.get_db_connection() as conn:
        async with conn.transaction():
            # 2. delete from db
            await conn.execute(
                "DELETE FROM chat WHERE assistant_id=$1 AND chat_id=$2;", chat.assistant_id, chat.chat_id
            )
