from typing import Dict, List, Optional

from tkhelper.models import ModelEntity
from tkhelper.utils import generate_random_id


__all__ = ["Admin"]


class Admin(ModelEntity):
    object: str = "Admin"
    admin_id: str
    username: str
    salt: Optional[str]
    password_hash: Optional[str]
    token: Optional[str]
    created_timestamp: int
    updated_timestamp: int

    @staticmethod
    def build(row: Dict):
        return Admin(
            admin_id=row["admin_id"],
            username=row["username"],
            salt=row["salt"],
            password_hash=row["password_hash"],
            token=row["token"],
            created_timestamp=row["created_timestamp"],
            updated_timestamp=row["updated_timestamp"],
        )

    @staticmethod
    def object_name() -> str:
        return "admin"

    @staticmethod
    def object_plural_name() -> str:
        return "admins"

    @staticmethod
    def table_name() -> str:
        return "app_admin"

    @staticmethod
    def id_field_name() -> str:
        return "admin_id"

    @staticmethod
    def primary_key_fields() -> List[str]:
        return ["admin_id"]

    @staticmethod
    def generate_random_id():
        return "X3Ar" + generate_random_id(12)

    @staticmethod
    def list_prefix_filter_fields() -> List[str]:
        return []

    @staticmethod
    def parent_models() -> List:
        return []

    @staticmethod
    def parent_operator() -> List:
        return []

    @staticmethod
    def create_fields() -> List[str]:
        return ["username", "salt", "password_hash", "token"]

    @staticmethod
    def update_fields() -> List[str]:
        return ["salt", "password_hash", "token"]

    @staticmethod
    def fields_exclude_in_response():
        return ["password_hash", "salt"]
