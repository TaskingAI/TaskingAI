### Create a record

#### Create a record by text

```bash
curl -X POST $$SERVICE_HOST$$/v1/collections/$$COLLECTION_ID$$/records \
     -H "Authorization: Bearer $$API_KEY$$" \
     -H "Content-Type: application/json" \
     -d '{
          "type": "text",
          "title": "Record title",
          "content": "Record content",
          "text_splitter": {
            "chunk_size": 200,
            "overlap_size": 20,
            "type": "token"
          },
          "metadata": {}
        }'
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

```bash
curl -X POST $$SERVICE_HOST$$/v1/collections/$$COLLECTION_ID$$/records \
     -H "Authorization: Bearer $$API_KEY$$" \
     -H "Content-Type: application/json" \
     -d '{
          "type": "web",
          "title": "Record title",
          "url": "https://www.tasking.ai",
          "text_splitter": {
            "chunk_size": 200,
            "overlap_size": 20,
            "type": "token"
          },
          "metadata": {}
        }'
```

#### By uploading a file:

Creating a record by uploading a file is two-fold: first, upload the file, and then create the record based on the uploaded file.

To upload a file, use the `upload_file`

```bash
curl -X POST $$SERVICE_HOST$$/v1/files \
     -H "Authorization: Bearer $$API_KEY$$" \
     -H "Content-Type: application/json" \
     -F "file=@example.txt" \
     -F "purpose=record_file"
```

Then, create a record based on the uploaded file:

```bash
curl -X POST $$SERVICE_HOST$$/v1/collections/$$COLLECTION_ID$$/records \
     -H "Authorization: Bearer $$API_KEY$$" \
     -H "Content-Type: application/json" \
     -d '{
          "type": "file",
          "title": "Record title",
          "file_id": "THE_UPLOADED_FILE_ID",
          "text_splitter": {
            "chunk_size": 200,
            "overlap_size": 20,
            "type": "token"
          },
          "metadata": {}
        }'
```
