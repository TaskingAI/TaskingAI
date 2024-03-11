from typing import Dict, Tuple
import aiohttp

from tkhelper.models import RedisOperator
from tkhelper.models.operator.postgres_operator import PostgresModelOperator
from tkhelper.models.entity import ModelEntity
from tkhelper.utils import ResponseWrapper, check_http_error
from tkhelper.error import raise_http_error, ErrorCode

from app.database import redis_conn, postgres_pool
from app.models import BundleInstance, Bundle
from app.config import CONFIG

__all__ = ["bundle_instance_ops"]


def __build_display_credentials(original_credentials: Dict, credential_schema: Dict) -> Dict:
    """
    build masked credentials for display purpose
    :param original_credentials: the original credentials
    :param credential_schema: the credential schema
    :return:
    """

    display_credentials = {}

    for key, value in original_credentials.items():
        # check if the key is in the schema
        if key in credential_schema:
            if credential_schema[key].get("secret"):
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


async def verify_bundle_credentials(bundle: Bundle, credentials: Dict) -> Tuple[Dict, Dict]:
    """
    :param bundle_id: the bundle ID
    :param credentials: the credentials of the bundle instance
    :return: a Tuple of encrypted credentials and display credentials
    """

    if not bundle:
        raise_http_error(ErrorCode.OBJECT_NOT_FOUND, "Bundle not found")

    async with aiohttp.ClientSession() as session:
        response = await session.post(
            f"{CONFIG.TASKINGAI_PLUGIN_URL}/v1/verify_credentials",
            json={
                "bundle_id": bundle.bundle_id,
                "credentials": credentials,
            },
        )
        response_wrapper = ResponseWrapper(response.status, await response.json())
        check_http_error(response_wrapper)
        response_data = response_wrapper.json()["data"]
        encrypted_credentials = response_data["encrypted_credentials"]
        display_credentials = __build_display_credentials(
            original_credentials=credentials,
            credential_schema=bundle.credentials_schema,
        )

    return encrypted_credentials, display_credentials


class BundleInstanceModelOperator(PostgresModelOperator):
    async def create(
        self,
        create_dict: Dict,
        **kwargs,
    ) -> ModelEntity:
        from app.services.tool import get_bundle

        # handle kwargs
        self._check_kwargs(object_id_required=None, **kwargs)
        bundle_id = create_dict["bundle_id"]
        credentials = create_dict["credentials"]
        name = create_dict["name"]

        # check not exists
        bundle_instance = await self.get(
            bundle_instance_id=bundle_id,
            raise_not_found_error=False,
        )
        if bundle_instance is not None:
            raise_http_error(ErrorCode.DUPLICATE_OBJECT, f"Bundle instance {bundle_id} already exists")

        # validate bundle and credentials
        bundle: Bundle = get_bundle(bundle_id)
        encrypted_credentials, display_credentials = await verify_bundle_credentials(
            bundle=bundle,
            credentials=credentials,
        )

        # create
        bundle_instance = await super().create(
            bundle_instance_id=bundle_id,  # currently we use the same bundle_id as the bundle_instance_id
            create_dict={
                "bundle_id": bundle_id,
                "encrypted_credentials": encrypted_credentials,
                "display_credentials": display_credentials,
                "name": name,
            },
        )

        return bundle_instance

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
        from app.services.tool import get_bundle

        self._check_kwargs(object_id_required=True, **kwargs)

        bundle_instance = await self.get(
            bundle_instance_id=kwargs.get("bundle_instance_id"),
        )

        credentials = update_dict["credentials"]
        name = update_dict["name"]

        encrypted_credentials = None
        display_credentials = None

        if credentials is not None:
            # verify bundle and credentials
            bundle: Bundle = get_bundle(bundle_instance.bundle_id)
            encrypted_credentials, display_credentials = await verify_bundle_credentials(
                bundle=bundle,
                credentials=credentials,
            )

        return await super().update(
            update_dict={
                "encrypted_credentials": encrypted_credentials,
                "display_credentials": display_credentials,
                "name": name,
            },
            **kwargs,
        )


bundle_instance_ops = BundleInstanceModelOperator(
    postgres_pool=postgres_pool,
    entity_class=BundleInstance,
    redis=RedisOperator(
        entity_class=BundleInstance,
        redis_conn=redis_conn,
    ),
)
