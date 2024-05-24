### Update a record

```python
import taskingai
from taskingai.retrieval import TokenTextSplitter

record = taskingai.retrieval.update_record(
    collection_id="$$COLLECTION_ID$$",
    record_id="$$RECORD_ID$$",
    content="Machine learning is a subfield of artificial intelligence...",
    text_splitter=TokenTextSplitter(chunk_size=200, overlap_size=20),
    metadata={"file_name":"machine_learning.pdf", "author": "James Brown"}
)
```

To update a new record, use the `update_record` method. This method requires two primary parameters:

- `collection_id`: Required. The identifier of the collection where the record will be stored.
- `content`: Optional. The textual content of the record.
- `text_splitter`: Required if `content` is specified.
  The text splitter to use for splitting the text into smaller chunks.
- `metadata`: Optional. A dictionary containing the metadata of the record.
