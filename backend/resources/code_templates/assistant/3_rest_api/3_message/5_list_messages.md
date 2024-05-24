### List Messages

```bash
curl -X GET $$SERVICE_HOST$$/v1/assistants/$$ASSISTANT_ID$$/chats/$$CHAT_ID$$/messages?limit=20&order=desc \
     -H "Authorization: Bearer $$API_KEY$$" \
     -H "Content-Type: application/json"
```

Parameters and Usage:

- `limit`: Sets the maximum number of chats to return in the list. It should be in the range of 1 to 100.
- `order`: `desc` or `asc`. Determines the order in which the assistants are listed. The sort key is the `created_timestamp` field of the message.
- `before`/`after`: It specifies the point before/after which the next set of messages should be fetched.

The method will return a list of Message objects representing the messages in the chat session.
