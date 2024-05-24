### List collections

```bash
curl -X GET $$SERVICE_HOST$$/v1/collections?limit=20&order=desc \
     -H "Authorization: Bearer $$API_KEY$$" \
     -H "Content-Type: application/json"
```

Here are the required parameters for the pagination features:

- Order: Specify the order of the returned list as ascending (asc) or descending (desc), sorting on the `created_timestamp` field. It is set to `desc` by default.
- Limit: Set a maximum number of entries to return in a single request. The default value is 20.
- After/Before: Use cursors for pagination, retrieving collections in pages either after or before the specified cursor. Note that you cannot use both after and before simultaneously.
