### Text Embedding

The OpenAI compatible API provides a chat completion endpoint that allows you to interact with your models and assistants with responses in OpenAI's response schema.

#### Single usage (cURL)

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

### Single usage (Python)
```python
from openai import OpenAI

client = OpenAI(
    api_key="$$TASKINGAI_API_KEY$$",
    base_url="$$SERVICE_HOST$$/v1",
)

response = client.embeddings.create(
    model="$$MODEL_ID$$",
    input=["Hello!"]
)

print(response)
```
For batch usage, simply add more strings to the list in the `input` field.


#### Batch usage (cURL)

```bash
curl -X POST $$SERVICE_HOST$$/v1/embeddings \
     -H "Authorization: Bearer $$TASKINGAI_API_KEY$$" \
     -H "Content-Type: application/json" \
     -d '{
          "model": "$$MODEL_ID$$",
          "input": [
            "Hello!",
            "How are you?",
            "I am good."
          ],
          "encoding_format": "float"
        }'
```
