from provider_dependency.chat_completion import *

__all__ = [
    "build_fireworks_header",
]


def build_fireworks_header(credentials: ProviderCredentials):
    return {
        "Authorization": f"Bearer {credentials.FIREWORKS_API_KEY}",
        "Content-Type": "application/json",
    }
