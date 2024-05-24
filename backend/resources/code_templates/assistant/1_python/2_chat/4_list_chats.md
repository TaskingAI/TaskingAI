### List Chats

```python
import taskingai

chats = taskingai.assistant.list_chats(
    assistant_id="$$ASSISTANT_ID$$",
    order="desc",
    limit=20
)
```

Parameters and Usage:

- `limit`: Sets the maximum number of chats to return in the list.
- `order`: `desc` or `asc`. Determines the order in which the assistants are listed. The sort key is the `created_timestamp` field of the chat.
- `before`/`after`: It specifies the point before/after which the next set of chats should be fetched.

The method will return a list of Chat objects, each representing a chat session with the assistant.
