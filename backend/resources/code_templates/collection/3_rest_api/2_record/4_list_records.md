### List records

```bash
curl -X GET $$SERVICE_HOST$$/v1/collections/$$COLLECTION_ID$$/records?limit=20&order=desc \
     -H "Authorization: Bearer $$API_KEY$$" \
     -H "Content-Type: application/json"
```

If `after` or `before` is not specified, the function will return the first `limit` number of records in the collection, sorted in ascending order of creation time by default.
When one of `after` or `before` is specified, the function will return the next `limit` number of records in the collection, sorted in ascending or descending order, respectively.

Note that only one of `after` or `before` can be specified at a time.
