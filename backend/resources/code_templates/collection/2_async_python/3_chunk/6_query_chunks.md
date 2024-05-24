### Query chunks

```python
import taskingai

chunks = await taskingai.retrieval.a_query_chunks(
    collection_id="$$COLLECTION_ID$$",
    query_text="Basketball",
    top_k=2
)
```
