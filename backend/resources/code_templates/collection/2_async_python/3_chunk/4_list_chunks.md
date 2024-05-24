### List chunks

```python
import taskingai

records = await taskingai.retrieval.a_list_chunks(
    collection_id="$$COLLECTION_ID$$",
    limit=20,
    after="$$CHUNK_ID$$"
)
```

If `after` or `before` is not specified, the function will return the first `limit` number of records in the collection, sorted in ascending order of creation time by default.
When one of `after` or `before` is specified, the function will return the next `limit` number of records in the collection, sorted in ascending or descending order, respectively.

Note that only one of `after` or `before` can be specified at a time.
