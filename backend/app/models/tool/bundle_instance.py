from typing import Dict, List
from tkhelper.models import ModelEntity
from tkhelper.utils import load_json_attr

from .plugin import Plugin

__all__ = ["BundleInstance"]


class BundleInstance(ModelEntity):
    bundle_instance_id: str

    encrypted_credentials: Dict
    display_credentials: Dict
    bundle_id: str  # get bundle_id from plugin service
    name: str

    metadata: Dict
    plugins: List[Plugin]
    description: str
    icon_url: str

    created_timestamp: int
    updated_timestamp: int

    @staticmethod
    def build(row):
        from app.services.tool import list_plugins, get_bundle

        try:
            plugins = list_plugins(bundle_id=row["bundle_id"])
        except Exception as e:
            plugins = []

        bundle = get_bundle(row["bundle_id"])

        return BundleInstance(
            bundle_instance_id=row["bundle_instance_id"],
            encrypted_credentials=load_json_attr(row, "encrypted_credentials", {}),
            display_credentials=load_json_attr(row, "display_credentials", {}),
            bundle_id=row["bundle_id"],
            name=row["name"],
            metadata=load_json_attr(row, "metadata", {}),
            plugins=plugins,
            description=bundle.description,
            icon_url=bundle.icon_url,
            created_timestamp=row["created_timestamp"],
            updated_timestamp=row["updated_timestamp"],
        )

    def to_response_dict(self, **kwargs) -> Dict:
        from app.services.tool import i18n_text

        # todo: currently we only support en
        lang = kwargs.get("lang", "en")
        return {
            "object": "BundleInstance",
            "bundle_instance_id": self.bundle_instance_id,
            "display_credentials": self.display_credentials,
            "bundle_id": self.bundle_id,
            "name": self.name,
            "metadata": self.metadata,
            "plugins": [plugin.to_dict(lang=lang) for plugin in self.plugins],
            "description": i18n_text(self.bundle_id, self.description, lang),
            "icon_url": self.icon_url,
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
