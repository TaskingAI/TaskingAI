### Text Embedding

The OpenAI compatible API provides a chat completion endpoint that allows you to interact with your models and assistants with responses in OpenAI's response schema.

#### Single usage

```bash
curl -X POST $$SERVICE_HOST$$/v1/embeddings \
     -H "Authorization: Bearer $$TASKINGAI_API_KEY$$" \
     -H "Content-Type: application/json" \
     -d '{
          "model": "$$MODEL_ID$$",
          "input": "Hello!",
          "encoding_format": "float"
        }'
```

#### Batch usage

```bash
curl -X POST $$SERVICE_HOST$$/v1/embeddings \
     -H "Authorization: Bearer $$TASKINGAI_API_KEY$$" \
     -H "Content-Type: application/json" \
     -d '{
          "model": "$$MODEL_ID$$",
          "input": [
            "Hello!",
            "How are you?",
            "I am fine."
          ]
          "encoding_format": "float"
        }'
```
