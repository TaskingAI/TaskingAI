### Update a record

```bash
curl -X POST $$SERVICE_HOST$$/v1/collections/$$COLLECTION_ID$$/record/$$RECORD_ID$$ \
     -H "Authorization: Bearer $$API_KEY$$" \
     -H "Content-Type: application/json",
     -d '{
          "type": "text",
          "title": "New Record title",
          "content": "New Record content",
          "text_splitter": {
            "chunk_size": 200,
            "overlap_size": 20,
            "type": "token"
          },
          "metadata": {}
        }'
```

To update a new record, use the `update_record` method. This method requires two primary parameters:

- `collection_id`: Required. The identifier of the collection where the record will be stored.
- `content`: Optional. The textual content of the record.
- `text_splitter`: Required if `content` is specified.
  The text splitter to use for splitting the text into smaller chunks.
- `metadata`: Optional. A dictionary containing the metadata of the record.
