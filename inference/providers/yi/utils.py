from provider_dependency.chat_completion import *

__all__ = [
    "build_yi_header",
]


def build_yi_header(credentials: ProviderCredentials):
    return {
        "Authorization": f"Bearer {credentials.YI_API_KEY}",
        "Content-Type": "application/json",
    }
