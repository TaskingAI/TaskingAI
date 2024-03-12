from tkhelper.models import RedisOperator, ModelEntity
from tkhelper.models.operator.postgres_operator import PostgresModelOperator
from tkhelper.error import raise_request_validation_error
from tkhelper.utils import check_http_error
from typing import Dict, Tuple, Optional

from app.database import redis_conn, postgres_pool
from app.models import Model, ModelSchema, Provider, ModelType

__all__ = ["model_ops"]


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


async def verify_model_credentials(
    model_schema_id: str,
    provider_model_id: Optional[str],
    model_type: Optional[str],
    credentials: Dict,
    properties: Optional[Dict],
) -> Tuple[str, str, str, Dict, Dict, Dict]:
    """
    Verify model credentials
    :param model_schema_id: the model schema id
    :param provider_model_id: the provider model id
    :param model_type: the model type
    :param credentials: the credentials
    :param properties: the properties
    :return: a tuple of provider_id, provider_model_id, model_type, properties, encrypted_credentials, display_credentials
    """
    from app.services.model import get_model_schema, get_provider
    from app.services.inference import verify_credentials

    # verify model schema exists
    model_schema: ModelSchema = get_model_schema(model_schema_id)
    if not model_schema:
        raise_request_validation_error(message=f"Model schema {model_schema_id} not found.")

    # get provider
    provider: Provider = get_provider(model_schema.provider_id)
    provider_id = provider.provider_id

    properties = properties or model_schema.properties
    provider_model_id = provider_model_id or model_schema.provider_model_id

    if model_schema.type == ModelType.WILDCARD:
        if not model_type:
            raise_request_validation_error("Model type is required for wildcard models.")
        elif model_type == ModelType.WILDCARD:
            raise_request_validation_error("Model type cannot be wildcard.")
    else:
        model_type = model_schema.type

        # verify model credentials
    response = await verify_credentials(
        model_schema_id=model_schema.model_schema_id,
        provider_model_id=provider_model_id,
        model_type=model_type,
        credentials=credentials,
        properties=properties,
    )
    check_http_error(response)
    response_data = response.json()["data"]
    encrypted_credentials = response_data["encrypted_credentials"]
    properties = response_data["properties"]
    display_credentials = _build_display_credentials(
        original_credentials=credentials,
        credential_schema=provider.credentials_schema,
    )

    return (provider_id, provider_model_id, model_type, properties, encrypted_credentials, display_credentials)


class ModelModelOperator(PostgresModelOperator):
    async def create(
        self,
        create_dict: Dict,
        **kwargs,
    ) -> ModelEntity:
        # handle kwargs
        self._check_kwargs(object_id_required=None, **kwargs)
        model_schema_id = create_dict["model_schema_id"]
        name = create_dict["name"]

        # verify model credentials
        (
            provider_id,
            provider_model_id,
            model_type,
            properties,
            encrypted_credentials,
            display_credentials,
        ) = await verify_model_credentials(
            model_schema_id=model_schema_id,
            provider_model_id=create_dict.get("provider_model_id"),
            model_type=create_dict.get("type"),
            credentials=create_dict["credentials"],
            properties=create_dict.get("properties"),
        )

        # create model
        model = await super().create(
            create_dict={
                "model_schema_id": model_schema_id,
                "provider_id": provider_id,
                "provider_model_id": provider_model_id,
                "name": name,
                "type": model_type,
                "encrypted_credentials": encrypted_credentials,
                "display_credentials": display_credentials,
                "properties": properties,
            },
            **kwargs,
        )

        return model

    async def update(
        self,
        update_dict: Dict,
        **kwargs,
    ) -> ModelEntity:
        """
        Update a model
        :param update_dict: the model update dictionary
        :param kwargs: other parameters
        :return: the updated model
        """

        self._check_kwargs(object_id_required=True, **kwargs)
        model_id = kwargs.get("model_id")

        name = update_dict.get("name")
        credentials = update_dict.get("credentials")

        # get model
        model = await self.get(model_id=model_id)

        # prepare update dict
        new_update_dict = {}

        if name is not None:
            new_update_dict["name"] = name

        if credentials is not None:
            # verify model credentials
            (
                provider_id,
                provider_model_id,
                model_type,
                properties,
                encrypted_credentials,
                display_credentials,
            ) = await verify_model_credentials(
                model_schema_id=update_dict.get("model_schema_id") or model.model_schema_id,
                provider_model_id=update_dict.get("provider_model_id") or model.provider_model_id,
                model_type=update_dict.get("type") or model.type,
                credentials=update_dict.get("credentials") or model.credentials,
                properties=update_dict.get("properties") or model.properties,
            )
            new_update_dict["provider_id"] = provider_id
            new_update_dict["provider_model_id"] = provider_model_id
            new_update_dict["type"] = model_type
            new_update_dict["properties"] = properties
            new_update_dict["encrypted_credentials"] = encrypted_credentials
            new_update_dict["display_credentials"] = display_credentials

        return await super().update(
            update_dict=new_update_dict,
            **kwargs,
        )


model_ops = ModelModelOperator(
    postgres_pool=postgres_pool,
    entity_class=Model,
    redis=RedisOperator(
        entity_class=Model,
        redis_conn=redis_conn,
    ),
)
