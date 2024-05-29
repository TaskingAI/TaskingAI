### Chat completion

#### Single round chat completion

```python
import taskingai
from taskingai.inference import SystemMessage, UserMessage

# choose an available chat_completion model from your project
model_id = "$$MODEL_ID$$"

# create a chat_completion task
chat_completion_result = await taskingai.inference.a_chat_completion(
    model_id=model_id,
    messages=[
        SystemMessage("You are a health advisor providing nutritional advice. You should always reply with a professional, kind, and patient tone."),
        UserMessage("How much sugar can a woman take in a day?"),
    ]
)
```

#### Multi-round chat completion

```python
from taskingai.inference import AssistantMessage

# multi round chat completion
chat_completion_result = await taskingai.inference.a_chat_completion(
    model_id="$$MODEL_ID$$",
    messages=[
        SystemMessage("You are a health advisor providing nutritional advice. You should always reply with a professional, kind, and patient tone."),
        UserMessage("How much sugar can a woman take in a day?"),
        AssistantMessage("The AHA suggests a added-sugar limit of no more than 100 calories per day (about 6 teaspoons or 24 grams) for woman."),
        # Here in this example the UserMessage and AssistantMessage are manually created by calling builder functions
        # In real scenarios, those messages should be the ones retrieved by taskingai.assistant.list_messages
        UserMessage("What about man?")
    ]
)
```

For more information about chat completion including stream mode and function calls, please refer to the [documentation](https://docs.tasking.ai/docs/guide/model/manage_models/chat-completion/).
