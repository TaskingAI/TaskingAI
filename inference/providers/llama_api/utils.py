from provider_dependency.chat_completion import *

__all__ = [
    "build_llama_api_header",
]


def build_llama_api_header(credentials: ProviderCredentials):
    return {
        "Authorization": f"Bearer {credentials.LLAMA_API_API_KEY}",
        "Content-Type": "application/json",
    }
