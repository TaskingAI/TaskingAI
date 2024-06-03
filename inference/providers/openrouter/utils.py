from provider_dependency.chat_completion import *

__all__ = [
    "build_openrouter_header",
]


def build_openrouter_header(credentials: ProviderCredentials):
    return {
        "Authorization": f"Bearer {credentials.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
