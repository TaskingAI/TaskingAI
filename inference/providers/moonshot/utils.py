from provider_dependency.chat_completion import *

__all__ = [
    "build_moonshot_header",
]


def build_moonshot_header(credentials: ProviderCredentials):
    return {
        "Authorization": f"Bearer {credentials.MOONSHOT_API_KEY}",
        "Content-Type": "application/json",
    }
