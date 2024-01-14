from common.models import Chat, Assistant, SerializePurpose
from common.database.redis import redis_object_get_object, redis_object_set_object


async def get_chat(conn, assistant: Assistant, chat_id: str):
    # 1. get from redis
    assistant_id = assistant.assistant_id
    chat: Chat = await redis_object_get_object(Assistant, key=f"{assistant_id}:{chat_id}")
    if chat:
        return chat

    # 2. get from db
    row = await conn.fetchrow("SELECT * FROM chat WHERE assistant_id = $1 AND chat_id = $2", assistant_id, chat_id)

    # 3. return if exists
    if row:
        chat = Chat.build(row)
        await redis_object_set_object(Chat, key=chat_id, value=chat.to_dict(purpose=SerializePurpose.REDIS))
        return chat

    return None
