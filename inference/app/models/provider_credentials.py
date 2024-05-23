from pydantic import BaseModel, Field
from .utils import aes_encrypt, aes_decrypt
from config import load_str_env
from typing import Dict, Optional, List, Tuple
from app.error import ErrorCode, raise_http_error
import random

__all__ = ["ProviderCredentials", "validate_credentials"]


class ProviderCredentials(BaseModel):

    credentials: Dict[str, str] = Field({})

    def __getattr__(self, item):
        # This method is called only if Python doesn't find the attribute
        # in the usual places (instance dictionary or class hierarchy).
        # Attempt to get an attribute; return None if not found.
        return self.credentials.get(item, None)

    def encrypt(self):
        for key, value in self.credentials.items():
            if value is not None:
                encrypted_value = aes_encrypt(value)
                self.credentials[key] = str(encrypted_value)
        return self

    def decrypt(self):
        # Decrypt all values in the credentials dictionary.
        for key, value in self.credentials.items():
            if value is not None and "," in value:
                try:
                    decrypted_value = aes_decrypt(value)
                    self.credentials[key] = str(decrypted_value)
                except ValueError as e:
                    raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, f"error decrypting {key}: {e}")
            else:
                raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, f"invalid credentials. Not encrypted: {value}")
        return self

    def load_input(self, provider_id, credentials: Dict[str, str]):
        from app.cache import get_provider

        allowed_fields = get_provider(provider_id).allowed_credential_names()
        required_fields = get_provider(provider_id).required_credential_names()

        def load_credential_set_from_input(suffix=""):
            """Load a set of credentials from input."""
            load_result = {}
            for field in allowed_fields:
                if field in credentials:
                    load_result[field] = credentials[f"{field}{suffix}"]
                else:
                    if field in required_fields:
                        raise_http_error(ErrorCode.REQUEST_VALIDATION_ERROR, f"Required field {field} is missing.")
            return load_result

        # Load the default credential set
        credentials_set = [load_credential_set_from_input()]

        # Try to load additional credential sets
        count = 1
        while True:
            try:
                next_credentials = load_credential_set_from_input(f"_{count}")
                credentials_set.append(next_credentials)
                count += 1
            except Exception:
                break
        # Choose a random set of credentials
        chosen_credentials = random.choice(credentials_set)
        for key, value in chosen_credentials.items():
            self.credentials[key] = value
        return self

    def load_default(self, provider_id):
        from app.cache import get_provider

        # Get the allowed and required credential names
        allowed_fields = get_provider(provider_id).allowed_credential_names()
        required_fields = get_provider(provider_id).required_credential_names()

        def load_credential_set(suffix=""):
            """Load a set of credentials from environment variables."""
            load_result = {}
            for name in allowed_fields:
                load_result[name] = load_str_env(f"{name}{suffix}", required=name in required_fields)
            return load_result

        # Load the default credential set
        credentials_set = [load_credential_set()]

        # Try to load additional credential sets
        count = 1
        while True:
            try:
                next_credentials = load_credential_set(f"_{count}")
                credentials_set.append(next_credentials)
                count += 1
            except Exception:
                break

        # Choose a random set of credentials
        chosen_credentials = random.choice(credentials_set)
        for key, value in chosen_credentials.items():
            self.credentials[key] = value
        return self

    def to_dict(self, provider_id):
        from app.cache import get_provider

        allowed_fields = get_provider(provider_id).allowed_credential_names()
        return {field: self.credentials.get(field) for field in allowed_fields}


def validate_credentials(
    model_infos: Optional[List[Tuple]],
    credentials_dict: Optional[Dict],
    encrypted_credentials_dict: Optional[Dict],
) -> ProviderCredentials:
    """
    Validate credentials of a provider
    :param model_infos: the model info list
    :param credentials_dict: the credentials dictionary
    :param encrypted_credentials_dict: the encrypted credentials dictionary
    :return: a ProviderCredentials object with validated credentials
    """
    credentials = ProviderCredentials()
    for model in model_infos:
        provider_id = model[0].provider_id

        # handle credentials
        if credentials_dict and encrypted_credentials_dict:
            raise_http_error(
                ErrorCode.REQUEST_VALIDATION_ERROR,
                "either credentials or encrypted_credentials is required, but not both.",
            )

        if credentials_dict:
            credentials.load_input(provider_id, credentials_dict)
        elif encrypted_credentials_dict:
            try:
                credentials.load_input(provider_id, encrypted_credentials_dict)
                credentials.decrypt()
            except Exception as e:
                raise_http_error(
                    ErrorCode.REQUEST_VALIDATION_ERROR,
                    f"The encrypted credentials are invalid.",
                )
        else:
            credentials.load_default(provider_id)
    return credentials
