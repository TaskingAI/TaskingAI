from typing import Dict, List
from tkhelper.models import ModelEntity, RedisOperator
from tkhelper.models.operator.postgres_operator import PostgresModelOperator
from tkhelper.utils import load_json_attr

from app.database import redis_conn, postgres_pool

__all__ = ["BundleInstance", "bundle_instance_ops"]


class BundleInstance(ModelEntity):
    bundle_instance_id: str

    encrypted_credentials: Dict
    display_credentials: Dict
    bundle_id: str  # get bundle_id from plugin service
    name: str

    metadata: Dict

    created_timestamp: int
    updated_timestamp: int

    @staticmethod
    def build(row):
        return BundleInstance(
            bundle_instance_id=row["bundle_instance_id"],
            encrypted_credentials=load_json_attr(row, "encrypted_credentials", {}),
            display_credentials=load_json_attr(row, "display_credentials", {}),
            bundle_id=row["bundle_id"],
            name=row["name"],
            metadata=load_json_attr(row, "metadata", {}),
            created_timestamp=row["created_timestamp"],
            updated_timestamp=row["updated_timestamp"],
        )

    def to_response_dict(self) -> Dict:
        return {
            "object": "BundleInstance",
            "bundle_instance_id": self.bundle_instance_id,
            "display_credentials": self.display_credentials,
            "bundle_id": self.bundle_id,
            "name": self.name,
            "metadata": self.metadata,
            "created_timestamp": self.created_timestamp,
            "updated_timestamp": self.updated_timestamp,
        }

    @staticmethod
    def object_name() -> str:
        return "bundle_instance"

    @staticmethod
    def object_plural_name() -> str:
        return "bundle_instances"

    @staticmethod
    def table_name() -> str:
        return "bundle_instance"

    @staticmethod
    def id_field_name() -> str:
        return "bundle_instance_id"

    @staticmethod
    def primary_key_fields() -> List[str]:
        return ["bundle_instance_id"]

    @staticmethod
    def generate_random_id() -> str:
        # currently, we directly use the bundle_id
        raise NotImplementedError

    @staticmethod
    def list_prefix_filter_fields() -> List[str]:
        return ["bundle_instance_id", "name"]

    @staticmethod
    def parent_models() -> List:
        return []

    @staticmethod
    def parent_operator() -> List:
        return []

    @staticmethod
    def create_fields() -> List[str]:
        raise NotImplementedError

    @staticmethod
    def update_fields() -> List[str]:
        raise NotImplementedError

    @staticmethod
    def fields_exclude_in_response():
        return ["encrypted_credentials"]


bundle_instance_ops = PostgresModelOperator(
    postgres_pool=postgres_pool,
    entity_class=BundleInstance,
    redis=RedisOperator(
        entity_class=BundleInstance,
        redis_conn=redis_conn,
    ),
)
