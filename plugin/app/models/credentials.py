from pydantic import BaseModel, Field
from app.utils import aes_encrypt, aes_decrypt
from config import load_str_env
from typing import Dict

__all__ = ["BundleCredentials", "validate_bundle_credentials"]


class BundleCredentials(BaseModel):

    credentials: Dict[str, str] = Field({})

    def __getattr__(self, item):
        # This method is called only if Python doesn't find the attribute
        # in the usual places (instance dictionary or class hierarchy).
        if item in self.credentials:
            return self.credentials.get(item)
        else:
            # If the item is not in credentials return None
            return None

    def encrypt(self):
        for key, value in self.credentials.items():
            if value is not None:
                encrypted_value = aes_encrypt(value)
                self.credentials[key] = str(encrypted_value)
        return self

    def decrypt(self):
        for key, value in self.credentials.items():
            if value is not None:
                if "," in value:
                    try:
                        decrypted_value = aes_decrypt(value)
                        self.credentials[key] = str(decrypted_value)
                    except ValueError as e:
                        raise ValueError(f"error decrypting {key}: {e}")
                else:
                    raise ValueError(f"invalid credentials. Not encrypted: {value}")
        return self

    def load_input(self, bundle_id, credentials: Dict[str, str]):
        try:
            from app.cache import get_bundle

            allowed_fields = get_bundle(bundle_id).allowed_credential_names()
            for field in allowed_fields:
                if field in credentials:
                    self.credentials[field] = credentials[field]
            return self
        except Exception as e:
            raise ValueError(f"error loading credentials from input: {e}")

    def load_default(self, bundle_id):
        try:
            from app.cache import get_bundle

            bundle_schemas = get_bundle(bundle_id).credentials_schema
            for credential_name in bundle_schemas:
                credential_schema = bundle_schemas[credential_name]
                credential_required = credential_schema.get("required", True)
                self.credentials[credential_name] = load_str_env(credential_name, required=credential_required)
            return self
        except Exception as e:
            raise ValueError(f"error loading credentials from env: {e}")

    def to_dict(self, bundle_id):
        from app.cache import get_bundle

        allowed_fields = get_bundle(bundle_id).allowed_credential_names()
        res = {field: getattr(self, field, None) for field in allowed_fields}
        return res


def validate_bundle_credentials(data: Dict) -> BundleCredentials:
    from app.cache import get_bundle

    bundle_id = data.get("bundle_id")
    if bundle_id and isinstance(bundle_id, str):
        if not get_bundle(bundle_id):
            raise ValueError(f"provider {bundle_id} does not exist.")
    else:
        raise ValueError("bundle_id is required.")

    # handle credentials
    if data.get("credentials") and data.get("encrypted_credentials"):
        raise ValueError("either credentials or encrypted_credentials is required, but not both.")

    credentials = BundleCredentials()

    if data.get("credentials"):
        if not isinstance(data.get("credentials"), dict):
            raise ValueError("credentials must be a dict.")
        credentials.load_input(bundle_id, data.get("credentials"))
    elif data.get("encrypted_credentials"):
        if not isinstance(data.get("encrypted_credentials"), dict):
            raise ValueError("encrypted_credentials must be a dict.")
        credentials.load_input(bundle_id, data.get("encrypted_credentials"))
        credentials.decrypt()
    else:

        try:
            credentials.load_default(bundle_id)
        except Exception as e:
            raise ValueError(f"Failed to load default credentials for provider {bundle_id} from env")

    return credentials
