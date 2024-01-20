from common.database.postgres.pool import postgres_db_pool
from common.models import Chunk, Record, SortOrderEnum, Collection, ListResult
from typing import Optional
from typing import Dict
from common.database_ops.utils import list_objects


async def list_get_collection_chunks(
    collection: Collection,
    limit: int,
    order: SortOrderEnum,
    # todo: add different sort field options
    after_chunk: Optional[Chunk] = None,
    before_chunk: Optional[Chunk] = None,
    offset: int = 0,
    prefix_filters: Optional[Dict] = None,
    equal_filters: Optional[Dict] = None,
) -> ListResult:
    """
    List collection chunks
    :param collection: the collection where the chunk belongs to
    :param limit: the limit of the query
    :param order: the order of the query, asc or desc
    :param after_chunk: the chunk to query after
    :param before_chunk: the chunk to query before
    :param offset: the offset of the query
    :param prefix_filters: the prefix filters, key is the column name, value is the prefix value
    :param equal_filters: the equal filters, key is the column name, value is the equal value
    :return: a list of chunks, total count of chunks, and whether there are more chunks
    """

    # add collection_id to equal_filters
    if equal_filters is None:
        equal_filters = {}
    equal_filters["collection_id"] = collection.collection_id

    table_name = Collection.get_chunk_table_name(collection.collection_id)

    async with postgres_db_pool.get_db_connection() as conn:
        return await list_objects(
            conn=conn,
            object_class=Chunk,
            table_name=table_name,
            limit=limit,
            order=order,
            sort_field="created_timestamp",
            object_id_name="chunk_id",
            after_value=after_chunk.created_timestamp if after_chunk else None,
            after_id=after_chunk.chunk_id if after_chunk else None,
            before_value=before_chunk.created_timestamp if before_chunk else None,
            before_id=before_chunk.chunk_id if before_chunk else None,
            offset=offset,
            prefix_filters=prefix_filters,
            equal_filters=equal_filters,
        )


async def list_get_record_chunks(
    record: Record,
    limit: int,
    order: SortOrderEnum,
    # todo: add different sort field options
    after_chunk: Optional[Chunk] = None,
    before_chunk: Optional[Chunk] = None,
    offset: int = 0,
    prefix_filters: Optional[Dict] = None,
    equal_filters: Optional[Dict] = None,
) -> ListResult:
    """
    List record chunks
    :param record: the record where the chunk belongs to
    :param limit: the limit of the query
    :param order: the order of the query, asc or desc
    :param after_chunk: the chunk to query after
    :param before_chunk: the chunk to query before
    :param offset: the offset of the query
    :param prefix_filters: the prefix filters, key is the column name, value is the prefix value
    :param equal_filters: the equal filters, key is the column name, value is the equal value
    :return: a list of chunks, total count of chunks, and whether there are more chunks
    """

    # add collection_id to equal_filters
    if equal_filters is None:
        equal_filters = {}
    equal_filters["collection_id"] = record.collection_id
    equal_filters["record_id"] = record.record_id

    table_name = Collection.get_chunk_table_name(record.collection_id)

    async with postgres_db_pool.get_db_connection() as conn:
        return await list_objects(
            conn=conn,
            object_class=Chunk,
            table_name=table_name,
            limit=limit,
            order=order,
            sort_field="created_timestamp",
            object_id_name="chunk_id",
            after_value=after_chunk.created_timestamp if after_chunk else None,
            after_id=after_chunk.chunk_id if after_chunk else None,
            before_value=before_chunk.created_timestamp if before_chunk else None,
            before_id=before_chunk.chunk_id if before_chunk else None,
            offset=offset,
            prefix_filters=prefix_filters,
            equal_filters=equal_filters,
        )
