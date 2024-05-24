### Update a chunk

```bash
curl -X POST $$SERVICE_HOST$$/v1/collections/$$COLLECTION_ID$$/chunks/$$CHUNK_ID$$ \
     -H "Authorization: Bearer $$API_KEY$$" \
     -H "Content-Type: application/json" \
     -d '{
          "content": "new text content of the chunk",
          "metadata": {}
        }'
```
