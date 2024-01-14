from pydantic import BaseModel
from typing import Dict, Optional
from ..utils import generate_random_id
from .base import SerializePurpose


class Admin(BaseModel):
    admin_id: str
    username: str
    salt: Optional[str]
    password_hash: Optional[str]
    token: Optional[str]
    created_timestamp: int
    updated_timestamp: int

    @staticmethod
    def object_name():
        return "Admin"

    @staticmethod
    def generate_random_id():
        return "X3Ar" + generate_random_id(12)

    @classmethod
    def build(cls, row: Dict):
        return cls(
            admin_id=row["admin_id"],
            username=row["username"],
            salt=row["salt"],
            password_hash=row["password_hash"],
            token=row["token"],
            created_timestamp=row["created_timestamp"],
            updated_timestamp=row["updated_timestamp"],
        )

    def to_dict(self, purpose: SerializePurpose):
        ret = {
            "object": self.object_name(),
            "admin_id": self.admin_id,
            "username": self.username,
            "token": self.token,
            "created_timestamp": self.created_timestamp,
            "updated_timestamp": self.updated_timestamp,
        }
        if purpose == SerializePurpose.REDIS:
            ret["salt"] = self.salt
            ret["password_hash"] = self.password_hash
        elif purpose == SerializePurpose.RESPONSE:
            ret["token"] = self.token

        return ret
