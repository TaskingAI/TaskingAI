<p>
<a href="https://www.tasking.ai"><img src="../static/img/logo.png" alt="https://www.tasking.ai"></a>
</p>

# TaskingAI

<p align="center">
  <a href="https://hub.docker.com/u/taskingai"><img alt="Docker Image Version (latest semver)" src="https://img.shields.io/docker/v/taskingai/taskingai-server?label=docker"></a>
  <a href="https://github.com/TaskingAI/TaskingAI/blob/master/LICENSE"><img alt="GitHub License" src="https://img.shields.io/github/license/taskingai/taskingai"></a>
  <a href="https://pypi.org/project/taskingai"><img alt="PyPI version" src="https://img.shields.io/pypi/v/taskingai?color=blue"></a>
  <a href="https://twitter.com/TaskingAI"><img alt="X (formerly Twitter) URL" src="https://img.shields.io/twitter/url?url=https%3A%2F%2Ftwitter.com%2FTaskingAI"></a>
  <a href="https://www.youtube.com/@TaskingAI"><img alt="YouTube Channel Subscribers" src="https://img.shields.io/youtube/channel/subscribers/UCxUnOM-ZbZKmyR_Q5vAUSTA"></a>
  <a href="https://discord.gg/RqwcD3vG3k"><img alt="Discord" src="https://img.shields.io/discord/1244486619914834110"></a>
</p>

<p align="center">
  <a href="../README.md"><img alt="Readme (English)" src="https://img.shields.io/badge/English-2EA26A"></a>
  <a href="./README.de.md"><img alt="Readme (Deutsch)" src="https://img.shields.io/badge/Deutsch-2EA26A"></a>
  <a href="./README.fr.md"><img alt="Readme (Français)" src="https://img.shields.io/badge/Français-2EA26A"></a>
  <a href="./README.es.md"><img alt="Readme (Español)" src="https://img.shields.io/badge/Español-2EA26A"></a>
  <a href="./README.pt.md"><img alt="Readme (Português)" src="https://img.shields.io/badge/Português-2EA26A"></a>
  <a href="./README.zh-cn.md"><img alt="Readme (简体中文)" src="https://img.shields.io/badge/简体中文-2EA26A"></a>
  <a href="./README.zh-tw.md"><img alt="Readme (繁體中文)" src="https://img.shields.io/badge/繁體中文-2EA26A"></a>
  <a href="./README.jp.md"><img alt="Readme (日本語)" src="https://img.shields.io/badge/日本語-2EA26A"></a>
  <a href="./README.kr.md"><img alt="Readme (한국어)" src="https://img.shields.io/badge/한국어-2EA26A"></a>
</p>

[TaskingAI](https://www.tasking.ai) 是一个面向 **基于LLM的代理开发和部署** 的BaaS（后端即服务）平台。它统一了数百个LLM模型的集成，并提供直观的用户界面来管理您的LLM应用程序功能模块，包括工具、RAG系统、助手、对话历史等。

### 主要特点

1. **多合一LLM平台**：通过统一API访问数百种AI模型。
2. **丰富的增强功能**：使用数百个可自定义的内置**工具**和高级**检索增强生成**(RAG)系统增强LLM代理性能。
3. **BaaS启发的工作流**：分离AI逻辑（服务器端）和产品开发（客户端），提供清晰的路径，从基于控制台的原型设计到使用RESTful API和客户端SDK的可扩展解决方案。
4. **一键部署**：一键将您的AI代理部署到生产阶段，并轻松扩展它们。让TaskingAI处理其余工作。
5. **异步高效**：利用Python FastAPI的异步功能进行高性能并发计算，增强应用程序的响应速度和可扩展性。
6. **直观的UI控制台**：简化项目管理并允许在控制台内进行工作流测试。

<p>
<img src="static/img/console.png" alt="">
</p>

### 集成

**模型**：TaskingAI 连接了来自不同提供商的数百个LLM，包括OpenAI，Anthropic等。我们还允许用户通过Ollama，LM Studio和Local AI集成本地主机模型。

<p>
<img src="../static/img/model_providers.png" alt="">
</p>

**插件**：TaskingAI支持广泛的内置插件来增强您的AI代理，包括Google搜索、网站阅读器、股票市场检索等。用户还可以创建自定义工具以满足特定需求。

<p>
<img src="../static/img/plugins.png" alt="">
</p>

---

## 为什么选择 TaskingAI?

### 现有解决方案的问题🙁

**LangChain** 是一个用于LLM应用程序开发的工具框架，但它面临实际限制：

- **无状态性**：依赖客户端或外部服务进行数据管理。
- **可扩展性挑战**：无状态性影响跨会话的一致数据处理。
- **外部依赖性**：依赖外部资源如模型SDK和向量存储。

**OpenAI的Assistant API** 在提供类似GPT的功能方面表现出色，但也有自身限制：

- **绑定功能**：集成如工具和检索绑定位于每个助手，不适用于多租户应用程序。
- **专有限制**：限于OpenAI模型，不适合多种需求。
- **自定义限制**：用户不能自定义代理配置如内存和检索系统。

### TaskingAI 如何解决问题😃

- **支持有状态和无状态使用**：无论是跟踪和管理消息历史和代理对话会话，还是只进行无状态对话完成请求，TaskingAI都能覆盖。
- **解耦的模块化管理**：将工具、RAG系统、语言模型的管理从代理中解耦出来，允许自由组合这些模块以构建强大的AI代理。
- **多租户支持**：TaskingAI 支持开发后的快速部署，并可用于多租户场景。无需担心云服务，只需专注于AI代理开发。
- **统一API**：TaskingAI 提供所有模块的统一API，包括工具、RAG系统、语言模型等。超容易管理和更改AI代理的配置。

## 使用 TaskingAI 可以构建什么？

- [x] **互动应用演示**
- [x] **企业生产力AI 代理**
- [x] **面向商业的多租户AI本地应用**

---

如果你发现它有用，请给我们一个 **免费星标🌟** 😇

<p>
<img src="static/img/star.gif" alt="">
</p>

---

## 使用Docker快速开始

一种启动自托管TaskingAI社区版的简单方式是通过 [Docker](https://www.docker.com/)。

### 先决条件

- 在您的机器上安装Docker和Docker Compose。
- 安装Git以克隆存储库。
- Python环境（Python 3.8以上）用于运行客户端SDK。

### 安装

首先，从GitHub上克隆TaskingAI（社区版）仓库。

```bash
git clone https://github.com/taskingai/taskingai.git
cd taskingai
```

在克隆的仓库内，进入docker目录并使用Docker Compose启动服务。

```bash
cd docker
```

1. **将 `.env.example` 复制为 `.env`**：

   ```sh
   cp .env.example .env
   ```

2. **编辑 `.env` 文件**：
   在你喜欢的文本编辑器中打开 `.env` 文件，并更新必要的配置。确保所有必需的环境变量都正确设置。

3. **启动 Docker Compose**：
   执行以下命令来启动所有服务：
   ```sh
   docker-compose -p taskingai --env-file .env up -d
   ```

服务启动后，通过浏览器访问 http://localhost:8080 地址来访问 TaskingAI 控制台。默认的用户名和密码是 `admin` 和 `TaskingAI321`。

### 升级

如果您已经安装了TaskingAI的早期版本，并希望升级到最新版本，首先更新存储库。

```bash
git pull origin master
```

然后停止当前的docker服务，通过拉取最新镜像升级到最新版本，最后重新启动服务。

```bash
cd docker
docker-compose -p taskingai down
docker-compose -p taskingai pull
docker-compose -p taskingai --env-file .env up -d
```

不用担心数据丢失；如果有需要，您的数据将自动迁移到最新版本的架构。

### TaskingAI UI控制台

[![TaskingAI控制台演示](https://img.youtube.com/vi/4A5uQoawETU/maxresdefault.jpg)](https://youtu.be/4A5uQoawETU)

**_<p style="text-align: center; font-size: small; ">点击上面的图片查看TaskingAI控制台演示视频。</p>_**

### TaskingAI客户端SDK

控制台启动后，您可以使用TaskingAI客户端SDK以编程方式与TaskingAI服务器进行交互。

确保您已安装Python 3.8或更高版本，并设置虚拟环境（可选但推荐）。

使用pip安装TaskingAI Python客户端SDK。

```bash
pip install taskingai
```

这是一个客户端代码示例：

```python
import taskingai
taskingai.init(api_key='YOUR_API_KEY', host='http://localhost:8080')

# 创建一个新的助手
assistant = taskingai.assistant.create_assistant(
    model_id="YOUR_MODEL_ID",
    memory="naive",
)

# 创建一个新的聊天
chat = taskingai.assistant.create_chat(
    assistant_id=assistant.assistant_id,
)

# 发送用户消息
taskingai.assistant.create_message(
    assistant_id=assistant.assistant_id,
    chat_id=chat.chat_id,
    text="Hello!",
)

# 生成助手响应
assistant_message = taskingai.assistant.generate_message(
    assistant_id=assistant.assistant_id,
    chat_id=chat.chat_id,
)

print(assistant_message)
```

请注意，`YOUR_API_KEY` 和 `YOUR_MODEL_ID` 应替换为您在控制台中创建的实际API密钥和聊天完成模型ID。

您可以在 [文档](https://docs.tasking.ai/docs/guide/getting_started/self_hosting/overview)中了解更多。

## 资源

- [文档](https://docs.tasking.ai)
- [API参考](https://docs.tasking.ai/api)
- [联系我们](https://www.tasking.ai/contact-us)

## 社区和贡献

请参阅我们的 [贡献指南](../CONTRIBUTING.md) 了解如何为项目做出贡献。

## 许可证和行为准则

TaskingAI 在特定的 [TaskingAI开源许可证](./LICENSE)下发布。通过为该项目做出贡献，您同意遵守其条款。

## 支持和联系

有关支持, 请参阅我们的 [文档](https://docs.tasking.ai) 或通过 [support@tasking.ai](mailto:support@tasking.ai) 联系我们。
