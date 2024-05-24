### Create a collection

```python
import taskingai

collection = await taskingai.retrieval.a_create_collection(
    embedding_model_id="$$MODEL_ID$$",
    capacity=1000,
    name="machine learning",
    description="The evolving history and application of machine learning"
)
```

Please properly set collection name and description with meaningful texts. This may affect the performance of your retrieval system.
