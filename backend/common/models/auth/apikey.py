from common.utils import generate_random_id
from pydantic import BaseModel
from typing import Dict
from common.models import SerializePurpose
from common.utils import aes_decrypt
from common.database.redis import redis_object_pop, redis_object_set_object, redis_object_get_object

__all__ = ["Apikey"]


class Apikey(BaseModel):
    apikey_id: str
    encrypted_apikey: str
    name: str
    updated_timestamp: int
    created_timestamp: int

    @staticmethod
    def object_name():
        return "Apikey"

    @staticmethod
    def generate_random_id():
        return generate_random_id(8)

    @staticmethod
    def generate_random_apikey(apikey_id):
        return "tk" + apikey_id + generate_random_id(22)

    @staticmethod
    def get_apikey_id_from_apikey(apikey):
        return apikey[2:10]

    @classmethod
    def build(cls, row: Dict):
        return cls(
            apikey_id=row["apikey_id"],
            encrypted_apikey=row["encrypted_apikey"],
            name=row["name"],
            updated_timestamp=row["updated_timestamp"],
            created_timestamp=row["created_timestamp"],
        )

    def to_dict(self, purpose: SerializePurpose = None, plain: bool = False):
        ret = {
            "object": self.object_name(),
            "apikey_id": self.apikey_id,
            "name": self.name,
            "updated_timestamp": self.updated_timestamp,
            "created_timestamp": self.created_timestamp,
        }

        if purpose == SerializePurpose.REDIS:
            ret["encrypted_apikey"] = self.encrypted_apikey

        elif purpose == SerializePurpose.RESPONSE:
            apikey = aes_decrypt(self.encrypted_apikey)
            if plain:
                ret["apikey"] = apikey
            else:
                ret["apikey"] = apikey[:2] + "*" * (len(apikey) - 4) + apikey[-2:]

        return ret

    @classmethod
    async def get_redis(cls, apikey_id: str):
        return await redis_object_get_object(Apikey, apikey_id)

    async def set_redis(self):
        await redis_object_set_object(
            Apikey,
            key=self.apikey_id,
            value=self.to_dict(purpose=SerializePurpose.REDIS),
        )

    async def pop_redis(self):
        await redis_object_pop(
            Apikey,
            key=self.apikey_id,
        )
