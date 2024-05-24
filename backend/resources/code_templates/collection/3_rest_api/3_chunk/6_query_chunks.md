### Query chunks

```bash
curl -X POST $$SERVICE_HOST$$/v1/collections/$$COLLECTION_ID$$/chunks/query \
     -H "Authorization: Bearer $$API_KEY$$" \
     -H "Content-Type: application/json" \
     -d '{
          "top_k": 3,
          "max_tokens": 100,
          "query_text": "What is machine learning?"
        }'
```
