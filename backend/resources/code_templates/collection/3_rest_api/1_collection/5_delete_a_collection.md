### Delete a collection

```bash
curl -X DELETE $$SERVICE_HOST$$/v1/collections/$$COLLECTION_ID$$ \
     -H "Authorization: Bearer $$API_KEY$$" \
     -H "Content-Type: application/json"
```

When executed, the specified collection is permanently removed from the project and the records and chunks associated with it are also deleted.

Be cautious when deleting a collection especially when it is already associated with an assistant.
Deletion may cause the Assistant to receive unexpected errors when generating response messages.
