from typing import Optional, Dict
from common.models import Assistant, Chat, SortOrderEnum, ListResult
from common.database_ops.assistant import chat as db_chat
from common.error import ErrorCode, raise_http_error
from .assistant import validate_and_get_assistant

__all__ = [
    "list_chats",
    "create_chat",
    "update_chat",
    "get_chat",
    "delete_chat",
    "is_chat_locked",
    "lock_chat",
    "unlock_chat",
]


async def validate_and_get_chat(assistant: Assistant, chat_id: str) -> Chat:
    chat = await db_chat.get_chat(assistant, chat_id)
    if not chat:
        raise_http_error(ErrorCode.OBJECT_NOT_FOUND, message=f"Chat {chat_id} not found.")
    return chat


async def list_chats(
    assistant_id: str,
    limit: int,
    order: SortOrderEnum,
    after: Optional[str],
    before: Optional[str],
    offset: Optional[int],
    id_search: Optional[str],
    name_search: Optional[str],
) -> ListResult:
    """
    List chats
    :param assistant_id: the assistant id
    :param limit: the limit of the query
    :param order: the order of the query, asc or desc
    :param after: the cursor ID to query after
    :param before: the cursor ID to query before
    :param offset: the offset of the query
    :param id_search: the chat ID to search for
    :param name_search: the chat name to search for
    :return: a list of chats, total count of chats, and whether there are more chats
    """

    # validate assistant
    assistant = await validate_and_get_assistant(assistant_id=assistant_id)

    # validate after and before
    after_chat, before_chat = None, None

    if after:
        after_chat = await validate_and_get_chat(assistant, after)

    if before:
        before_chat = await validate_and_get_chat(assistant, before)

    return await db_chat.list_chats(
        assistant=assistant,
        limit=limit,
        order=order,
        after_chat=after_chat,
        before_chat=before_chat,
        offset=offset,
        prefix_filters={
            "chat_id": id_search,
            "name": name_search,
        },
    )


async def create_chat(
    assistant_id: str,
    metadata: Dict[str, str],
) -> Chat:
    """
    Create chat
    :param assistant_id: the assistant id
    :param metadata: the chat metadata
    :return: the created chat
    """

    # validate assistant
    assistant: Assistant = await validate_and_get_assistant(assistant_id=assistant_id)

    # create chat
    chat = await db_chat.create_chat(
        assistant=assistant,
        metadata=metadata,
    )
    return chat


async def update_chat(
    assistant_id: str,
    chat_id: str,
    metadata: Optional[Dict[str, str]],
) -> Chat:
    """
    Update chat
    :param assistant_id: the assistant id
    :param chat_id: the chat id
    :param metadata: the chat metadata to update
    :return: the updated chat
    """

    assistant: Assistant = await validate_and_get_assistant(assistant_id=assistant_id)
    chat: Chat = await validate_and_get_chat(assistant=assistant, chat_id=chat_id)

    update_dict = {}

    if metadata:
        update_dict["metadata"] = metadata

    if update_dict:
        chat = await db_chat.update_chat(
            assistant=assistant,
            chat=chat,
            update_dict=update_dict,
        )

    return chat


async def get_chat(assistant_id: str, chat_id: str) -> Chat:
    """
    Get chat
    :param assistant_id: the assistant id
    :param chat_id: the chat id
    :return: the chat
    """
    assistant: Assistant = await validate_and_get_assistant(assistant_id=assistant_id)
    chat: Chat = await validate_and_get_chat(assistant, chat_id)
    return chat


async def delete_chat(assistant_id: str, chat_id: str) -> None:
    """
    Delete chat
    :param assistant_id: the assistant id
    :param chat_id: the chat id
    """
    assistant: Assistant = await validate_and_get_assistant(assistant_id=assistant_id)
    chat: Chat = await validate_and_get_chat(assistant, chat_id)
    await db_chat.delete_chat(chat)


async def is_chat_locked(assistant_id: str, chat_id: str) -> bool:
    """
    Is chat locked
    :param assistant_id: the assistant id
    :param chat_id : the chat id
    :return: True or False, indicating whether the chat is locked
    """
    return await db_chat.is_chat_locked(assistant_id, chat_id)


async def lock_chat(assistant_id: str, chat_id: str):
    """
    Lock the chat
    :param assistant_id: the assistant id
    :param chat_id: the chat id
    :return:
    """
    await db_chat.set_chat_lock(assistant_id, chat_id, True)


async def unlock_chat(assistant_id: str, chat_id: str):
    """
    Unlock the chat
    :param assistant_id: the assistant id
    :param chat_id: the chat id
    :return:
    """
    await db_chat.set_chat_lock(assistant_id, chat_id, False)
