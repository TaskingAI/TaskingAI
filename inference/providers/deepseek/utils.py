from provider_dependency.chat_completion import *

__all__ = [
    "build_deepseek_header",
]


def build_deepseek_header(credentials: ProviderCredentials):
    return {
        "Authorization": f"Bearer {credentials.DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }
