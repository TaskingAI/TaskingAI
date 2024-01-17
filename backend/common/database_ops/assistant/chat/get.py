from common.database.postgres.pool import postgres_db_pool
from common.models import Chat, Assistant


async def get_chat(assistant: Assistant, chat_id: str):
    # 1. get from redis
    assistant_id = assistant.assistant_id
    chat: Chat = await Chat.get_redis(assistant_id, chat_id)
    if chat:
        return chat

    async with postgres_db_pool.get_db_connection() as conn:
        # 2. get from db
        row = await conn.fetchrow("SELECT * FROM chat WHERE assistant_id = $1 AND chat_id = $2", assistant_id, chat_id)

    # 3. return if exists
    if row:
        chat = Chat.build(row)
        await chat.set_redis()
        return chat

    return None
