import json

from pydantic import BaseModel, Field
from typing import Dict, Optional, List
from app.utils import i18n_text
from config import CONFIG

__all__ = ["Bundle"]


class Bundle(BaseModel):
    bundle_id: str
    provider: str
    developer: str
    name: str
    description: str
    credentials_schema: Dict
    icon_url: str

    @staticmethod
    def object_name():
        return "Bundle"

    @classmethod
    def build(cls, bundle_dict: Dict):
        """
        Build a Bundle object
        :param bundle_dict: the dictionary of the bundle
        :param i18n: the i18n dictionary (language code: {key: value})
        :return: a Bundle object
        """
        bundle_id = bundle_dict["id"]
        return cls(
            bundle_id=bundle_id,
            provider=bundle_dict["provider"],
            developer=bundle_dict["developer"],
            name=bundle_dict["name"],
            description=bundle_dict["description"],
            credentials_schema=bundle_dict.get("credentials_schema", {}),
            icon_url=f"{CONFIG.ICON_URL_PREFIX}/images/plugins/bundles/icons/{bundle_id}.png"
        )

    def to_dict(self, lang: str):
        credentials_schema_dict = {
            k: {
                "type": v["type"],
                "description": i18n_text(self.bundle_id, v["description"], lang),
                "secret": v.get("secret", False),
                "required": v.get("required", False),
            }
            for k, v in self.credentials_schema.items()
        }

        return {
            "object": self.object_name(),
            "bundle_id": self.bundle_id,
            "provider": self.provider,
            "developer": self.developer,
            "name": i18n_text(self.bundle_id, self.name, lang),
            "description": i18n_text(self.bundle_id, self.description, lang),
            "credentials_schema": credentials_schema_dict,
            "icon_url": self.icon_url,
        }

    def allowed_credential_names(self):
        return [k for k in self.credentials_schema]

    def required_credential_names(self):
        return [
            k for k in self.credentials_schema
            if self.credentials_schema[k].get("required", False)
        ]

class BundleEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Bundle):
            return obj.to_dict('en')
        return json.JSONEncoder.default(self, obj)

