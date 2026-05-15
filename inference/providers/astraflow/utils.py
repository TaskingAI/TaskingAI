from provider_dependency.chat_completion import *

__all__ = [
    "build_astraflow_header",
]


def build_astraflow_header(credentials: ProviderCredentials):
    return {
        "Authorization": f"Bearer {credentials.ASTRAFLOW_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
