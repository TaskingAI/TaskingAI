### Create a chunk

```python
import taskingai
from taskingai.retrieval import Chunk

chunk: Chunk = await taskingai.retrieval.a_create_chunk(
    collection_id="$$COLLECTION_ID$$",
    content="The dog is a domesticated descendant of the wolf. Also called the domestic dog, it is derived from extinct gray wolves, and the gray wolf is the dog's closest living relative. The dog was the first species to be domesticated by humans.",
)

print(f"created chunk: {chunk.chunk_id}")
```
