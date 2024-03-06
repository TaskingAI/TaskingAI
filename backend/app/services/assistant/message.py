from typing import Dict

from app.models import Message, MessageRole, MessageContent
from app.operators import message_ops

__all__ = [
    "create_message",
]


async def create_message(
    assistant_id: str,
    chat_id: str,
    role: MessageRole,
    content: MessageContent,
    metadata: Dict[str, str],
) -> Message:
    """
    Create message
    :param assistant_id: the assistant id
    :param chat_id: the chat id
    :param role: the message role
    :param content: the message content
    :param metadata: the message metadata
    :return: the created message
    """

    # create message
    message: Message = await message_ops.create(
        assistant_id=assistant_id,
        chat_id=chat_id,
        create_dict={
            "role": role,
            "content": content,
            "metadata": metadata,
        },
    )

    return message
