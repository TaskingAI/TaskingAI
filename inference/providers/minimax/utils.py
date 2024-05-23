from provider_dependency.chat_completion import *

__all__ = [
    "build_minimax_header",
]


def build_minimax_header(credentials: ProviderCredentials):
    return {
        "Authorization": f"Bearer {credentials.MINIMAX_API_KEY}",
        "Content-Type": "application/json",
    }
