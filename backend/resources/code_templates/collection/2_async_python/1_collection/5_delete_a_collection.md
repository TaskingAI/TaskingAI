### Delete a collection

```python
import taskingai

await taskingai.retrieval.a_delete_collection(collection_id="$$COLLECTION_ID$$")
```

When executed, the specified collection is permanently removed from the project and the records and chunks associated with it are also deleted.

Be cautious when deleting a collection especially when it is already associated with an assistant.
Deletion may cause the Assistant to receive unexpected errors when generating response messages.
