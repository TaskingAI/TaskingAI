from typing import Optional, Dict
from common.models import Model, ModelType, ListResult, SortOrderEnum, ModelSchema, Provider
from common.database_ops.model import model as db_model
from .model_schema import get_model_schema, get_provider
from common.error import ErrorCode, raise_http_error
from common.services.inference.common import verify_credentials
from common.utils import check_http_error

__all__ = [
    "list_models",
    "create_model",
    "update_model",
    "get_model",
    "delete_model",
]


async def validate_and_get_model(model_id: str) -> Model:
    model = await db_model.get_model(model_id)
    if not model:
        raise_http_error(ErrorCode.OBJECT_NOT_FOUND, message=f"Model {model_id} not found.")
    return model


async def list_models(
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
        after_model = await validate_and_get_model(after)

    if before:
        before_model = await validate_and_get_model(before)

    return await db_model.list_models(
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
            "type": model_type,
        },
    )


def _build_display_credentials(original_credentials: Dict, credential_schema: Dict) -> Dict:
    """
    build masked credentials for display purpose
    :param original_credentials: the original credentials
    :param credential_schema: the credential schema
    :return:
    """

    display_credentials = {}

    for key, value in original_credentials.items():
        # check if the key is in the schema
        if key in credential_schema["properties"]:
            if credential_schema["properties"][key].get("secret"):
                # mask the secret value
                value_length = len(value)

                if value_length <= 8:
                    # if the value length is less than 8, just mask the whole value
                    masked_value = "*" * value_length
                else:
                    masked_value = value[:2] + "*" * min(10, value_length - 4) + value[-2:]

                display_credentials[key] = masked_value
            else:
                # the value is not secret, so just keep the original value
                display_credentials[key] = value

    return display_credentials


async def create_model(
    model_schema_id: str,
    name: str,
    credentials: Dict,
    properties: Optional[Dict],
):
    # verify model schema exists
    model_schema: ModelSchema = get_model_schema(model_schema_id)
    if not model_schema:
        raise_http_error(
            ErrorCode.OBJECT_NOT_FOUND,
            message=f"Model schema {model_schema_id} not found.",
        )
    if model_schema.properties is None and properties is not None:
        raise_http_error(
            ErrorCode.REQUEST_VALIDATION_ERROR,
            message="Properties are not allowed for this model schema.",
        )

    # get provider
    provider: Provider = get_provider(model_schema.provider_id)

    # verify model credentials
    response = await verify_credentials(
        provider_id=model_schema.provider_id,
        provider_model_id=model_schema.provider_model_id,
        model_type=model_schema.type.value,
        credentials=credentials,
        properties=properties,
    )
    check_http_error(response)
    data = response.json()["data"]
    encrypted_credentials = data["encrypted_credentials"]
    properties = data["properties"]
    display_credentials = _build_display_credentials(
        original_credentials=credentials,
        credential_schema=provider.credentials_schema,
    )

    model = await db_model.create_model(
        model_schema_id=model_schema_id,
        provider_id=model_schema.provider_id,
        provider_model_id=model_schema.provider_model_id,
        name=name,
        type=model_schema.type,
        encrypted_credentials=encrypted_credentials,
        display_credentials=display_credentials,
        properties=properties,
    )
    return model


async def update_model(
    model_id: str,
    name: Optional[str],
    credentials: Optional[Dict],
    properties: Optional[Dict],
):
    model: Model = await validate_and_get_model(model_id)
    update_dict = {}

    if name is not None:
        update_dict["name"] = name

    if credentials is not None:
        # verify model credentials
        model_schema = model.model_schema()
        response = await verify_credentials(
            provider_id=model_schema.provider_id,
            provider_model_id=model_schema.provider_model_id,
            model_type=model_schema.type.value,
            credentials=credentials,
            properties=properties,
        )
        check_http_error(response)
        data = response.json()["data"]
        encrypted_credentials = data["encrypted_credentials"]
        properties = data["properties"]

        # get provider
        provider: Provider = get_provider(model_schema.provider_id)

        # build masked credentials for display purpose
        display_credentials = _build_display_credentials(
            original_credentials=credentials,
            credential_schema=provider.credentials_schema,
        )

        update_dict["encrypted_credentials"] = encrypted_credentials
        update_dict["display_credentials"] = display_credentials
        update_dict["properties"] = properties

    model = await db_model.update_model(
        model=model,
        update_dict=update_dict,
    )
    return model


async def get_model(model_id: str):
    model: Model = await validate_and_get_model(model_id)
    return model


async def delete_model(model_id: str):
    model: Model = await validate_and_get_model(model_id)
    await db_model.delete_model(model)
    return model
