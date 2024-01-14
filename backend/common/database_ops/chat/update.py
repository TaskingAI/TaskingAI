from common.models import Chat, Assistant
from typing import Dict
from ..utils import update_object
from .get import get_chat
from common.database.redis import redis_object_pop


async def update_chat(conn, assistant: Assistant, chat: Chat, update_dict: Dict):
    # 1. pop from redis
    await redis_object_pop(Assistant, f"{chat.assistant_id}:{chat.chat_id}")

    # 2. Update chat in database
    await update_object(
        conn,
        update_dict=update_dict,
        update_time=True,
        table_name="chat",
        condition_fields={"assistant_id": chat.assistant_id, "chat_id": chat.chat_id},
    )

    # 3. Get updated chat
    chat = await get_chat(conn, assistant, chat.chat_id)

    return chat
