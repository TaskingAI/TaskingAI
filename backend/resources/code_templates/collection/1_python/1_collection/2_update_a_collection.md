### Update a collection

```python
import taskingai
from taskingai.retrieval import Collection

collection: Collection = taskingai.retrieval.update_collection(
    collection_id="$$COLLECTION_ID$$",
    name="new name",
    description="new description",
    metadata={"key": "value"}
)
```

Only name, description, and metadata are supported for updating a collection. The metadata attribute will have no effect on information retrieval performance; it is only for storing additional information for the collection.
