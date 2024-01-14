from common.models import Chat
from common.database.redis import redis_object_pop


async def delete_chat(postgres_conn, chat: Chat):
    # 1. pop from redis
    await redis_object_pop(Chat, f"{chat.assistant_id}:{chat.chat_id}")

    async with postgres_conn.transaction():
        # 2. delete from db
        await postgres_conn.execute(
            "DELETE FROM chat WHERE assistant_id=$1 AND chat_id=$2;", chat.assistant_id, chat.chat_id
        )
