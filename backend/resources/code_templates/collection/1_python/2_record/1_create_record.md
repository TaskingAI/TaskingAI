### Create a record

#### Create a record by text

```python
import taskingai
from taskingai.retrieval import Record, TokenTextSplitter

# Suppose you have a collection already created, you can get the collection_id from it.
record: Record = taskingai.retrieval.create_record(
    collection_id="$$COLLECTION_ID$$",
    type="text",
    content="Machine learning is a subfield of artificial intelligence...",
    text_splitter=TokenTextSplitter(chunk_size=200, chunk_overlap=20),
    metadata= {}
)
```

- `collection_id`: The identifier of the collection where the record will be stored.
- `content`: The textual content of the record.
- `text_splitter`: The text splitter to use for splitting the text into smaller chunks. Currently, we support `TokenTextSplitter`.
- `metadata`: A dictionary containing the metadata of the record.

The `chunk_size` and `chunk_overlap` of `TokenTextSplitter` represent the max tokens per text chunk for processing
and token overlap between chunks, with 0 indicating no overlap.

After executing this function, a new record is initiated within the specified collection.

The parameter `text_splitter` is not a property of the record so will not be included in the response.
It is only used for the creation process to split the text into smaller chunks.

#### Create a record by web URL

```python
import taskingai
from taskingai.retrieval import Record, TokenTextSplitter

# Suppose you have a collection already created, you can get the collection_id from it.
record: Record = taskingai.retrieval.create_record(
    collection_id="$$COLLECTION_ID$$",
    type="web",
    url="https://www.tasking.ai",
    text_splitter=TokenTextSplitter(chunk_size=200, chunk_overlap=20),
)
```

#### By uploading a file:

Creating a record by uploading a file is two-fold: first, upload the file, and then create the record based on the uploaded file.

To upload a file, use the `upload_file`

```python
from taskingai.file import upload_file

new_file = taskingai.file.upload_file(file=open("YOUR_FILE_PATH", "rb"), purpose="record_file")
print(f"uploaded file id: {new_file.file_id}")
```

Then, create a record based on the uploaded file:

```python
record: Record = taskingai.retrieval.create_record(
    collection_id="$$COLLECTION_ID$$",
    type="file",
    title="Machine learning",
    file_id=new_file.file_id,
    text_splitter={"type": "token", "chunk_size": 200, "chunk_overlap": 20},
)
print(f"created record: {record.record_id}")
```
