from openai import OpenAI
from backend.tests.common.config import CONFIG

client = OpenAI(
    api_key=CONFIG.Authentication,
    base_url=CONFIG.OAPI_BASE_URL,
)
OPENAI_TEXT_EMBEDDING_MODEL_ID = CONFIG.text_embedding_model_id
OPENAI_CHAT_COMPLETION_MODEL_ID = CONFIG.chat_completion_model_id
