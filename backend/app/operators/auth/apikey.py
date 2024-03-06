from typing import Dict

from tkhelper.models import RedisOperator, ModelEntity
from tkhelper.models.operator.postgres_operator import PostgresModelOperator
from tkhelper.encryption.aes import aes_encrypt

from app.database import postgres_pool, redis_conn
from app.models import Apikey

__all__ = ["apikey_ops"]


class ApikeyModelOperator(PostgresModelOperator):
    async def create(
        self,
        create_dict: Dict,
        **kwargs,
    ) -> ModelEntity:
        # handle kwargs
        self._check_kwargs(object_id_required=None, **kwargs)
        name = create_dict["name"]

        # generate id and apikey
        new_id = Apikey.generate_random_id()
        new_apikey = Apikey.generate_random_apikey(new_id)
        new_encrypted_apikey = aes_encrypt(new_apikey)

        # create apikey
        apikey = await super().create(
            apikey_id=new_id,
            create_dict={
                "name": name,
                "encrypted_apikey": new_encrypted_apikey,
            },
        )

        return apikey


apikey_ops = ApikeyModelOperator(
    postgres_pool=postgres_pool,
    entity_class=Apikey,
    redis=RedisOperator(
        entity_class=Apikey,
        redis_conn=redis_conn,
    ),
)
