from typing import Optional, Dict
from common.models import Model, ModelType, ListResult, SortOrderEnum
from common.database_ops import model as db_model
from .model_schema import get_model_schema
from common.error import ErrorCode, raise_http_error

__all__ = [
    "list_models",
    "create_model",
    "update_model",
    "get_model",
    "delete_model",
]


async def validate_and_get_model(postgres_conn, model_id: str) -> Model:
    model = await db_model.get_model(postgres_conn, model_id)
    if not model:
        raise_http_error(ErrorCode.OBJECT_NOT_FOUND, message=f"Model {model_id} not found.")
    return model


async def list_models(
    postgres_conn,
    limit: int,
    order: SortOrderEnum,
    after: Optional[str],
    before: Optional[str],
    offset: Optional[int],
    id_search: Optional[str],
    name_search: Optional[str],
    provider_id: Optional[str],
    model_type: Optional[ModelType],
) -> ListResult:
    """
    List models
    :param postgres_conn: postgres connection
    :param limit: the limit of the query
    :param order: the order of the query, asc or desc
    :param after: the cursor ID to query after
    :param before: the cursor ID to query before
    :param offset: the offset of the query
    :param id_search: the model ID to search for
    :param name_search: the model name to search for
    :param provider_id: the provider ID to filter by
    :param model_type: the model type to filter by
    :return: a list of models, total count of models, and whether there are more models
    """

    after_model, before_model = None, None

    if after:
        after_model = await validate_and_get_model(postgres_conn, after)

    if before:
        before_model = await validate_and_get_model(postgres_conn, before)

    return await db_model.list_models(
        postgres_conn=postgres_conn,
        limit=limit,
        order=order,
        after_model=after_model,
        before_model=before_model,
        offset=offset,
        prefix_filters={
            "model_id": id_search,
            "name": name_search,
        },
        equal_filters={
            "provider_id": provider_id,
            "model_type": model_type,
        },
    )


async def create_model(
    postgres_conn,
    model_schema_id: str,
    name: str,
    credentials: Dict,
):
    # todo verify credentials
    model_schema = get_model_schema(model_schema_id)
    # todo: encrypt credentials
    model = await db_model.create_model(
        conn=postgres_conn,
        model_schema_id=model_schema_id,
        provider_id=model_schema.provider_id,
        provider_model_id=model_schema.provider_model_id,
        name=name,
        encrypted_credentials=credentials,
        display_credentials=credentials,
    )
    return model


async def update_model(postgres_conn, model_id: str, name: Optional[str], credentials: Optional[Dict]):
    model: Model = await validate_and_get_model(postgres_conn, model_id)
    update_dict = {}
    if name:
        update_dict["name"] = name
    if credentials:
        # todo verify credentials
        # todo: encrypt credentials
        update_dict["encrypted_credentials"] = credentials
        update_dict["display_credentials"] = credentials
    model = await db_model.update_model(
        conn=postgres_conn,
        model=model,
        update_dict=update_dict,
    )
    return model


async def get_model(postgres_conn, model_id: str):
    model: Model = await validate_and_get_model(postgres_conn, model_id)
    return model


async def delete_model(postgres_conn, model_id: str):
    model: Model = await validate_and_get_model(postgres_conn, model_id)
    await db_model.delete_model(postgres_conn, model)
    return model
