from common.database.postgres.pool import postgres_db_pool
from common.models import Record, SortOrderEnum, Collection
from typing import Optional, Tuple, List
from typing import Dict
from common.database_ops.utils import get_object_total, list_objects


async def get_record_total(prefix_filters: Dict, equal_filters: Dict) -> int:
    """
    Get total count of records
    :param prefix_filters: the prefix filters, key is the column name, value is the prefix value
    :param equal_filters: the equal filters, key is the column name, value is the equal value
    :return: total count of records
    """
    async with postgres_db_pool.get_db_connection() as conn:
        return await get_object_total(
            conn=conn,
            table_name="record",
            prefix_filters=prefix_filters,
            equal_filters=equal_filters,
        )


async def list_records(
    collection: Collection,
    limit: int,
    order: SortOrderEnum,
    # todo: add different sort field options
    after_record: Optional[Record] = None,
    before_record: Optional[Record] = None,
    offset: int = 0,
    prefix_filters: Optional[Dict] = None,
    equal_filters: Optional[Dict] = None,
) -> Tuple[List[Record], int, bool]:
    """
    List records
    :param collection: the collection where the record belongs to
    :param limit: the limit of the query
    :param order: the order of the query, asc or desc
    :param after_record: the record to query after
    :param before_record: the record to query before
    :param offset: the offset of the query
    :param prefix_filters: the prefix filters, key is the column name, value is the prefix value
    :param equal_filters: the equal filters, key is the column name, value is the equal value
    :return: a list of records, total count of records, and whether there are more records
    """

    # add collection_id to equal_filters
    if equal_filters is None:
        equal_filters = {}
    equal_filters["collection_id"] = collection.collection_id

    async with postgres_db_pool.get_db_connection() as conn:
        return await list_objects(
            conn=conn,
            object_class=Record,
            table_name="record",
            limit=limit,
            order=order,
            sort_field="created_timestamp",
            after_value=after_record.created_timestamp if after_record else None,
            before_value=before_record.created_timestamp if before_record else None,
            offset=offset,
            prefix_filters=prefix_filters,
            equal_filters=equal_filters,
        )
