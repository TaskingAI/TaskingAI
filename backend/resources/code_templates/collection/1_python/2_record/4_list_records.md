### List records

```python
import taskingai

records = taskingai.retrieval.list_records(
    collection_id="$$COLLECTION_ID$$",
    limit=20,
    order="desc",
    after="$$RECORD_ID$$"
)
```

If `after` or `before` is not specified, the function will return the first `limit` number of records in the collection, sorted in ascending order of creation time by default.
When one of `after` or `before` is specified, the function will return the next `limit` number of records in the collection, sorted in ascending or descending order, respectively.

Note that only one of `after` or `before` can be specified at a time.
