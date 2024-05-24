### List Messages

```python
import taskingai

chats = taskingai.assistant.list_messages(
    assistant_id="$$ASSISTANT_ID$$",
    chat_id="$$CHAT_ID$$",
    order="desc",
    limit=20,
    after="$$MESSAGE_ID$$",
)
```

Parameters and Usage:

- `limit`: Sets the maximum number of chats to return in the list. It should be in the range of 1 to 100.
- `order`: `desc` or `asc`. Determines the order in which the assistants are listed. The sort key is the `created_timestamp` field of the message.
- `before`/`after`: It specifies the point before/after which the next set of messages should be fetched.

The method will return a list of Message objects representing the messages in the chat session.
