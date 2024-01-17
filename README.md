<p align="center">
<img src="static/img/logo.svg" alt="">
</p>

---

# TaskingAI: open source platform for AI-native application development

## Introduction

TaskingAI is a managed AI Agent development platform offering a cloud service with a suite of modules like `Model`, `Retrieval`, `Assistant`, and `Tool`. It integrates these modules to provide a streamlined, intelligent, and easy experience for AI application development.

### Key Features

1. **Multiple LLM Integration:** TaskingAI integrated the majority of mainstream Large Language Models (LLMs) in the industry from various providers, and unified their interface.

   - **Note:** For integration of other models or privately developed models, contributions can be made to our
     [Inference](https://github.com/TaskingAI/TaskingAI-Inference) repository for seamless integration.

2. **Flexible combination with decoupled modules:** Tasking AI decoupled language models, retrieval systems, and tools, allowing for flexible combinations of modules to meet the needs of different scenarios.
3. **Intuitive Cloud-Based Interface:** The platform boasts a straightforward and user-friendly cloud interface. This includes easy management of Models, Assistants, Tools, and Retrieval systems, simplifying the complexity of AI development.

4. **API-Oriented Design:** TaskingAI is designed with an API-first approach, enabling quick and efficient integration of your AI Agents into existing workflows. This feature enhances adaptability and streamlines the process of embedding AI capabilities into various applications.

## What Can You Achieve with TaskingAI?

1. **Build Your Own AI Agent:** Easily construct AI agents specialized in specific domains or professions through TaskingAI.
   These agents can be seamlessly integrated into your workflows via APIs, enhancing efficiency and productivity.

2. **Enrich Your Agent with Knowledge Bases and Tools:** Utilize TaskingAI's decoupled Retrieval and Tool functionalities to expand your agent's capabilities.
   This modular approach allows for the addition of extensive knowledge sources and tools, making your AI agents more versatile and capable.
3. **Publish your AI Agent:** You can also utilze TaskingAI's SDK or REST API to embed your AI agent into your own applications.

## Why TaskingAI?

| Feature                    | LangChain         | TaskingAI                 |
| -------------------------- | ----------------- | ------------------------- |
| **Project Members**        | 1                 | **Unlimited**             |
| **Workspace Roles**        | Admin only        | **Admin & Collaborators** |
| **Ecosystem**              | Open Source       | **Open Source**           |
| **Retrieval System**       | Rely on 3rd-Party | **Decoupled**             |
| **Tool Integration**       | ✓                 | ✓                         |
| **Multiple LLM Providers** | ✓                 | ✓                         |
| **Custom Memory**          | ✓                 | ✓                         |
| **API-Oriented**           | -                 | ✓                         |
| **Multi-Tenant Project**   | -                 | ✓                         |
| **Local Deployment**       | -                 | ✓                         |

TaskingAI stands out with its open-source ecosystem, unlimited project members, and a unique combination of features
like decoupled retrieval systems, tool integration, support for multiple LLM providers, custom memory, and
API-orientation. Additionally, it offers the flexibility of multi-tenant projects and local deployment, catering to a broader range of user needs compared to LangChain.

### Resources

- [Platform](https://app.tasking.ai)
- [Documentation](https://docs.tasking.ai)
- [API Reference](https://docs.tasking.ai/api)
- [Contact Us](https://www.tasking.ai/contact-us)

## Quickstart

### Installation

Install TaskingAI using pip:

```bash
pip install taskingai
```

### Setting Up Your Credentials

Obtain your `TASKINGAI_API_KEY` from the TaskingAI console and set it as an environment variable.

### Sample Code

Here's a basic example to create a chat completion task:

```python
from taskingai.inference import chat_completion, SystemMessage, UserMessage

model_id = "YOUR_MODEL_ID"
chat_completion = chat_completion(
    model_id=model_id,
    messages=[
        SystemMessage("You are a professional nutritionist. You should always reply with a friendly tone."),
        UserMessage("How much sugar can a person consume in a day?"),
    ]
)
```

## Community and Contribution

Please see our [contribution guidelines](./CONTRIBUTING.md) for how to contribute to the project.

## License and Code of Conduct

TaskingAI is released under a specific [TaskingAI Open Source License](./LICENSE). By contributing to this project, you agree to abide by its terms.

## Support and Contact

For support, please refer to our [documentation](https://docs.tasking.ai) or contact us at [support@tasking.ai](mailto:support@tasking.ai).
