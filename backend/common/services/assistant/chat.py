from typing import Optional, Dict
from common.models import Assistant, Chat, SortOrderEnum, ListResult
from common.database_ops import chat as db_chat
from common.error import ErrorCode, raise_http_error
from .assistant import validate_and_get_assistant

__all__ = [
    "list_chats",
    "create_chat",
    "update_chat",
    "get_chat",
    "delete_chat",
]


async def validate_and_get_chat(postgres_conn, assistant: Assistant, chat_id: str) -> Chat:
    chat = await db_chat.get_chat(postgres_conn, assistant, chat_id)
    if not chat:
        raise_http_error(ErrorCode.OBJECT_NOT_FOUND, message=f"Chat {chat_id} not found.")
    return chat


async def list_chats(
    postgres_conn,
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
    :param postgres_conn: postgres connection
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
    assistant = await validate_and_get_assistant(postgres_conn, assistant_id=assistant_id)

    # validate after and before
    after_chat, before_chat = None, None

    if after:
        after_chat = await validate_and_get_chat(postgres_conn, assistant, after)

    if before:
        before_chat = await validate_and_get_chat(postgres_conn, assistant, before)

    return await db_chat.list_chats(
        postgres_conn=postgres_conn,
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
    postgres_conn,
    assistant_id: str,
    metadata: Dict[str, str],
) -> Chat:
    """
    Create chat
    :param postgres_conn: postgres connection
    :param assistant_id: the assistant id
    :param metadata: the chat metadata
    :return: the created chat
    """

    # validate assistant
    assistant: Assistant = await validate_and_get_assistant(postgres_conn, assistant_id=assistant_id)

    # create chat
    chat = await db_chat.create_chat(
        postgres_conn=postgres_conn,
        assistant=assistant,
        metadata=metadata,
    )
    return chat


async def update_chat(
    postgres_conn,
    assistant_id: str,
    chat_id: str,
    metadata: Optional[Dict[str, str]],
) -> Chat:
    """
    Update chat
    :param postgres_conn: postgres connection
    :param assistant_id: the assistant id
    :param chat_id: the chat id
    :param metadata: the chat metadata to update
    :return: the updated chat
    """

    assistant: Assistant = await validate_and_get_assistant(postgres_conn, assistant_id=assistant_id)
    chat: Chat = await validate_and_get_chat(postgres_conn, assistant=assistant, chat_id=chat_id)

    update_dict = {}

    if metadata:
        update_dict["metadata"] = metadata

    if update_dict:
        chat = await db_chat.update_chat(
            conn=postgres_conn,
            assistant=assistant,
            chat=chat,
            update_dict=update_dict,
        )

    return chat


async def get_chat(postgres_conn, assistant_id: str, chat_id: str) -> Chat:
    """
    Get chat
    :param postgres_conn: postgres connection
    :param assistant_id: the assistant id
    :param chat_id: the chat id
    :return: the chat
    """
    assistant: Assistant = await validate_and_get_assistant(postgres_conn, assistant_id=assistant_id)
    chat: Chat = await validate_and_get_chat(postgres_conn, assistant, chat_id)
    return chat


async def delete_chat(postgres_conn, assistant_id: str, chat_id: str) -> None:
    """
    Delete chat
    :param postgres_conn: postgres connection
    :param assistant_id: the assistant id
    :param chat_id: the chat id
    """
    assistant: Assistant = await validate_and_get_assistant(postgres_conn, assistant_id=assistant_id)
    chat: Chat = await validate_and_get_chat(postgres_conn, assistant, chat_id)
    await db_chat.delete_chat(postgres_conn, chat)
