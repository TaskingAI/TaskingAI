### Delete an Assistant

```python
import taskingai

await taskingai.assistant.a_delete_assistant(assistant_id="$$ASSISTANT_ID$$")
```

When executed, the assistant is permanently removed from the project and all the chats and messages associated with it are also deleted.
