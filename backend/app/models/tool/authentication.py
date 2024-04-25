from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, Dict
from tkhelper.encryption.aes import aes_encrypt, aes_decrypt
import logging

logger = logging.getLogger(__name__)

__all__ = ["ActionAuthentication", "ActionAuthenticationType", "validate_authentication_data"]


class ActionAuthenticationType(str, Enum):
    bearer = "bearer"
    basic = "basic"
    custom = "custom"
    none = "none"


def validate_authentication_data(data: Dict):
    if not isinstance(data, dict):
        raise ValueError("Authentication should be a dict.")

    if "type" not in data or not data.get("type"):
        raise ValueError("Type is required for authentication.")

    if data["type"] == ActionAuthenticationType.custom:
        if "content" not in data or data["content"] is None:
            raise ValueError("Content is required for custom authentication.")
        if data["content"] and not isinstance(data["content"], dict):
            raise ValueError("Content should be a dict for custom authentication.")
        for key in data["content"]:
            if not isinstance(key, str) or not key:
                raise ValueError("Key in content should be a string.")
            if not isinstance(data["content"][key], str) or not data["content"][key]:
                raise ValueError("Value in content should be a string.")

    elif data["type"] == ActionAuthenticationType.bearer:
        if "secret" not in data or data["secret"] is None:
            raise ValueError(f'Secret is required for {data["type"]} authentication.')

    elif data["type"] == ActionAuthenticationType.basic:
        if "secret" not in data or data["secret"] is None:
            raise ValueError(f'Secret is required for {data["type"]} authentication.')
        # assume the secret is a base64 encoded string

    elif data["type"] == ActionAuthenticationType.none:
        data["secret"] = None
        data["content"] = None

    return data


class ActionAuthentication(BaseModel):
    encrypted: bool = Field(False)
    type: ActionAuthenticationType = Field(...)
    secret: Optional[str] = Field(None, min_length=1, max_length=1024)
    content: Optional[Dict] = Field(None)

    def is_encrypted(self):
        return self.encrypted or self.type == ActionAuthenticationType.none

    def encrypt(self):
        # logger.debug("------------------- Encryption Start -------------------")
        # logger.debug(f"Before encryption: {self.model_dump_json()}")

        if self.encrypted or self.type == ActionAuthenticationType.none:
            return
        if self.secret is not None:
            self.secret = aes_encrypt(self.secret)
        if self.content is not None:
            for key in self.content:
                self.content[key] = aes_encrypt(self.content[key])
        self.encrypted = True

        # logger.debug(f"After encryption: {self.model_dump_json()}")
        # logger.debug("------------------- Encryption End -------------------")

    def decrypt(self):
        # logger.debug("------------------- Decryption Start -------------------")
        # logger.debug(f"Before decryption: {self.model_dump_json()}")

        if not self.encrypted or self.type == ActionAuthenticationType.none:
            return
        if self.secret is not None:
            self.secret = aes_decrypt(self.secret)
        if self.content is not None:
            for key in self.content:
                self.content[key] = aes_decrypt(self.content[key])
        self.encrypted = False

        # logger.debug(f"After decryption: {self.model_dump_json()}")
        # logger.debug("------------------- Decryption End -------------------")

    def to_display_dict(self):
        if self.encrypted:
            raise ValueError("The authentication is not ready for display.")

        model_dict = self.model_dump()
        # make secret and all content value in "xx****xx" format
        if self.secret:
            if len(self.secret) > 4:
                model_dict["secret"] = f"{self.secret[:2]}****{self.secret[-2:]}"

        if self.content:
            for key in self.content:
                if self.content[key] and len(self.content[key]) > 4:
                    model_dict["content"][key] = f"{self.content[key][:2]}****{self.content[key][-2:]}"

        return model_dict
