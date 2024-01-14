from common.models import Assistant, Chat
from .get import get_chat
from typing import Dict
import json


async def create_chat(
    postgres_conn,
    assistant: Assistant,
    metadata: Dict[str, str],
) -> Chat:
    """
    Create chat
    :param postgres_conn: postgres connection
    :param assistant: the assistant where the chat belongs to
    :param metadata: the chat metadata
    :return: the created chat
    """

    # generate chat id
    new_chat_id = Chat.generate_random_id()

    async with postgres_conn.transaction():
        # 1. insert chat into database
        await postgres_conn.execute(
            """
            INSERT INTO chat (chat_id, assistant_id, metadata)
            VALUES ($1, $2, $3)
        """,
            new_chat_id,
            assistant.assistant_id,
            json.dumps(metadata),
        )

    # 2. get and return
    chat = await get_chat(postgres_conn, assistant=assistant, chat_id=new_chat_id)

    return chat
