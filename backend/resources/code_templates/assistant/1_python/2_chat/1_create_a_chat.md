### Create a Chat

```python
chat: Chat = taskingai.assistant.create_chat(
    assistant_id="$$ASSISTANT_ID$$",
    name='new chat',
    metadata={
        "user_country": "Australia",
        "user_age": "25",
    },
)
```

The metadata can be used to store any information that you want to associate with the chat session.
