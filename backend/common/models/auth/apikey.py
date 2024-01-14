from common.utils import generate_random_id
from pydantic import BaseModel
from typing import Dict
from common.models import SerializePurpose

__all__ = ["Apikey"]


class Apikey(BaseModel):
    apikey_id: str
    # todo: use apikey_secret
    apikey: str
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
        return apikey[:8]

    @classmethod
    def build(cls, row: Dict):
        return cls(
            apikey_id=row["apikey_id"],
            apikey=row["apikey"],
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
            ret["apikey"] = self.apikey

        elif purpose == SerializePurpose.RESPONSE:
            if plain:
                ret["apikey"] = self.apikey
            else:
                ret["apikey"] = self.apikey[:2] + "*" * (len(self.apikey) - 4) + self.apikey[-2:]

        return ret
