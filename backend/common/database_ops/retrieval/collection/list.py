from common.database.postgres.pool import postgres_db_pool
from common.models import Collection, SortOrderEnum
from typing import Optional, Tuple, List
from typing import Dict
from common.database_ops.utils import get_object_total, list_objects


async def get_collection_total(prefix_filters: Dict, equal_filters: Dict) -> int:
    """
    Get total count of collections
    :param prefix_filters: the prefix filters, key is the column name, value is the prefix value
    :param equal_filters: the equal filters, key is the column name, value is the equal value
    :return: total count of collections
    """
    async with postgres_db_pool.get_db_connection() as conn:
        return await get_object_total(
            conn=conn,
            table_name="collection",
            prefix_filters=prefix_filters,
            equal_filters=equal_filters,
        )


async def list_collections(
    limit: int,
    order: SortOrderEnum,
    after_collection: Optional[Collection] = None,
    before_collection: Optional[Collection] = None,
    offset: int = 0,
    prefix_filters: Optional[Dict] = None,
    equal_filters: Optional[Dict] = None,
) -> Tuple[List[Collection], int, bool]:
    """
    List collections
    :param limit: the limit of the query
    :param order: the order of the query, asc or desc
    :param after_collection: the collection to query after
    :param before_collection: the collection to query before
    :param offset: the offset of the query
    :param prefix_filters: the prefix filters, key is the column name, value is the prefix value
    :param equal_filters: the equal filters, key is the column name, value is the equal value
    :return: a list of collections, total count of collections, and whether there are more collections
    """

    # todo: add different sort field options
    async with postgres_db_pool.get_db_connection() as conn:
        return await list_objects(
            conn=conn,
            object_class=Collection,
            table_name="collection",
            limit=limit,
            order=order,
            sort_field="created_timestamp",
            after_value=after_collection.created_timestamp if after_collection else None,
            before_value=before_collection.created_timestamp if before_collection else None,
            offset=offset,
            prefix_filters=prefix_filters,
            equal_filters=equal_filters,
        )
