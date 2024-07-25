from pydantic import BaseModel
from typing import Dict
from .utils import i18n_text

__all__ = ["Provider"]

from config import CONFIG


class ProviderResource(BaseModel):
    taskingai_documentation_url: str
    official_site_url: str
    official_pricing_url: str
    official_credentials_url: str


class Provider(BaseModel):
    provider_id: str
    name: str
    description: str
    credentials_schema: Dict
    icon_svg_url: str
    resources: ProviderResource
    updated_timestamp: int
    enable_proxy: bool
    enable_custom_headers: bool
    return_token_usage: bool
    return_stream_token_usage: bool

    @staticmethod
    def object_name():
        return "Provider"

    @classmethod
    def build(cls, row: Dict):
        try:
            provider_id = row["provider_id"]
            icon_svg_url = f"{CONFIG.IMAGE_URL_PREFIX}/providers/icons/{provider_id}.svg"
            resources_data = row["resources"]

            return cls(
                provider_id=provider_id,
                credentials_schema=row.get("credentials_schema"),
                name=row["name"],
                description=row["description"],
                icon_svg_url=icon_svg_url,
                resources=ProviderResource(**resources_data),
                updated_timestamp=row["updated_timestamp"],
                enable_proxy=row.get("enable_proxy", False),
                enable_custom_headers=row.get("enable_custom_headers", False),
                return_token_usage=row.get("return_token_usage", False),
                return_stream_token_usage=row.get("return_stream_token_usage", False),
            )
        except KeyError as e:
            error_msg = f"Missing key '{e.args[0]}' for provider '{provider_id}'. Please check the data."
            raise KeyError(error_msg) from e

    def to_dict(self, lang: str):
        properties_dict = self.credentials_schema.get("properties", {})
        credentials_schema_dict = {
            "type": "object",
            "properties": {
                k: {
                    "type": v["type"],
                    "description": i18n_text(self.provider_id, v["description"], lang),
                    "secret": v.get("secret", False),
                }
                for k, v in properties_dict.items()
            },
            "required": self.credentials_schema.get("required", []),
        }
        return {
            "object": self.object_name(),
            "provider_id": self.provider_id,
            "name": i18n_text(self.provider_id, self.name, lang),
            "description": i18n_text(self.provider_id, self.description, lang),
            "credentials_schema": credentials_schema_dict,
            "icon_svg_url": self.icon_svg_url,
            "resources": self.resources.model_dump(),
            "updated_timestamp": self.updated_timestamp,
            "enable_proxy": self.enable_proxy,
            "enable_custom_headers": self.enable_custom_headers,
        }

    def allowed_credential_names(self):
        return [k for k in self.credentials_schema["properties"]]

    def required_credential_names(self):
        return [k for k in self.credentials_schema["required"]]
