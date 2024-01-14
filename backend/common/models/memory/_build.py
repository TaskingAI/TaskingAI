from .naive import *
from .message_window import *
from .zero import *


def build_chat_memory(memory_dict: Optional[Dict]) -> Optional[ChatMemory]:
    memory_type = memory_dict.get("type")
    if memory_type is None:
        return None

    # Depending on the type of memory, initialize the appropriate memory instance
    if memory_type == MemoryType.zero:
        # Zero memory doesn't require additional information
        messages = []
        if memory_dict and "messages" in memory_dict:
            for msg in memory_dict["messages"]:
                messages.append(ChatMemoryMessage(**msg))
        return ChatZeroMemory(messages=messages)

    elif memory_type == MemoryType.naive:
        # Naive memory might include a list of messages
        messages = []
        if memory_dict and "messages" in memory_dict:
            for msg in memory_dict["messages"]:
                messages.append(ChatMemoryMessage(**msg))
        return ChatNaiveMemory(messages=messages)

    elif memory_type == MemoryType.message_window:
        # Message window memory also includes a list of messages
        messages = []
        if memory_dict and "messages" in memory_dict:
            for msg in memory_dict["messages"]:
                messages.append(ChatMemoryMessage(**msg))
        max_messages = memory_dict.get("max_messages")
        max_tokens = memory_dict.get("max_tokens")
        return ChatMessageWindowMemory(messages=messages, max_messages=max_messages, max_tokens=max_tokens)

    else:
        # If the memory type is unknown, return None
        return None


def build_assistant_memory(memory_dict: Dict) -> Optional[AssistantMemory]:
    if not isinstance(memory_dict, Dict):
        return None

    # Check if the memory dictionary is provided and has the 'type' key
    if not memory_dict or "type" not in memory_dict:
        return None

    memory_type = memory_dict["type"]

    if memory_type == MemoryType.zero.value:
        # For zero memory, no additional information is needed
        return AssistantZeroMemory()

    elif memory_type == MemoryType.naive.value:
        # For naive memory, no additional configuration is needed
        return AssistantNaiveMemory()

    elif memory_type == MemoryType.message_window.value:
        # For message window memory, additional configuration is needed
        max_messages = memory_dict.get("max_messages")
        max_tokens = memory_dict.get("max_tokens")

        # Validate that required fields are present
        if max_messages is None or max_tokens is None:
            return None

        return AssistantMessageWindowMemory(max_messages=max_messages, max_tokens=max_tokens)

    else:
        # If the memory type is unknown, return None
        return None
