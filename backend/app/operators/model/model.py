from tkhelper.models import RedisOperator, ModelEntity
from tkhelper.models.operator.postgres_operator import PostgresModelOperator
from tkhelper.error import raise_http_error, raise_request_validation_error, ErrorCode
from tkhelper.utils import check_http_error
from typing import Dict, Tuple

from app.database import redis_conn, postgres_pool
from app.models import Model, ModelSchema, Provider, ModelType, ModelFallbackConfig

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
    provider_model_id: str,
    properties: Dict,
    configs: Dict,
    model_type: str,
    credentials: Dict,
    encrypted_credentials: Dict = None,
    fallbacks: ModelFallbackConfig = None,
) -> Tuple[str, str, str, str, Dict, Dict, Dict, Dict]:
    """
    verify model credentials and build display credentials
    :param model_schema_id: the model schema id
    :param provider_model_id: the provider model id
    :param properties: the properties
    :param configs: the configs
    :param model_type: the model type
    :param credentials: the credentials
    :param encrypted_credentials: the encrypted credentials
    :param fallbacks: the fallback models
    :return: a tuple of (the model schema id, provider id, provider model id, model type,
        encrypted credentials, display credentials, properties)

    """
    from app.services.model import get_model_schema, get_provider
    from app.services.inference import verify_credentials

    # verify model schema exists
    model_schema: ModelSchema = get_model_schema(model_schema_id)
    if not model_schema:
        raise_http_error(
            error_code=ErrorCode.OBJECT_NOT_FOUND,
            message=f"Model schema {model_schema_id} not found.",
        )

    # get provider
    provider: Provider = get_provider(model_schema.provider_id)

    provider_model_id = provider_model_id or model_schema.provider_model_id

    properties = properties or model_schema.properties
    provider_model_id = provider_model_id or model_schema.provider_model_id

    if model_schema.type == ModelType.WILDCARD:
        if not model_type:
            raise_request_validation_error("Model type is required for wildcard models.")
        elif model_type == ModelType.WILDCARD:
            raise_request_validation_error("Model type cannot be wildcard.")
    else:
        model_type = model_schema.type

    if fallbacks:
        fallback_list = fallbacks.get("model_list")
        seen_model_ids = set()  # Set to track seen model IDs
        for fb in fallback_list:
            model_id = fb.get("model_id")
            if model_id in seen_model_ids:
                raise_request_validation_error(f"Duplicate fallback model ID {model_id} detected.")
            seen_model_ids.add(model_id)
            model = await model_ops.get(model_id=model_id)
            # check the fallback model type is the same as the main model type
            if model.type != model_type:
                raise_request_validation_error(
                    f"Fallback model {model_id} type {model.type} is not the same as model schema type: {model_type}."
                )

    # verify model credentials
    response = await verify_credentials(
        model_schema_id=model_schema.model_schema_id,
        provider_model_id=provider_model_id,
        model_type=model_type,
        credentials=credentials,
        encrypted_credentials=encrypted_credentials,
        properties=properties,
        configs=configs,
    )
    check_http_error(response)
    response_data = response.json()["data"]
    encrypted_credentials = response_data["encrypted_credentials"]
    properties = response_data["properties"] or {}
    display_credentials = None
    if credentials:
        display_credentials = _build_display_credentials(
            original_credentials=credentials,
            credential_schema=provider.credentials_schema,
        )

    return (
        model_schema_id,
        model_schema.provider_id,
        provider_model_id,
        model_type,
        encrypted_credentials,
        display_credentials,
        properties,
        configs,
    )


class ModelOperator(PostgresModelOperator):
    async def create(
        self,
        create_dict: Dict,
        **kwargs,
    ) -> ModelEntity:
        fallbacks = create_dict.get("fallbacks") or {}
        # verify model credentials
        (
            model_schema_id,
            provider_id,
            provider_model_id,
            model_type,
            encrypted_credentials,
            display_credentials,
            properties,
            configs,
        ) = await verify_model_credentials(
            model_schema_id=create_dict["model_schema_id"],
            provider_model_id=create_dict.get("provider_model_id"),
            properties=create_dict.get("properties"),
            model_type=create_dict.get("type"),
            credentials=create_dict["credentials"],
            configs=create_dict.get("configs") or {},
            fallbacks=fallbacks,
        )

        model = await super().create(
            create_dict={
                "model_schema_id": model_schema_id,
                "provider_id": provider_id,
                "provider_model_id": provider_model_id,
                "name": create_dict["name"],
                "type": model_type,
                "encrypted_credentials": encrypted_credentials,
                "display_credentials": display_credentials,
                "properties": properties,
                "configs": configs,
                "fallbacks": fallbacks,
            },
        )
        return model

    async def update(self, update_dict: Dict, **kwargs) -> ModelEntity:
        model_id = kwargs["model_id"]
        model: Model = await super().get(model_id=model_id)

        new_update_dict = {}
        if update_dict.get("name") is not None:
            new_update_dict["name"] = update_dict.get("name")

        model_schema_id = update_dict.get("model_schema_id")
        provider_model_id = update_dict.get("provider_model_id")
        model_type = update_dict.get("type")
        credentials = update_dict.get("credentials")
        properties = update_dict.get("properties")
        configs = update_dict.get("configs")
        fallbacks = update_dict.get("fallbacks") or {}

        if model_schema_id or provider_model_id or model_type or credentials or properties or configs:
            # verify model credentials
            (
                new_model_schema_id,
                new_provider_id,
                new_provider_model_id,
                new_model_type,
                new_encrypted_credentials,
                new_display_credentials,
                new_properties,
                new_configs,
            ) = await verify_model_credentials(
                model_schema_id=model_schema_id or model.model_schema_id,
                provider_model_id=provider_model_id or model.provider_model_id,
                properties=properties or model.properties,
                model_type=model_type or model.type,
                credentials=credentials,
                encrypted_credentials=model.encrypted_credentials if not credentials else None,
                configs=configs,
                fallbacks=fallbacks,
            )

            new_update_dict["model_schema_id"] = new_model_schema_id
            new_update_dict["provider_id"] = new_provider_id
            new_update_dict["provider_model_id"] = new_provider_model_id
            new_update_dict["type"] = new_model_type
            new_update_dict["properties"] = new_properties
            new_update_dict["configs"] = new_configs or model.configs
            if fallbacks:
                new_update_dict["fallbacks"] = fallbacks
            if credentials:
                new_update_dict["encrypted_credentials"] = new_encrypted_credentials
                new_update_dict["display_credentials"] = new_display_credentials

        model = await super().update(
            model_id=model_id,
            update_dict=new_update_dict,
        )
        return model


model_ops = ModelOperator(
    postgres_pool=postgres_pool,
    entity_class=Model,
    redis=RedisOperator(
        entity_class=Model,
        redis_conn=redis_conn,
    ),
)
