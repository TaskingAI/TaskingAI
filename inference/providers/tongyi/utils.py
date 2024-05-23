from provider_dependency.chat_completion import *

__all__ = ["build_tongyi_header", "build_tongyi_header_stream"]


def build_tongyi_header(credentials: ProviderCredentials):
    return {
        "Authorization": f"Bearer {credentials.TONGYI_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "*/*",
    }


def build_tongyi_header_stream(credentials: ProviderCredentials):
    return {
        "Authorization": f"Bearer {credentials.TONGYI_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
    }
