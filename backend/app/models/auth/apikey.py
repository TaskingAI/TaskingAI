from typing import Dict, List

from tkhelper.models import ModelEntity
from tkhelper.utils import generate_random_id
from tkhelper.encryption.aes import aes_decrypt


__all__ = ["Apikey"]


class Apikey(ModelEntity):
    object: str = "Apikey"

    apikey_id: str
    name: str
    encrypted_apikey: str
    apikey: str
    created_timestamp: int
    updated_timestamp: int

    @staticmethod
    def build(row: Dict):
        encrypted_apikey = row["encrypted_apikey"]
        apikey = aes_decrypt(encrypted_apikey)
        return Apikey(
            apikey_id=row["apikey_id"],
            encrypted_apikey=encrypted_apikey,
            apikey=apikey,
            name=row["name"],
            created_timestamp=row["created_timestamp"],
            updated_timestamp=row["updated_timestamp"],
        )

    def to_response_dict(self) -> Dict:
        response_dict = super().to_response_dict()
        apikey = self.apikey
        response_dict["apikey"] = apikey[:2] + "*" * (len(apikey) - 4) + apikey[-2:]
        return response_dict

    @staticmethod
    def object_name() -> str:
        return "apikey"

    @staticmethod
    def object_plural_name() -> str:
        return "apikeys"

    @staticmethod
    def table_name() -> str:
        return "apikey"

    @staticmethod
    def id_field_name() -> str:
        return "apikey_id"

    @staticmethod
    def primary_key_fields() -> List[str]:
        return ["apikey_id"]

    @staticmethod
    def generate_random_id() -> str:
        return generate_random_id(8)

    @staticmethod
    def generate_random_apikey(apikey_id):
        return "tk" + apikey_id + generate_random_id(22)

    @staticmethod
    def get_apikey_id_from_apikey(apikey):
        return apikey[2:10]

    @staticmethod
    def parent_models() -> List:
        return []

    @staticmethod
    def parent_operator() -> List:
        return []

    @staticmethod
    def create_fields() -> List[str]:
        return ["name"]

    @staticmethod
    def update_fields() -> List[str]:
        return ["name"]

    @staticmethod
    def fields_exclude_in_response():
        return ["encrypted_apikey"]
