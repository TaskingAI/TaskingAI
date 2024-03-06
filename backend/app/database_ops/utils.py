from typing import Dict
from tkhelper.utils import current_timestamp_int_milliseconds
import json
from typing import Any, Optional
from tkhelper.models import SortOrderEnum, ListResult
import logging

logger = logging.getLogger(__name__)


async def update_object(conn, update_dict: Dict, update_time: bool, table_name: str, equal_filters: Dict) -> None:
    # 2. build update dict
    pg_update_dict = update_dict.copy()
    for key, value in update_dict.items():
        if isinstance(value, (dict, list)):
            pg_update_dict[key] = json.dumps(value)

    timestamp_int = current_timestamp_int_milliseconds()

    # 3. Prepare the SET clause for the update query
    updates = ", ".join(
        f"{key} = ${idx}" for idx, key in enumerate(pg_update_dict.keys(), start=len(equal_filters) + 2)
    )
    if update_time:
        updates += ", updated_timestamp = $1"

    # 4. Prepare the WHERE clause for the update query
    conditions = " AND ".join(f"{key} = ${idx}" for idx, key in enumerate(equal_filters.keys(), start=2))

    # 5. Prepare the final query
    query = f"UPDATE {table_name} SET {updates} WHERE {conditions}"

    # 6. Prepare the arguments for the query
    args = [timestamp_int, *equal_filters.values(), *pg_update_dict.values()]

    # 7. Execute the query
    await conn.execute(query, *args)


async def get_object_total(
    conn,
    table_name: str,
    prefix_filters: Optional[Dict] = None,
    equal_filters: Optional[Dict] = None,
) -> int:
    """
    Build sql script for get total count operations
    :param conn: postgres connection
    :param table_name: table name
    :param prefix_filters: the prefix filters, key is the column name, value is the prefix value
    :param equal_filters: the equal filters, key is the column name, value is the equal value
    :return: sql query script and params
    """

    params = []
    where_clauses = []

    # add prefix filters
    if prefix_filters:
        for field, value in prefix_filters.items():
            if value is not None:
                where_clauses.append(f"{field} LIKE ${len(params) + 1}")
                params.append(f"{value}%")

    # add equal filters
    if equal_filters:
        for field, value in equal_filters.items():
            if value is not None:
                where_clauses.append(f"{field} = ${len(params) + 1}")
                params.append(value)

    # build query
    combined_where_clause = " AND ".join(where_clauses)
    combined_where_clause = f"WHERE {combined_where_clause}" if where_clauses else ""

    query = f"""
      SELECT COUNT(*)
      FROM {table_name}
      {combined_where_clause}
      """

    value = await conn.fetchval(query, *params)
    return value


async def list_objects(
    conn,
    object_class,
    table_name: str,
    order: SortOrderEnum,
    sort_field: str,
    object_id_name: Optional[str],
    limit: Optional[int] = None,
    after_id: Optional[str] = None,
    after_value: Optional[Any] = None,
    before_id: Optional[str] = None,
    before_value: Optional[Any] = None,
    offset: Optional[int] = None,
    prefix_filters: Optional[Dict] = None,
    equal_filters: Optional[Dict] = None,
) -> ListResult:
    """
    Build sql script for listing operations
    :param conn: postgres connection
    :param object_class: the class of the object to build
    :param table_name: table name
    :param limit: the maximum number of records to return
    :param order: the order of records to return, desc or asc
    :param sort_field: the field to sort records by
    :param object_id_name: the name of the object id
    :param after_value: the cursor represented by a value to fetch the next page
    :param after_id: the object id of the after cursor
    :param before_value: the cursor represented by a value to fetch the previous page
    :param before_id: the object id of the before cursor
    :param offset: the offset of records to return
    :param prefix_filters: the prefix filters, key is the column name, value is the prefix value
    :param equal_filters: the equal filters, key is the column name, value is the equal value
    :return: a tuple of list of objects, total_count and has_more

    """

    params = []
    where_clauses = []

    # assume all id fields are named as {table_name}_id
    secondary_sort_field = object_id_name
    after_secondary_value = after_id
    before_secondary_value = before_id

    # add prefix filters
    if prefix_filters:
        for field, value in prefix_filters.items():
            if value is not None:
                where_clauses.append(f"{field} LIKE ${len(params) + 1}")
                params.append(f"{value}%")

    # add equal filters
    if equal_filters:
        for field, value in equal_filters.items():
            if value is not None:
                where_clauses.append(f"{field} = ${len(params) + 1}")
                params.append(value)

    # add timestamp condition
    sql_order = "ASC" if order == SortOrderEnum.ASC else "DESC"
    if after_value is not None and after_secondary_value is not None:
        operator = ">" if order == SortOrderEnum.ASC else "<"
        where_clauses.append(
            f"({sort_field}, {secondary_sort_field}) {operator} (${len(params) + 1}, ${len(params) + 2})"
        )
        params.extend([after_value, after_secondary_value])

    # if using before value, we need to reverse the order
    if before_value is not None and before_secondary_value is not None:
        operator = "<" if order == SortOrderEnum.ASC else ">"
        where_clauses.append(
            f"({sort_field}, {secondary_sort_field}) {operator} (${len(params) + 1}, ${len(params) + 2})"
        )
        params.extend([before_value, before_secondary_value])
        sql_order = "DESC" if order == SortOrderEnum.ASC else "ASC"

    # combine where clauses
    combined_where_clause = " AND ".join(where_clauses)
    combined_where_clause = f"WHERE {combined_where_clause}" if where_clauses else ""

    # offset
    sql_offset = f"OFFSET ${len(params) + 1}" if offset is not None else ""
    if offset is not None:
        params.append(offset)

    # fetch one more object than the limit to check for 'has_more'
    limit_clause = ""
    if limit is not None:
        extended_limit = limit + 1
        limit_clause = f"LIMIT ${len(params) + 1}"
        params.append(extended_limit)

    # build query
    query = f"""
    SELECT *
    FROM {table_name}
    {combined_where_clause}
    ORDER BY {sort_field} {sql_order}, {secondary_sort_field} {sql_order}
    {limit_clause}
    {sql_offset}
    """

    # fetch rows
    rows = await conn.fetch(query, *params)

    # build objects
    objs = [object_class.build(row) for row in rows]

    # check if there are more objects than the limit
    has_more = len(objs) > limit if limit else False

    # If using before value, we need to adjust the objs list
    if before_value:
        # Adjust the list to contain only up to 'limit' models
        objs = objs[:limit] if limit else objs
        # Reverse the list to return the correct order
        objs.reverse()

    # If not using before value, adjust normally
    else:
        # Adjust the list to contain only up to 'limit' models
        objs = objs[:limit] if limit else objs

    # get total count
    total = await get_object_total(conn, table_name, prefix_filters, equal_filters)

    return objs, total, has_more
