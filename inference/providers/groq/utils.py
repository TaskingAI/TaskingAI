from provider_dependency.chat_completion import *

__all__ = [
    "build_groq_header",
]


def build_groq_header(credentials: ProviderCredentials):
    return {
        "Authorization": f"Bearer {credentials.GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
