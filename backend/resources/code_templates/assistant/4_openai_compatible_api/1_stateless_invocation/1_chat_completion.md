### Chat completion

The OpenAI compatible API provides a chat completion endpoint that allows you to interact with your models and assistants with responses in OpenAI's response schema.

#### Single round chat completion

```bash
curl -X POST $$SERVICE_HOST$$/v1/chat/completions \
     -H "Authorization: Bearer $$TASKINGAI_API_KEY$$" \
     -H "Content-Type: application/json" \
     -d '{
          "model": "$$ASSISTANT_ID$$",
          "stream": false,
          "messages": [
            {
              "content": "What is the sum of 12 + 23?",
              "role": "user"
            }
          ],
        }'
```

#### Multi-round chat completion

```bash
curl -X POST $$SERVICE_HOST$$/v1/chat/completions \
     -H "Authorization: Bearer $$TASKINGAI_API_KEY$$" \
     -H "Content-Type: application/json" \
     -d '{
          "model": "$$ASSISTANT_ID$$",
          "stream": false,
          "messages": [
            {
              "content": "What is the sum of 12 + 23?",
              "role": "user"
            },
            {
              "content": "The result of 12 + 23 is 35.",
              "role": "assistant"
            },
            {
              "content": "Thank you. What is the product of 12 * 23?",
              "role": "user"
            }
          ],
        }'
```

For more information about chat completion including stream mode and function calls, please refer to the [documentation](https://docs.tasking.ai/docs/guide/sdks/python/assistant/stateless_invocations).
