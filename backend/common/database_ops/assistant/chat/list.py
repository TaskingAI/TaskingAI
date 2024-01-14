from common.database.postgres.pool import postgres_db_pool
from common.models import Chat, SortOrderEnum, Assistant
from typing import Optional, Tuple, List
from typing import Dict
from common.database_ops.utils import get_object_total, list_objects


async def get_chat_total(prefix_filters: Dict, equal_filters: Dict) -> int:
    """
    Get total count of chats
    :param prefix_filters: the prefix filters, key is the column name, value is the prefix value
    :param equal_filters: the equal filters, key is the column name, value is the equal value
    :return: total count of chats
    """

    async with postgres_db_pool.get_db_connection() as conn:
        return await get_object_total(
            conn=conn,
            table_name="chat",
            prefix_filters=prefix_filters,
            equal_filters=equal_filters,
        )


async def list_chats(
    assistant: Assistant,
    limit: int,
    order: SortOrderEnum,
    # todo: add different sort field options
    after_chat: Optional[Chat] = None,
    before_chat: Optional[Chat] = None,
    offset: int = 0,
    prefix_filters: Optional[Dict] = None,
    equal_filters: Optional[Dict] = None,
) -> Tuple[List[Chat], int, bool]:
    """
    List chats
    :param assistant: the assistant where the chat belongs to
    :param limit: the limit of the query
    :param order: the order of the query, asc or desc
    :param after_chat: the chat to query after
    :param before_chat: the chat to query before
    :param offset: the offset of the query
    :param prefix_filters: the prefix filters, key is the column name, value is the prefix value
    :param equal_filters: the equal filters, key is the column name, value is the equal value
    :return: a list of chats, total count of chats, and whether there are more chats
    """

    # add assistant_id to equal_filters
    if equal_filters is None:
        equal_filters = {}
    equal_filters["assistant_id"] = assistant.assistant_id

    async with postgres_db_pool.get_db_connection() as conn:
        return await list_objects(
            conn=conn,
            object_class=Chat,
            table_name="chat",
            limit=limit,
            order=order,
            sort_field="created_timestamp",
            after_value=after_chat.created_timestamp if after_chat else None,
            before_value=before_chat.created_timestamp if before_chat else None,
            offset=offset,
            prefix_filters=prefix_filters,
            equal_filters=equal_filters,
        )
