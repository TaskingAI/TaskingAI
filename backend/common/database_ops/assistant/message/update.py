from common.database.postgres.pool import postgres_db_pool
from common.models import Message, Chat
from typing import Dict
from common.database_ops.utils import update_object
from .get import get_message


async def update_message(chat: Chat, message: Message, update_dict: Dict):
    # 1. Update message in database
    async with postgres_db_pool.get_db_connection() as conn:
        await update_object(
            conn,
            update_dict=update_dict,
            update_time=True,
            table_name="message",
            equal_filters={
                "assistant_id": message.assistant_id,
                "chat_id": message.chat_id,
                "message_id": message.message_id,
            },
        )

    # 2. Get updated message
    message = await get_message(chat, message.message_id)

    return message
