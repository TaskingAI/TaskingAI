### Update a Message

```python
import taskingai

# Only metadata can be updated
updated_message = await taskingai.assistant.a_update_message(
    assistant_id="$$ASSISTANT_ID$$",
    chat_id="$$CHAT_ID$$",
    message_id="$$MESSAGE_ID$$",
    # Replace with the actual values
    metadata={
        "user_agent": "Mozilla/5.0",
    }
)
```
