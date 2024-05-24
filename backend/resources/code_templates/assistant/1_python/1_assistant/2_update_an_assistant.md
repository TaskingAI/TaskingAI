### Update an assistant

```python
import taskingai
from taskingai.assistant import Assistant

## All attributes apart from assistant_id are editable, please refer to the documentation for more information
assistant: Assistant = taskingai.assistant.update_assistant(
    assistant_id="$$ASSISTANT_ID$$",
    name="Updated Assistant Name",
    description="This is my new assistant",
    model_id="$$MODEL_ID$$",
)
```

Method Parameters and Usage:

- `assistant_id`: The unique identifier of the assistant you intend to update.
- `model_id` (Optional): The ID of an available chat completion model in your project.
- `name` (Optional): A new name for the assistant.
- `description` (Optional): A new description that better explains the purpose or functionalities of the assistant.
- `system_prompt_template` (Optional): A list of system prompt chunks for defining the assistant's conversational flow and context.
- `memory` (Optional): Specifies the memory configuration for the assistant.
- `tools` (Optional): A list of tools to enhance the assistant's capabilities.
- `retrievals` (Optional): A list of retrieval configurations for the assistant.
- `metadata` (Optional): Additional metadata for the assistant. This can store up to 16 key-value pairs, with each key's length being less than 64 characters and each value's length less than 512 characters.

The `update_assistant` method returns the updated Assistant object.
This object reflects the changes made to the assistant, including any new configurations or settings applied during the update process.
