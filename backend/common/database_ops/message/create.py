from common.models import Chat, Message
from .get import get_message
from typing import Dict
from common.models.message import MessageRole
import json


async def create_message(
    postgres_conn,
    chat: Chat,
    role: MessageRole,
    content: Dict,
    metadata: Dict[str, str],
) -> Message:
    """
    Create message
    :param postgres_conn: postgres connection
    :param chat: the chat where the message belongs to
    :param role: the message role, user or assistant
    :param content: the message content
    :param metadata: the message metadata
    :return: the created message
    """

    # generate message id
    new_message_id = Message.generate_random_id()

    async with postgres_conn.transaction():
        # 1. insert message into database
        await postgres_conn.execute(
            """
            INSERT INTO message (message_id, chat_id, assistant_id, role, content, metadata)
            VALUES ($1, $2, $3, $4, $5, $6)
        """,
            new_message_id,
            chat.chat_id,
            chat.assistant_id,
            role.value,
            json.dumps(content),
            json.dumps(metadata),
        )

    # 2. get and return
    message = await get_message(postgres_conn, chat=chat, message_id=new_message_id)

    return message
