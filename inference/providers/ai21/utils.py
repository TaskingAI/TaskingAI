from provider_dependency.chat_completion import *

__all__ = [
    "build_ai21_header",
]


def build_ai21_header(credentials: ProviderCredentials):
    return {
        "Authorization": f"Bearer {credentials.AI21_API_KEY}",
        "Content-Type": "application/json",
    }
