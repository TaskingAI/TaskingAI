### Create an Assistant

```python
import taskingai
from taskingai.assistant import Assistant
from taskingai.assistant.memory import AssistantNaiveMemory

assistant: Assistant = await taskingai.assistant.a_create_assistant(
    model_id="$$MODEL_ID$$",
    name="My Assistant",
    description="This is my assistant",
    system_prompt_template=["You are a professional assistant speaking {{language}}."],
    memory=AssistantNaiveMemory(),
    tools=[],
    retrievals=[],
)
```

Here are the parameters for the `create_assistant` method:

- `model_id`: The ID of a chat completion model available in your project.
- `memory`: Specifies the memory configuration for the assistant. [Learn more about memory](/docs/guide/assistant/components/1-memory.md).
- `name` (Optional): The name for the assistant.
- `description` (Optional): A brief description of the assistant.
- `system_prompt_template` (Optional): A list of system prompt chunks for defining the assistant's conversational flow and context. Prompt variables are wrapped in curly brackets. [Learn more about system_prompt_template](/docs/guide/assistant/components/2-system-prompt-template.md).
- `tools` (Optional): A list of tools to enhance the assistant's capabilities. [Learn more about tool integrations](/docs/guide/assistant/components/4-tools.md).
- `retrievals` (Optional): A list of retrieval configurations for the assistant. [Learn more about retrieval integrations](/docs/guide/assistant/components/3-retrievals.md).
- `metadata` (Optional): Additional metadata for the assistant. Can store up to 16 key-value pairs.

The `create_assistant` method returns a new Assistant object.
This object contains various properties and configurations of the newly created assistant, reflecting the settings and options specified during creation.
