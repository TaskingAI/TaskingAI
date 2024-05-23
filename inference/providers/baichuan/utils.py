from provider_dependency.chat_completion import *

__all__ = [
    "build_baichuan_header",
]


def build_baichuan_header(credentials: ProviderCredentials):
    return {
        "Authorization": f"Bearer {credentials.BAICHUAN_API_KEY}",
        "Content-Type": "application/json",
    }
