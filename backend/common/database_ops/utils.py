from typing import Dict
from common.utils import current_timestamp_int_milliseconds
import json


async def prepare_and_execute_update(
    conn, update_dict: Dict, update_time: bool, table_name: str, condition_fields: Dict
) -> None:
    pg_update_dict = update_dict.copy()
    for key, value in update_dict.items():
        if isinstance(value, (dict, list)):
            pg_update_dict[key] = json.dumps(value)

    timestamp_int = current_timestamp_int_milliseconds()
    # Prepare the SET clause for the update query
    updates = ", ".join(
        f"{key} = ${idx}" for idx, key in enumerate(pg_update_dict.keys(), start=len(condition_fields) + 2)
    )
    if update_time:
        updates += ", updated_timestamp = $1"

    # Prepare the WHERE clause for the update query
    conditions = " AND ".join(f"{key} = ${idx}" for idx, key in enumerate(condition_fields.keys(), start=2))

    # Prepare the final query
    query = f"UPDATE {table_name} SET {updates} WHERE {conditions}"

    # Prepare the arguments for the query
    args = [timestamp_int, *condition_fields.values(), *pg_update_dict.values()]

    # log function, query and args
    # logging.info(f'function: prepare_and_execute_update, query: {query}, args: {args}')

    # Execute the query
    await conn.execute(query, *args)
