import tiktoken
from ._base import ChatMemoryMessageRole
from common.models import MessageRole

tokenizer = tiktoken.encoding_for_model("text-embedding-ada-002")


# currently we simply use the same tokenizer for all models
def count_tokens(text: str) -> int:
    if not text or not isinstance(text, str):
        return 0
    tokens = tokenizer.encode(text)
    return len(tokens)


def message_role_to_memory_role(message_role: MessageRole):
    return ChatMemoryMessageRole.user if message_role == MessageRole.USER else ChatMemoryMessageRole.assistant
