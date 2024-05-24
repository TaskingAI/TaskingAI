### Create a collection

```bash
curl -X POST $$SERVICE_HOST$$/v1/collections \
     -H "Authorization: Bearer $$API_KEY$$" \
     -H "Content-Type: application/json" \
     -d '{
          "name": "History of Art",
          "description": "",
          "capacity": 1000,
          "embedding_model_id": "$$MODEL_ID$$",
          "metadata": {}
        }'
```

Please properly set collection name and description with meaningful texts. This may affect the performance of your retrieval system.
