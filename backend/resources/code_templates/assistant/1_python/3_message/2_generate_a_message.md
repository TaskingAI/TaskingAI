### Generate a message

#### Normal generation

```python
import taskingai
from taskingai.assistant.message import Message

assistant_message: Message = taskingai.assistant.generate_message(
    assistant_id="$$ASSISTANT_ID$$",
    chat_id="$$CHAT_ID$$",
)
```

#### Generation with variable values for system prompt template

```python
assistant_message: Message = taskingai.assistant.generate_message(
    assistant_id="$$ASSISTANT_ID$$",
    chat_id="$$CHAT_ID$$",
    # Replace with the actual values
    system_prompt_variables={
        "language": "Spanish",
        "country": "Spain"
    }
)
```

#### Generation with streaming

```python
from taskingai.assistant import MessageChunk

assistant_message_response = taskingai.assistant.generate_message(
    assistant_id="$$ASSISTANT_ID$$",
    chat_id="$$CHAT_ID$$",
    system_prompt_variables={
        "language": "English"
    },
    stream=True,
)

print(f"Assistant:", end=" ", flush=True)
for item in assistant_message_response:
    if isinstance(item, MessageChunk):
        print(item.delta, end="", flush=True)
```
