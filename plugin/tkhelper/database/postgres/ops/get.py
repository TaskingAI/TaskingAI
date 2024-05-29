from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


async def get_object(
    conn,
    table_name: str,
    equal_filters: Dict[str, any],
) -> Optional[Dict]:
    """
    Asynchronously retrieve an object from the database based on specified filters

    :param conn: An asynchronous database connection object.
    :param table_name: Name of the database table to query.
    :param equal_filters: Dictionary of column names and values to filter by.
    :return: A dictionary of the retrieved row, or None if no matching row is found.
    """

    if not equal_filters:
        raise ValueError("equal_filters cannot be empty")

    # Construct the WHERE clause with equality filters
    conditions = " AND ".join(f"{key} = ${idx + 1}" for idx, key in enumerate(equal_filters.keys()))

    # Construct the SELECT query
    query = f"SELECT * FROM {table_name} WHERE {conditions} LIMIT 1"

    # Prepare the arguments for the query
    args = list(equal_filters.values())

    # Execute the query and fetch the result
    record = await conn.fetchrow(query, *args)

    if record:
        # Convert the record to a dictionary if a row is found
        return dict(record)
    else:
        # Return None if no matching row is found
        return None
