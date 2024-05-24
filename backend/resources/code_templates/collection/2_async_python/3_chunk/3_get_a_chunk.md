### Get a chunk

```python
import taskingai

chunk = await taskingai.retrieval.a_get_chunk(
    collection_id="$$COLLECTION_ID$$",
    chunk_id="$$CHUNK_ID$$"
)

print(f"got chunk: {chunk}\n")
```
