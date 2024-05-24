### Delete a chunk

```python
import taskingai

# delete chunk
await taskingai.retrieval.a_delete_chunk(
    collection_id="$$COLLECTION_ID$$",
    chunk_id="$$CHUNK_ID$$",
)
print(f"deleted chunk $$CHUNK_ID$$ from collection $$COLLECTION_ID$$")
```

Once executed, the specified chunk is permanently removed from the collection. But at record-level, the record still exists if the deleted chunk was created by creating a record.
