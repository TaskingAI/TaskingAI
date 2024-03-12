<p>
<img src="static/img/logo.png" alt="https://www.tasking.ai">
</p>

# TaskingAI

[![Docs](https://img.shields.io/badge/docs-latest-brightgreen)](https://docs.tasking.ai/docs/guide/getting_started/overview/)
[![Docker Image Version (latest semver)](https://img.shields.io/docker/v/taskingai/taskingai-server?label=docker)](https://hub.docker.com/u/taskingai)
[![GitHub License](https://img.shields.io/github/license/taskingai/taskingai)](https://github.com/TaskingAI/TaskingAI/blob/master/LICENSE)
[![PyPI version](https://img.shields.io/pypi/v/taskingai?color=blue)](https://pypi.org/project/taskingai)
[![X (formerly Twitter) URL](https://img.shields.io/twitter/url?url=https%3A%2F%2Ftwitter.com%2FTaskingAI)](https://twitter.com/TaskingAI)
[![YouTube Channel Subscribers](https://img.shields.io/youtube/channel/subscribers/UCxUnOM-ZbZKmyR_Q5vAUSTA)](https://www.youtube.com/@TaskingAI)

[TaskingAI](https://www.tasking.ai) brings Firebase's simplicity to **AI-native app development**. The platform enables the creation of GPTs-like multi-tenant applications using a wide range of LLMs from various providers. It features distinct, modular functions such as Inference, Retrieval, Assistant, and Tool, seamlessly integrated to enhance the development process. TaskingAI’s cohesive design ensures an efficient, intelligent, and user-friendly experience in AI application development.

### Key Features

1. **All-In-One LLM Platform**: Access hundreds of AI models with unified APIs.
2. **Intuitive UI Console**: Simplifies project management and allows in-console workflow testing.
3. **BaaS-Inspired Workflow**: Separate AI logic (server-side) from product development (client-side), offering a clear pathway from console-based prototyping to scalable solutions using RESTful APIs and client SDKs.
4. **Customizable Integration**: Enhance LLM functionalities with customizable **tools** and advanced **Retrieval-Augmented Generation** (RAG) system
5. **Asynchronous Efficiency**: Harness Python FastAPI's asynchronous features for high-performance, concurrent computation, enhancing the responsiveness and scalability of the applications.

<p>
<img src="static/img/console.png" alt="">
</p>

### Integrations

**Models**: TaskingAI connects with hundreds of LLMs from various providers, including OpenAI, Anthropic, and more. We also allow users to integrate local host models through Ollama, LM Studio and Local AI.

<p>
<img src="static/img/model_providers.png" alt="">
</p>

**Plugins**: TaskingAI supports a wide range of built-in plugins to empower your AI agents, including Google search, website reader, stoke market retrieval, and more. Users can also create custom tools to meet their specific needs.

<p>
<img src="static/img/plugins.png" alt="">
</p>

## What Can You Build with TaskingAI?

- [x] **Interactive Application Demos**: Quickly create and deploy engaging application demos using TaskingAI's UI Console. It’s an ideal environment for demonstrating the potential of AI-native apps with real-time interaction and user engagement.

- [x] **AI Agents for Enterprise Productivity**: Create AI agents that utilize collective knowledge and tools to boost teamwork and productivity. TaskingAI streamlines the development of these shared AI resources, making it easier to foster collaboration and support across your organization. Leverage our Client SDKs and REST APIs for seamless integration and customization.

- [x] **Multi-Tenant AI-Native Applications for Business**: With TaskingAI, build robust, multi-tenant AI-native applications that are ready for production. It's perfectly suited for handling varied client needs while maintaining individual customization, security, and scalability. For serverless deployment, Please check out our [official website](https://www.tasking.ai) to learn more.

```python
# Easily build an agent with TaskingAI Client SDK
assistant = taskingai.assistant.create_assistant(
    model_id="YOUR_TASKINGAI_MODEL_ID",
    memory=AssistantNaiveMemory(),
    tools=[
        AssistantTool(
            type=AssistantToolType.ACTION,
            id=action_id,
        )
    ],
    retrievals=[
        AssistantRetrieval(
            type=AssistantRetrievalType.COLLECTION,
            id=collection_id,
        )
    ],
)
```

---

Please give us a **FREE STAR 🌟** if you find it helpful 😇

<p>
<img src="static/img/star.gif" alt="">
</p>

---

## Why TaskingAI?

### Problems with existing solutions 🙁

**LangChain** is a tool framework for LLM application development, but it faces practical limitations:

- **Statelessness**: Relies on client-side or external services for data management.
- **Scalability Challenges**: Statelessness impacts consistent data handling across sessions.
- **External Dependencies**: Depends on outside resources like model SDKs and vector storage.

**OpenAI's Assistant API** excels in delivering GPTs-like functionalities but comes with its own constraints:

- **Tied Functionalities**: Integrations like tools and retrievals are tied to each assistant, not suitable for multi-tenant applications.
- **Proprietary Limitations**: Restricted to OpenAI models, unsuitable for diverse needs.
- **Customization Limits**: Users cannot customize agent configuration such as memory and retrieval system.

### How TaskingAI solves the problem 😃

TaskingAI addresses these challenges with a **decoupled modular design** and **extensive model compatibility**, adhering to **open-source principles**.

Perfect for developers who need a scalable and customizable AI development environment, TaskingAI enhances project management with a **user-friendly UI console**. It supports development through **Client SDKs and REST APIs**, and its server efficiently stores data for various models. Importantly, TaskingAI natively supports **vector storage**, essential for the Retrieval-Augmented Generation (RAG) system, thereby facilitating a seamless progression from prototype to production.

## Architecture

TaskingAI's architecture is designed with modularity and flexibility at its core, enabling compatibility with a wide spectrum of LLMs. This adaptability allows it to effortlessly support a variety of applications, from straightforward demos to sophisticated, multi-tenant AI systems. Constructed on a foundation of open-source principles, TaskingAI incorporates numerous open-source tools, ensuring that the platform is not only versatile but also customizable.

<p>
<img src="static/img/architecture.png" alt="">
</p>

**[Nginx](https://www.nginx.com/)**: Functions as the frontend web server, efficiently routing traffic to the designated services within the architecture.

**Frontend ([TypeScript](https://www.typescriptlang.org/) + [React](https://react.dev/))**: This interactive and responsive user interface is built with TypeScript and React, allowing users to smoothly interact with backend APIs.

**Backend ([Python](https://www.python.org/) + [FastAPI](https://fastapi.tiangolo.com/))**: The backend, engineered with Python and FastAPI, offers high performance stemming from its asynchronous design. It manages business logic, data processing, and serves as the conduit between the frontend and AI inference services. Python's widespread use invites broader contributions, fostering a collaborative environment for continuous improvement and innovation.

**TaskingAI-Inference**: Dedicated to AI model inference, this component adeptly handles tasks such as response generation and natural language input processing. It's another standout project within TaskingAI's suite of open-source offerings.

**TaskingAI Core Services**: Comprises various services including Model, Assistant, Retrieval, and Tool, each integral to the platform's operation.

**[PostgreSQL](https://www.postgresql.org/) + [PGVector](https://github.com/pgvector/pgvector)**: Serves as the primary database, with PGVector enhancing vector operations for embedding comparisons, crucial for AI functionalities.

**[Redis](https://www.redis.com/)**: Delivers high-performance data caching, crucial for expediting response times and bolstering data retrieval efficiency.

## Quickstart with Docker

A simple way to initiate self-hosted TaskingAI community edition is through [Docker](https://www.docker.com/).

### Prerequisites

- Docker and Docker Compose installed on your machine.
- Git installed for cloning the repository.
- Python environment (above Python 3.8) for running the client SDK.

### Installation

First, clone the TaskingAI (community edition) repository from GitHub.

```bash
git clone https://github.com/taskingai/taskingai.git
cd taskingai
```

Inside the cloned repository, go to the docker directory and launch the services using Docker Compose.

```bash
cd docker
docker-compose -p taskingai up -d
```

Once the service is up, access the TaskingAI console through your browser with the URL http://localhost:8080.
The default username and password are `admin` and `TaskingAI321`.

### Upgrade

If you have already installed TaskingAI with a previous version and want to upgrade to the latest version, first update the repository.

```bash
git pull origin master
```

Then stop current docker service, upgrade to the latest version by pulling the latest image, and finally restart the service.

```bash
cd docker
docker-compose -p taskingai down
docker-compose -p taskingai pull
docker-compose -p taskingai up -d
```

Don't worry about data loss; your data will be automatically migrated to the latest version schema if needed.

### TaskingAI UI Console

[![TaskingAI Console Demo](https://img.youtube.com/vi/4A5uQoawETU/maxresdefault.jpg)](https://youtu.be/4A5uQoawETU)
**_<p style="text-align: center; font-size: small; ">Click the image above to view the TaskingAI Console Demo Video.</p>_**

### TaskingAI Client SDK

Once the console is up, you can programmatically interact with the TaskingAI server using the TaskingAI client SDK.

Ensure you have Python 3.8 or above installed, and set up a virtual environment (optional but recommended).
Install the TaskingAI Python client SDK using pip.

```bash
pip install taskingai
```

Here is a client code example:

```python
import taskingai
from taskingai.assistant.memory import AssistantNaiveMemory

taskingai.init(api_key='YOUR_API_KEY', host='http://localhost:8080')

# Create a new assistant
assistant = taskingai.assistant.create_assistant(
    model_id="YOUR_MODEL_ID",
    memory=AssistantNaiveMemory(),
)

# Create a new chat
chat = taskingai.assistant.create_chat(
    assistant_id=assistant.assistant_id,
)

# Send a user message
taskingai.assistant.create_message(
    assistant_id=assistant.assistant_id,
    chat_id=chat.chat_id,
    text="Hello!",
)

# generate assistant response
assistant_message = taskingai.assistant.generate_message(
    assistant_id=assistant.assistant_id,
    chat_id=chat.chat_id,
)

print(assistant_message)
```

Note that the `YOUR_API_KEY` and `YOUR_MODEL_ID` should be replaced with the actual API key and chat completion model ID you created in the console.

You can learn more in the [documentation](https://docs.tasking.ai/docs/guide/getting_started/self_hosting/overview).

## Resources

- [Documentation](https://docs.tasking.ai)
- [API Reference](https://docs.tasking.ai/api)
- [Contact Us](https://www.tasking.ai/contact-us)

## Community and Contribution

Please see our [contribution guidelines](./CONTRIBUTING.md) for how to contribute to the project.

## License and Code of Conduct

TaskingAI is released under a specific [TaskingAI Open Source License](./LICENSE). By contributing to this project, you agree to abide by its terms.

## Support and Contact

For support, please refer to our [documentation](https://docs.tasking.ai) or contact us at [support@tasking.ai](mailto:support@tasking.ai).
