### Delete an Assistant

```bash
curl -X DELETE $$SERVICE_HOST$$/v1/assistants/$$ASSISTANT_ID$$ \
     -H "Authorization: Bearer $$API_KEY$$" \
     -H "Content-Type: application/json" \
```

When executed, the assistant is permanently removed from the project and all the chats and messages associated with it are also deleted.
