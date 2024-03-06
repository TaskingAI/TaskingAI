from typing import Dict
import logging

logger = logging.getLogger(__name__)


async def delete_object(
    conn,
    table_name: str,
    equal_filters: Dict,
) -> bool:
    """
    Physically delete an object from the database.
    :param conn: a postgres connection
    :param table_name: the table name
    :param equal_filters: the equal filters to identify the object
    :return: a boolean indicating if the object is deleted
    """

    if not equal_filters:
        raise ValueError("equal_filters cannot be empty")

    # Prepare the WHERE clause for the delete query
    conditions = " AND ".join(f"{key} = ${idx + 1}" for idx, key in enumerate(equal_filters.keys()))

    # Prepare the final query
    query = f"DELETE FROM {table_name} WHERE {conditions} RETURNING 1"

    # Prepare the arguments for the query
    args = list(equal_filters.values())

    # Execute the query
    result = await conn.fetch(query, *args)

    logger.debug(f"delete_object: query={query}, args={args}, result={result}")

    return bool(result)
