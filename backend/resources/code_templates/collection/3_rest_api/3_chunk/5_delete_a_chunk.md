### Delete a chunk

```bash
curl -X DELETE $$SERVICE_HOST$$/v1/collections/$$COLLECTION_ID$$/chunks/$$CHUNK_ID$$ \
     -H "Authorization: Bearer $$API_KEY$$" \
     -H "Content-Type: application/json"
```

Once executed, the specified chunk is permanently removed from the collection. But at record-level, the record still exists if the deleted chunk was created by creating a record.
