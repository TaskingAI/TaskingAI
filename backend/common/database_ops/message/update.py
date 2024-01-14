from common.models import Message, Chat
from typing import Dict
from ..utils import update_object
from .get import get_message


async def update_message(conn, chat: Chat, message: Message, update_dict: Dict):
    # 1. Update message in database
    await update_object(
        conn,
        update_dict=update_dict,
        update_time=True,
        table_name="message",
        condition_fields={
            "assistant_id": message.assistant_id,
            "chat_id": message.chat_id,
            "message_id": message.message_id,
        },
    )

    # 2. Get updated message
    message = await get_message(conn, chat, message.message_id)

    return message
