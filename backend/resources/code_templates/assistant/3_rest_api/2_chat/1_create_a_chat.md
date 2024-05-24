### Create a Chat

```bash
curl -X POST $$SERVICE_HOST$$/v1/assistants/$$ASSISTANT_ID$$/chats \
     -H "Authorization: Bearer $$API_KEY$$" \
     -H "Content-Type: application/json" \
     -d '{
            "name": "Name",
            "metadata": {
              "key1": "value1"
            }
        }'
```

The metadata can be used to store any information that you want to associate with the chat session.
