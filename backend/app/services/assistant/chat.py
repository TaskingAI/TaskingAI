from app.models import Assistant, Chat, ChatMemory
from app.operators import chat_ops, assistant_ops

__all__ = [
    "get_chat",
    "update_chat_memory",
    "get_assistant_and_chat",
]


async def update_chat_memory(
    chat: Chat,
    memory: ChatMemory,
) -> Chat:
    """
    Update the chat memory
    :param chat: the chat to update
    :param memory: the chat memory to update
    :return: the updated chat
    """

    chat = await chat_ops.update(
        assistant_id=chat.assistant_id,
        chat_id=chat.chat_id,
        update_dict={"memory": memory.model_dump()},
    )

    return chat


async def get_chat(
    assistant_id: str,
    chat_id: str,
) -> Chat:
    """
    Get chat
    :param assistant_id: the assistant id
    :param chat_id: the chat id
    :return: the chat
    """
    chat: Chat = await chat_ops.get(
        assistant_id=assistant_id,
        chat_id=chat_id,
    )
    return chat


async def get_assistant_and_chat(
    assistant_id: str,
    chat_id: str,
) -> (Assistant, Chat):
    """
    Get chat
    :param assistant_id: the assistant id
    :param chat_id: the chat id
    :return: the chat
    """
    assistant: Assistant = await assistant_ops.get(
        assistant_id=assistant_id,
    )
    chat: Chat = await chat_ops.get(
        assistant_id=assistant_id,
        chat_id=chat_id,
    )
    return assistant, chat
