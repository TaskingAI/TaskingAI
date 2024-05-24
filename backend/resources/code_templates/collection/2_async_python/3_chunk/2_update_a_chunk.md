### Update a chunk

```python
import taskingai

chunk = await taskingai.retrieval.a_update_chunk(
    collection_id="$$COLLECTION_ID$$",
    chunk_id="$$CHUNK_ID$$",
    content="Machine learning is a subfield of artificial intelligence...",
    metadata={"file_name":"machine_learning.pdf", "author": "James Brown"
)
```
