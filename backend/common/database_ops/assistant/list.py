from common.models import Assistant, SortOrderEnum
from typing import Optional, Tuple, List
from typing import Dict
from ..utils import get_object_total, list_objects


async def get_assistant_total(postgres_conn, prefix_filters: Dict, equal_filters: Dict) -> int:
    """
    Get total count of assistants
    :param postgres_conn: postgres connection
    :param prefix_filters: the prefix filters, key is the column name, value is the prefix value
    :param equal_filters: the equal filters, key is the column name, value is the equal value
    :return: total count of assistants
    """

    return await get_object_total(
        conn=postgres_conn,
        table_name="assistant",
        prefix_filters=prefix_filters,
        equal_filters=equal_filters,
    )


async def list_assistants(
    postgres_conn,
    limit: int,
    order: SortOrderEnum,
    # todo: add different sort field options
    after_assistant: Optional[Assistant] = None,
    before_assistant: Optional[Assistant] = None,
    offset: int = 0,
    prefix_filters: Optional[Dict] = None,
    equal_filters: Optional[Dict] = None,
) -> Tuple[List[Assistant], int, bool]:
    """
    List assistants
    :param postgres_conn: postgres connection
    :param limit: the limit of the query
    :param order: the order of the query, asc or desc
    :param after_assistant: the assistant to query after
    :param before_assistant: the assistant to query before
    :param offset: the offset of the query
    :param prefix_filters: the prefix filters, key is the column name, value is the prefix value
    :param equal_filters: the equal filters, key is the column name, value is the equal value
    :return: a list of assistants, total count of assistants, and whether there are more assistants
    """

    return await list_objects(
        conn=postgres_conn,
        object_class=Assistant,
        table_name="assistant",
        limit=limit,
        order=order,
        sort_field="created_timestamp",
        after_value=after_assistant.created_timestamp if after_assistant else None,
        before_value=before_assistant.created_timestamp if before_assistant else None,
        offset=offset,
        prefix_filters=prefix_filters,
        equal_filters=equal_filters,
    )
