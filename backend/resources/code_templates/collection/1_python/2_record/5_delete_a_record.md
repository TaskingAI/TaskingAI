### Delete a record

```python
import taskingai

taskingai.retrieval.delete_record(
    collection_id="$$COLLECTION_ID$$",
    record_id="$$RECORD_ID$$"
)
```

Once executed, the specified record is permanently removed from the collection and the chunks associated with it are also deleted.
