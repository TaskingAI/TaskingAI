from common.models import Message, SortOrderEnum, Chat
from typing import Optional, Tuple, List
from typing import Dict
from ..utils import get_object_total, list_objects


async def get_message_total(postgres_conn, prefix_filters: Dict, equal_filters: Dict) -> int:
    """
    Get total count of messages
    :param postgres_conn: postgres connection
    :param prefix_filters: the prefix filters, key is the column name, value is the prefix value
    :param equal_filters: the equal filters, key is the column name, value is the equal value
    :return: total count of messages
    """

    return await get_object_total(
        conn=postgres_conn,
        table_name="message",
        prefix_filters=prefix_filters,
        equal_filters=equal_filters,
    )


async def list_messages(
    postgres_conn,
    chat: Chat,
    limit: int,
    order: SortOrderEnum,
    # todo: add different sort field options
    after_message: Optional[Message] = None,
    before_message: Optional[Message] = None,
) -> Tuple[List[Message], int, bool]:
    """
    List messages
    :param postgres_conn: postgres connection
    :param chat: the chat where the message belongs to
    :param limit: the limit of the query
    :param order: the order of the query, asc or desc
    :param after_message: the message to query after
    :param before_message: the message to query before
    :return: a list of messages, total count of messages, and whether there are more messages
    """

    # build equal_filters
    equal_filters = {"assistant_id": chat.assistant_id, "chat_id": chat.chat_id}

    return await list_objects(
        conn=postgres_conn,
        object_class=Message,
        table_name="message",
        limit=limit,
        order=order,
        sort_field="created_timestamp",
        after_value=after_message.created_timestamp if after_message else None,
        before_value=before_message.created_timestamp if before_message else None,
        equal_filters=equal_filters,
    )
