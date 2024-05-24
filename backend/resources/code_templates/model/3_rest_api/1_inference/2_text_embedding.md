### Text Embedding

#### Single usage

```bash
curl -X POST $$SERVICE_HOST$$/v1/inference/text_embedding \
     -H "Authorization: Bearer $$API_KEY$$" \
     -H "Content-Type: application/json" \
     -d '{
          "model_id": "$$MODEL_ID$$",
          "input": "Hello!",
          "input_type": "text"
        }'
```

#### Batch usage

```bash
curl -X POST $$SERVICE_HOST$$/v1/inference/text_embedding \
     -H "Authorization: Bearer $$API_KEY$$" \
     -H "Content-Type: application/json" \
     -d '{
          "model_id": "$$MODEL_ID$$",
          "input": [
            "Hello!",
            "How are you?",
            "I am fine."
          ]
          "input_type": "text"
        }'
```
