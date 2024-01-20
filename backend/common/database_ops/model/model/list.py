from common.database.postgres.pool import postgres_db_pool
from common.models import Model, SortOrderEnum
from typing import Optional, Tuple, List
from typing import Dict
from common.database_ops.utils import get_object_total, list_objects


async def get_model_total(
    prefix_filters: Dict,
    equal_filters: Dict,
) -> int:
    """
    Get total count of models
    :param prefix_filters: the prefix filters, key is the column name, value is the prefix value
    :param equal_filters: the equal filters, key is the column name, value is the equal value
    :return: total count of models
    """

    async with postgres_db_pool.get_db_connection() as conn:
        return await get_object_total(
            conn=conn,
            table_name="model",
            prefix_filters=prefix_filters,
            equal_filters=equal_filters,
        )


async def list_models(
    limit: int,
    order: SortOrderEnum,
    after_model: Optional[Model] = None,
    before_model: Optional[Model] = None,
    offset: int = 0,
    prefix_filters: Optional[Dict] = None,
    equal_filters: Optional[Dict] = None,
) -> Tuple[List[Model], int, bool]:
    """
    List models
    :param limit: the limit of the query
    :param order: the order of the query, asc or desc
    :param after_model: the model to query after
    :param before_model: the model to query before
    :param offset: the offset of the query
    :param prefix_filters: the prefix filters, key is the column name, value is the prefix value
    :param equal_filters: the equal filters, key is the column name, value is the equal value
    :return: a list of models, total count of models, and whether there are more models
    """

    # todo: add different sort field options

    async with postgres_db_pool.get_db_connection() as conn:
        return await list_objects(
            conn=conn,
            object_class=Model,
            table_name="model",
            limit=limit,
            order=order,
            sort_field="created_timestamp",
            object_id_name="model_id",
            after_value=after_model.created_timestamp if after_model else None,
            after_id=after_model.model_id if after_model else None,
            before_value=before_model.created_timestamp if before_model else None,
            before_id=before_model.model_id if before_model else None,
            offset=offset,
            prefix_filters=prefix_filters,
            equal_filters=equal_filters,
        )
