### List Assistants

```bash
curl -X GET $$SERVICE_HOST$$/v1/assistants?limit=20&order=desc \
     -H "Authorization: Bearer $$API_KEY$$" \
     -H "Content-Type: application/json"
```

Parameters and Usage:

- `limit`: Sets the maximum number of assistants to return in the list. This parameter helps in controlling the size of the output, especially in cases where there are numerous assistants.
- `order`: Determines the order in which the assistants are listed. It can be either ascending ("asc") or descending ("desc").
- `before`/`after`: A cursor used for pagination. It specifies the point before/after which the next set of assistants should be fetched. This is useful for navigating through the list of assistants in manageable chunks.

The list_assistants method returns a list of Assistant objects, each representing an assistant in your project.
This list provides a snapshot of all the assistants, along with their respective details and configurations.
