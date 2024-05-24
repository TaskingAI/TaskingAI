### Update a Chat

```bash
curl -X POST $$SERVICE_HOST$$/v1/assistants/$$ASSISTANT_ID$$/chats/$$CHAT_ID$$ \
     -H "Authorization: Bearer $$API_KEY$$" \
     -H "Content-Type: application/json" \
     -d '{
            "name": "Updated chat name",
            "metadata": {
              "key1": "value2"
            }
        }'
```
