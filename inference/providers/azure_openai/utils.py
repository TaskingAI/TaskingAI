from app.models import ProviderCredentials


def build_azure_chat_url(credentials: ProviderCredentials):
    api_version = credentials.AZURE_OPENAI_API_VERSION if credentials.AZURE_OPENAI_API_VERSION else "2023-05-15"
    api_url = (
        f"https://{credentials.AZURE_OPENAI_RESOURCE_NAME}.openai.azure.com/openai/deployments/"
        f"{credentials.AZURE_OPENAI_DEPLOYMENT_ID}/chat/completions?api-version={api_version}"
    )
    return api_url


def build_azure_text_url(credentials: ProviderCredentials):
    api_version = credentials.AZURE_OPENAI_API_VERSION if credentials.AZURE_OPENAI_API_VERSION else "2023-05-15"
    api_url = (
        f"https://{credentials.AZURE_OPENAI_RESOURCE_NAME}.openai.azure.com/openai/deployments/"
        f"{credentials.AZURE_OPENAI_DEPLOYMENT_ID}/embeddings?api-version={api_version}"
    )
    return api_url


def build_azure_openai_header(credentials: ProviderCredentials):
    return {"api-key": f"{credentials.AZURE_OPENAI_API_KEY}", "Content-Type": "application/json"}
