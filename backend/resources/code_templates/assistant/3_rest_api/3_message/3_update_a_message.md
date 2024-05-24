### Update a Message

```bash
curl -X POST $$SERVICE_HOST$$/v1/assistants/$$ASSISTANT_ID$$/chats/$$CHAT_ID$$/messages/$$MESSAGE_ID$$ \
     -H "Authorization: Bearer $$API_KEY$$" \
     -H "Content-Type: application/json" \
     -d '{
          "metadata": {}
        }'
```

Only `metadata` is editable in a message. When executed, the message is updated with the new metadata.
