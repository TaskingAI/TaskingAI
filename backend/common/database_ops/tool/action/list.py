from common.models import Action, SortOrderEnum
from typing import Optional, Tuple, List
from typing import Dict
from common.database_ops.utils import get_object_total, list_objects


async def get_action_total(postgres_conn, prefix_filters: Dict, equal_filters: Dict) -> int:
    """
    Get total count of actions
    :param postgres_conn: postgres connection
    :param prefix_filters: the prefix filters, key is the column name, value is the prefix value
    :param equal_filters: the equal filters, key is the column name, value is the equal value
    :return: total count of actions
    """

    return await get_object_total(
        conn=postgres_conn,
        table_name="action",
        prefix_filters=prefix_filters,
        equal_filters=equal_filters,
    )


async def list_actions(
    postgres_conn,
    limit: int,
    order: SortOrderEnum,
    after_action: Optional[Action] = None,
    before_action: Optional[Action] = None,
    offset: int = 0,
    prefix_filters: Optional[Dict] = None,
    equal_filters: Optional[Dict] = None,
) -> Tuple[List[Action], int, bool]:
    """
    List actions
    :param postgres_conn: postgres connection
    :param limit: the limit of the query
    :param order: the order of the query, asc or desc
    :param after_action: the action to query after
    :param before_action: the action to query before
    :param offset: the offset of the query
    :param prefix_filters: the prefix filters, key is the column name, value is the prefix value
    :param equal_filters: the equal filters, key is the column name, value is the equal value
    :return: a list of actions, total count of actions, and whether there are more actions
    """

    # todo: add different sort field options

    return await list_objects(
        conn=postgres_conn,
        object_class=Action,
        table_name="action",
        limit=limit,
        order=order,
        sort_field="created_timestamp",
        after_value=after_action.created_timestamp if after_action else None,
        before_value=before_action.created_timestamp if before_action else None,
        offset=offset,
        prefix_filters=prefix_filters,
        equal_filters=equal_filters,
    )
