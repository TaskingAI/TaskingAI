from typing import Optional, Dict
from common.models import Chat, Message, MessageContent, SortOrderEnum, ListResult, MessageRole
from common.database_ops import message as db_message
from common.error import ErrorCode, raise_http_error
from .chat import get_chat

__all__ = [
    "list_messages",
    "create_message",
    "update_message",
    "get_message",
]


async def validate_and_get_message(postgres_conn, chat: Chat, message_id: str) -> Message:
    message = await db_message.get_message(postgres_conn, chat, message_id)
    if not message:
        raise_http_error(ErrorCode.OBJECT_NOT_FOUND, message=f"Message {message_id} not found.")
    return message


async def list_messages(
    postgres_conn,
    assistant_id: str,
    chat_id: str,
    limit: int,
    order: SortOrderEnum,
    after: Optional[str],
    before: Optional[str],
) -> ListResult:
    """
    List messages
    :param postgres_conn: postgres connection
    :param assistant_id: the assistant id
    :param chat_id: the chat id
    :param limit: the limit of the query
    :param order: the order of the query, asc or desc
    :param after: the cursor ID to query after
    :param before: the cursor ID to query before
    :return: a list of messages, total count of messages, and whether there are more messages
    """

    # validate chat
    chat = await get_chat(postgres_conn, assistant_id=assistant_id, chat_id=chat_id)

    # validate after and before
    after_message, before_message = None, None

    if after:
        after_message = await validate_and_get_message(postgres_conn, chat, after)

    if before:
        before_message = await validate_and_get_message(postgres_conn, chat, before)

    return await db_message.list_messages(
        postgres_conn=postgres_conn,
        chat=chat,
        limit=limit,
        order=order,
        after_message=after_message,
        before_message=before_message,
    )


async def create_message(
    postgres_conn,
    assistant_id: str,
    chat_id: str,
    role: MessageRole,
    content: MessageContent,
    metadata: Dict[str, str],
) -> Message:
    """
    Create message
    :param postgres_conn: postgres connection
    :param assistant_id: the assistant id
    :param chat_id: the chat id
    :param role: the message role, user or assistant
    :param content: the message content
    :param metadata: the message metadata
    :return: the created message
    """

    # validate chat
    chat: Chat = await get_chat(postgres_conn, assistant_id=assistant_id, chat_id=chat_id)

    # create message
    message = await db_message.create_message(
        postgres_conn=postgres_conn,
        chat=chat,
        role=role,
        content=content,  # todo check content type
        metadata=metadata,
    )
    return message


async def update_message(
    postgres_conn,
    assistant_id: str,
    chat_id: str,
    message_id: str,
    metadata: Optional[Dict[str, str]],
) -> Message:
    """
    Update message
    :param postgres_conn: postgres connection
    :param assistant_id: the assistant id
    :param chat_id: the chat id
    :param message_id: the message id
    :param metadata: the message metadata to update
    :return: the updated message
    """

    # validate chat
    chat: Chat = await get_chat(postgres_conn, assistant_id=assistant_id, chat_id=chat_id)
    message: Message = await validate_and_get_message(postgres_conn, chat=chat, message_id=message_id)

    update_dict = {}

    if metadata:
        update_dict["metadata"] = metadata

    if update_dict:
        message = await db_message.update_message(
            conn=postgres_conn,
            chat=chat,
            message=message,
            update_dict=update_dict,
        )

    return message


async def get_message(postgres_conn, assistant_id: str, chat_id: str, message_id: str) -> Message:
    """
    Get message
    :param postgres_conn: postgres connection
    :param assistant_id: the assistant id
    :param chat_id: the chat id
    :param message_id: the message id
    :return: the message
    """

    # get chat
    chat: Chat = await get_chat(postgres_conn, assistant_id=assistant_id, chat_id=chat_id)
    message: Message = await validate_and_get_message(postgres_conn, chat, message_id)
    return message
