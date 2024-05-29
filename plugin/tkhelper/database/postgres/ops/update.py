from typing import Dict
from tkhelper.utils import current_timestamp_int_milliseconds
import logging
from tkhelper.utils import prepare_db_dict

logger = logging.getLogger(__name__)


async def update_object(
    conn,
    table_name: str,
    update_dict: Dict,
    equal_filters: Dict,
) -> None:
    """
    Update an object and its updated_timestamp in the database considering
    :param conn: a postgres connection
    :param update_dict: update dict
    :param table_name: the table name
    :param equal_filters: the equal filters
    :return: None
    """

    if not update_dict:
        raise ValueError("update_dict cannot be empty")

    if not equal_filters:
        raise ValueError("equal_filters cannot be empty")

    # 1. build update dict
    upsert_dict = prepare_db_dict(update_dict)

    # 2. Prepare the SET clause for the update query
    updates = ", ".join(f"{key} = ${idx}" for idx, key in enumerate(upsert_dict.keys(), start=len(equal_filters) + 2))
    updates += ", updated_timestamp = $1"

    # 3. Prepare the WHERE clause for the update query, including check
    conditions = " AND ".join(f"{key} = ${idx}" for idx, key in enumerate(equal_filters.keys(), start=2))

    # 4. Prepare the final query
    query = f"UPDATE {table_name} SET {updates} WHERE {conditions}"

    # 5. Prepare the arguments for the query
    args = [current_timestamp_int_milliseconds(), *equal_filters.values(), *upsert_dict.values()]

    # 6. Execute the query
    await conn.execute(query, *args)

    logger.debug(f"update_object: query={query}, args={args}")
