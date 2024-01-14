from common.database.postgres.pool import postgres_db_pool
from common.models import Assistant, Chat
from .get import get_chat
from typing import Dict
import json


async def create_chat(
    assistant: Assistant,
    metadata: Dict[str, str],
) -> Chat:
    """
    Create chat
    :param assistant: the assistant where the chat belongs to
    :param metadata: the chat metadata
    :return: the created chat
    """

    # generate chat id
    new_chat_id = Chat.generate_random_id()

    async with postgres_db_pool.get_db_connection() as conn:
        async with conn.transaction():
            # 1. insert chat into database
            await conn.execute(
                """
                INSERT INTO chat (chat_id, assistant_id, metadata)
                VALUES ($1, $2, $3)
            """,
                new_chat_id,
                assistant.assistant_id,
                json.dumps(metadata),
            )

    # 2. get and return
    chat = await get_chat(assistant=assistant, chat_id=new_chat_id)

    return chat
