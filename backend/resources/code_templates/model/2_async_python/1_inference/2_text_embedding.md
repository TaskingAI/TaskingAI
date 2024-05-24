### Text Embedding

#### Single usage

```python
import taskingai

embedding_result = await taskingai.inference.a_text_embedding(
    model_id="$$MODEL_ID$$",
    input="Machine learning is a subfield of artificial intelligence (AI) that involves the development of algorithms that allow computers to learn from and make decisions or predictions based on data."
)
```

#### Batch usage

```python
embedding_list = await taskingai.inference.a_text_embedding(
    model_id="$$MODEL_ID$$",
    input=[
        "Machine learning is a subfield of artificial intelligence (AI) that involves the development of algorithms that allow computers to learn from and make decisions or predictions based on data.",
        "Michael Jordan, often referred to by his initials MJ, is considered one of the greatest players in the history of the National Basketball Association (NBA)."
    ]
)
```
