### Delete a record

```bash
curl -X DELETE $$SERVICE_HOST$$/v1/collections/$$COLLECTION_ID$$/record/$$RECORD_ID$$ \
     -H "Authorization: Bearer $$API_KEY$$" \
     -H "Content-Type: application/json"
```

Once executed, the specified record is permanently removed from the collection and the chunks associated with it are also deleted.
