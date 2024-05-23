from provider_dependency.chat_completion import *

__all__ = [
    "build_openai_header",
]


def build_openai_header(credentials: ProviderCredentials):
    return {
        "Authorization": f"Bearer {credentials.OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
