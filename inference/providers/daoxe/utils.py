from provider_dependency.chat_completion import *

__all__ = [
    "build_daoxe_header",
]


def build_daoxe_header(credentials: ProviderCredentials):
    return {
        "Authorization": f"Bearer {credentials.DAOXE_API_KEY}",
        "Content-Type": "application/json",
    }
