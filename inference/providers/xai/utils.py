from provider_dependency.chat_completion import *

__all__ = [
    "build_xai_header",
]


def build_xai_header(credentials: ProviderCredentials):
    return {
        "Authorization": f"Bearer {credentials.XAI_API_KEY}",
        "Content-Type": "application/json",
    }
