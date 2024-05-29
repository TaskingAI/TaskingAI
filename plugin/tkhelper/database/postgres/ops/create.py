from typing import Dict, List
import logging
from tkhelper.utils import prepare_db_dict

logger = logging.getLogger(__name__)


async def create_object(
    conn,
    table_name: str,
    object_dict: Dict,
    primary_keys: List[str],
) -> None:
    """
    Asynchronously insert a new object into the database.

    :param conn: An asynchronous database connection object.
    :param table_name: Name of the database table where the new object will be inserted.
    :param object_dict: Dictionary containing the data to insert, where keys are column names.
    :param primary_keys: List of primary key column names.
    :return: None
    """

    if not object_dict:
        raise ValueError("object_dict cannot be empty")

    # Cast all the dict/list to str
    upsert_dict = prepare_db_dict(object_dict)

    # Construct the column names and placeholders for the values
    columns = ", ".join(upsert_dict.keys())
    placeholders = ", ".join(f"${i + 1}" for i in range(len(upsert_dict)))

    # Construct the INSERT query
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    # Prepare the values from the pg_create_dict
    values = list(upsert_dict.values())

    logger.debug(f"create_object: query={query}, values={values}")

    # Attempt to execute the insert query
    await conn.execute(query, *values)
