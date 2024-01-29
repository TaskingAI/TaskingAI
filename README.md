<p>
<img src="static/img/logo.png" alt="https://www.tasking.ai">
</p>

# TaskingAI

[TaskingAI](https://www.tasking.ai) brings Firebase's simplicity to **AI-native app development**. The platform enables the creation of GPTs-like multi-tenant applications using a wide range of LLMs from various providers. It features distinct, modular functions such as Inference, Retrieval, Assistant, and Tool, seamlessly integrated to enhance the development process. TaskingAI’s cohesive design ensures an efficient, intelligent, and user-friendly experience in AI application development.

**Key Features**:

1. **All-In-One LLM Platform**: Access hundreds of AI models with unified APIs.
2. **Intuitive UI Console**: Simplifies project management and allows in-console workflow testing.
3. **BaaS-Inspired Workflow**: Separate AI logic (server-side) from product development (client-side), offering a clear pathway from console-based prototyping to scalable solutions using RESTful APIs and client SDKs.
4. **Customizable Integration**: Enhance LLM functionalities with customizable **tools** and advanced **Retrieval-Augmented Generation** (RAG) system
5. **Asynchronous Efficiency**: Harness Python FastAPI's asynchronous features for high-performance, concurrent computation, enhancing the responsiveness and scalability of the applications.

<p>
<img src="static/img/console.png" alt="">
</p>

Please give us a **FREE STAR🌟** on GitHub if you find it useful.

<p>
<img src="static/img/star.gif" alt="">
</p>

## What Can You Build with TaskingAI?

- [x] **Interactive Application Demos**: Quickly create and deploy engaging application demos using TaskingAI's UI Console. It’s an ideal environment for demonstrating the potential of AI-native apps with real-time interaction and user engagement.

- [x] **AI Agents for Team Collaboration**: Develop AI agents that harness collective knowledge and tools, enhancing teamwork and efficiency. TaskingAI facilitates the creation of shared AI resources that streamline collaboration and support within your organization.

- [x] **Multi-Tenant AI-Native Applications for Business**: With TaskingAI, build robust, multi-tenant AI-native applications that are ready for production. It's perfectly suited for handling varied client needs while maintaining individual customization, security, and scalability.

## Why TaskingAI?

### Problems with existing products

The Assistant API from OpenAI, while robust for GPTs-like functionalities, has limitations due to its design where key functions like tools and documentation retrieval are tied to individual assistants. This structure can restrict flexibility in multi-tenant applications, where shared data is essential.

### How TaskingAI solves the problem

TaskingAI overcomes these obstacles by decoupling key modules, offering broader model support and an open-source framework. Its adaptability makes it a superior choice for developers needing more versatile, data-sharing capable AI solutions, particularly for complex, customizable projects.

### Comparisons

Here is a comparison table among the mainstream agent development frameworks and TaskingAI:

| Feature                  | LangChain               | TaskingAI               |
|--------------------------|-------------------------|-------------------------|
| **LLM Providers**        | Multiple providers      | **Multiple providers**  |
| **Retrieval System**     | Requires 3rd-party      | **Decoupled; flexible** |
| **Tool Integration**     | Requires 3rd-party      | **Decoupled; flexible** |
| **Agent Memory**         | Configurable            | **Customizable**        |
| **Development Method**   | Python-based SDK        | **RESTful APIs & SDKs** |
| **Async Support**        | Selective model support | **Comprehensive**       |
| **Multi-Tenant Support** | Complex setup           | **Simplified setup**    |

## Architecture

TaskingAI's architecture is designed with modularity and flexibility at its core, enabling compatibility with a wide spectrum of LLMs. This adaptability allows it to effortlessly support a variety of applications, from straightforward demos to sophisticated, multi-tenant AI systems. Constructed on a foundation of open-source principles, TaskingAI incorporates numerous open-source tools, ensuring that the platform is not only versatile but also customizable.

<p>
<img src="static/img/architecture.png" alt="">
</p>

**[Nginx](https://www.nginx.com/)**: Functions as the frontend web server, efficiently routing traffic to the designated services within the architecture.

**Frontend ([TypeScript](https://www.typescriptlang.org/) + [React](https://react.dev/))**: This interactive and responsive user interface is built with TypeScript and React, allowing users to smoothly interact with backend APIs.

**Backend ([Python](https://www.python.org/) + [FastAPI](https://fastapi.tiangolo.com/))**: The backend, engineered with Python and FastAPI, offers high performance stemming from its asynchronous design. It manages business logic, data processing, and serves as the conduit between the frontend and AI inference services. Python's widespread use invites broader contributions, fostering a collaborative environment for continuous improvement and innovation.

**[TaskingAI-Inference](https://github.com/taskingai/taskingai-inference)**: Dedicated to AI model inference, this component adeptly handles tasks such as response generation and natural language input processing. It's another standout project within TaskingAI's suite of open-source offerings.

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

### TaskingAI UI Console

[![TaskingAI Console Demo](https://img.youtube.com/vi/4A5uQoawETU/maxresdefault.jpg)](https://youtu.be/4A5uQoawETU)
***<p style="text-align: center; font-size: small; ">Click the image above for TaskingAI Console Demo Video</p>***



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
