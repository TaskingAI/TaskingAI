from provider_dependency.chat_completion import *

__all__ = [
    "build_siliconcloud_header",
]


def build_siliconcloud_header(credentials: ProviderCredentials):
    return {
        "Authorization": f"Bearer {credentials.SILICONCLOUD_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
