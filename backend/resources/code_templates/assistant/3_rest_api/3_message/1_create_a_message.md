### Create a message

```bash
curl -X POST $$SERVICE_HOST$$/v1/assistants/$$ASSISTANT_ID$$/chats/$$CHAT_ID$$/messages \
     -H "Authorization: Bearer $$API_KEY$$" \
     -H "Content-Type: application/json" \
     -d '{
          "role": "user",
          "content": {
            "text": "Hello!"
          },
          "metadata": {}
        }'
```

The method accepts the `assistant_id` of the assistant you want to use, the `chat_id` of the chat session you want to send the message to, and the `text` of the message you want to send.

It returns a Message object representing the user's message created in the chat session.

### Best Practices for Message Creation:

- **Sequential Conversation Flow**: While TaskingAI allows users to create multiple user messages in succession before generating an assistant message, it is not recommended. For optimal results, it is advisable to follow a back-and-forth pattern – creating a user message and then immediately generating an assistant message. This approach aligns with the training of most chat completion models, which are typically trained on a conversational format involving alternating messages between the user and the assistant.

- **Immediate Response Generation**: Generating an assistant message right after a user message can lead to more coherent and contextually relevant responses. This mimics natural conversation flows and leverages the AI model's capacity to provide immediate and pertinent replies.
