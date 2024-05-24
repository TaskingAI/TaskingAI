### Update a Chat

```python
import taskingai
from taskingai.assistant.chat import Chat

chat: Chat = await taskingai.assistant.a_update_chat(
    assistant_id="$$ASSISTANT_ID$$",
    chat_id="$$CHAT_ID$$",
    name='updated chat name',
    metadata={
        "user_country": "Canada",
        "user_age": "28",
    },
)
print(f"updated chat: {chat}\n")
```
