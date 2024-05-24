### Get a Chat

```python
import taskingai
from taskingai.assistant.chat import Chat

chat: Chat = await taskingai.assistant.a_get_chat(
    assistant_id="$$ASSISTANT_ID$$",
    chat_id="$$CHAT_ID$$",
)
```
