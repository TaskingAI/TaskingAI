from pydantic import BaseModel
from typing import Dict, Optional
from common.utils import generate_random_id
from common.models import SerializePurpose
from common.database.redis import redis_object_pop, redis_object_set_object, redis_object_get_object


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

    @classmethod
    async def get_redis_by_id(cls, admin_id: str):
        return await redis_object_get_object(Admin, admin_id)

    @classmethod
    async def get_redis_by_username(cls, username: str):
        return await redis_object_get_object(Admin, username)

    async def set_redis(self):
        await redis_object_set_object(
            Admin,
            key=self.admin_id,
            value=self.to_dict(purpose=SerializePurpose.REDIS),
        )
        await redis_object_set_object(
            Admin,
            key=self.username,
            value=self.to_dict(purpose=SerializePurpose.REDIS),
        )

    async def pop_redis(self):
        await redis_object_pop(
            Admin,
            key=self.admin_id,
        )
        await redis_object_pop(
            Admin,
            key=self.username,
        )
