from provider_dependency.chat_completion import *

__all__ = [
    "build_volcengine_header",
]


def build_volcengine_header(credentials: ProviderCredentials):
    return {
        "Authorization": f"Bearer {credentials.VOLCENGINE_API_KEY}",
        "Content-Type": "application/json",
    }
