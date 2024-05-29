### Generate a message

#### Normal generation

```bash
curl -X POST $$SERVICE_HOST$$/v1/assistants/$$ASSISTANT_ID$$/chats/$$CHAT_ID$$/generate \
     -H "Authorization: Bearer $$API_KEY$$" \
     -H "Content-Type: application/json" \
     -d '{
          "stream": false,
          "debug": false
        }'
```

#### Generation with variable values for system prompt template

```bash
curl -X POST $$SERVICE_HOST$$/v1/assistants/$$ASSISTANT_ID$$/chats/$$CHAT_ID$$/generate \
     -H "Authorization: Bearer $$API_KEY$$" \
     -H "Content-Type: application/json" \
     -d '{
          "system_prompt_variables": {
            "language": "English"
          },
          "stream": false,
          "debug": false
        }'
```

#### Generation with streaming

```bash
curl -X POST $$SERVICE_HOST$$/v1/assistants/$$ASSISTANT_ID$$/chats/$$CHAT_ID$$/generate \
     -H "Authorization: Bearer $$API_KEY$$" \
     -H "Content-Type: application/json" \
     -d '{
          "system_prompt_variables": {
            "language": "English"
          },
          "stream": True,
          "debug": false
        }'
```
