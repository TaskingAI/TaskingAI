from provider_dependency.chat_completion import *

__all__ = [
    "build_togetherai_header",
]


def build_togetherai_header(credentials: ProviderCredentials):
    return {
        "Authorization": f"Bearer {credentials.TOGETHERAI_API_KEY}",
        "Content-Type": "application/json",
    }
