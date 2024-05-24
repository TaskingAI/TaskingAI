### Chat completion

#### Single round chat completion

```bash
curl -X POST $$SERVICE_HOST$$/v1/inference/chat_completion \
     -H "Authorization: Bearer $$API_KEY$$" \
     -H "Content-Type: application/json" \
     -d '{
          "model_id": "$$MODEL_ID$$",
          "configs": {
            "temperature": 0.5
          },
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
curl -X POST $$SERVICE_HOST$$/v1/inference/chat_completion \
     -H "Authorization: Bearer $$API_KEY$$" \
     -H "Content-Type: application/json" \
     -d '{
          "model_id": "$$MODEL_ID$$",
          "configs": {
            "temperature": 0.5
          },
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

For more information about chat completion including stream mode and function calls, please refer to the [documentation](https://docs.tasking.ai/docs/guide/model/manage_models/chat-completion/).
