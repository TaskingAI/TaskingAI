### Update a collection

```bash
curl -X POST $$SERVICE_HOST$$/v1/collections/$$COLLECTION_ID$$ \
     -H "Authorization: Bearer $$API_KEY$$" \
     -H "Content-Type: application/json" \
     -d '{
          "name": "Updated collection name",
          "description": "Updated collection description",
          "metadata": {}
        }'
```

Only name, description, and metadata are supported for updating a collection. The metadata attribute will have no effect on information retrieval performance; it is only for storing additional information for the collection.
