from provider_dependency.chat_completion import *

__all__ = [
    "build_leptonai_header",
]


def build_leptonai_header(credentials: ProviderCredentials):
    return {
        "Authorization": f"Bearer {credentials.LEPTONAI_API_KEY}",
        "Content-Type": "application/json",
    }
