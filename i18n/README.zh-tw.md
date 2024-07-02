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

[TaskingAI](https://www.tasking.ai) 是一個面向 **基於LLM的代理開發和部署** 的BaaS（後端即服務）平台。它統一了數百個LLM模型的整合，並提供直觀的用戶界面來管理您的LLM應用程序功能模塊，包括工具、RAG系統、助手、對話歷史等。

### 主要特點

1. **多合一LLM平台**：通過統一API訪問數百種AI模型。
2. **豐富的增強功能**：使用數百個可自訂的內建**工具**和高級**檢索增強生成**(RAG)系統增強LLM代理性能。
3. **BaaS啟發的工作流**：分離AI邏輯（服務器端）和產品開發（客戶端），提供清晰的路徑，從基於控制台的原型設計到使用RESTful API和客戶端SDK的可擴展解決方案。
4. **一鍵部署**：一鍵將您的AI代理部署到生產階段，並輕鬆擴展它們。讓TaskingAI處理其餘工作。
5. **異步高效**：利用Python FastAPI的異步功能進行高性能並發計算，增強應用程序的響應速度和可擴展性。
6. **直觀的UI控制台**：簡化項目管理並允許在控制台內進行工作流測試。

<p>
<img src="static/img/console.png" alt="">
</p>

### 集成

**模型**：TaskingAI 連接了來自不同提供商的數百個LLM，包括OpenAI，Anthropic等。我們還允許用戶通過Ollama，LM Studio和Local AI集成本地主機模型。

<p>
<img src="../static/img/model_providers.png" alt="">
</p>

**插件**：TaskingAI支持廣泛的內建插件來增強您的AI代理，包括Google搜索、網站閱讀器、股票市場檢索等。用戶還可以創建自訂工具以滿足特定需求。

<p>
<img src="../static/img/plugins.png" alt="">
</p>

---

## 為什麼選擇 TaskingAI?

### 現有解決方案的問題🙁

**LangChain** 是一個用於LLM應用程序開發的工具框架，但它面臨實際限制：

- **無狀態性**：依賴客戶端或外部服務進行數據管理。
- **可擴展性挑戰**：無狀態性影響跨會話的一致數據處理。
- **外部依賴性**：依賴外部資源如模型SDK和向量存儲。

**OpenAI的Assistant API** 在提供類似GPT的功能方面表現出色，但也有自身限制：

- **綁定功能**：集成如工具和檢索位於每個助手，不適用於多租戶應用程序。
- **專有限制**：限於OpenAI模型，不適合多種需求。
- **自訂限制**：用戶不能自訂代理配置如內存和檢索系統。

### TaskingAI 如何解決問題😃

- **支持有狀態和無狀態使用**：無論是跟蹤和管理消息歷史和代理對話會話，還是只進行無狀態對話完成請求，TaskingAI都能涵蓋。
- **解耦的模組化管理**：將工具、RAG系統、語言模型的管理從代理中解耦出來，允許自由組合這些模塊以構建強大的AI代理。
- **多租戶支持**：TaskingAI 支持開發後的快速部署，並可用於多租戶場景。無需擔心雲服務，只需專注於AI代理開發。
- **統一API**：TaskingAI 提供所有模塊的統一API，包括工具、RAG系統、語言模型等。超容易管理和更改AI代理的配置。

## 使用 TaskingAI 可以構建什麼？

- [x] **互動應用示範**
- [x] **企業生產力AI代理**
- [x] **面向商業的多租戶AI本地應用**

---

如果你發現它有用，請給我們一個 **免費星標🌟** 😇

<p>
<img src="static/img/star.gif" alt="">
</p>

---

## 使用Docker快速開始

一種啟動自託管TaskingAI社區版的簡單方式是通過 [Docker](https://www.docker.com/)。

### 先決條件

- 在您的機器上安裝Docker和Docker Compose。
- 安裝Git以克隆存儲庫。
- Python環境（Python 3.8以上）用於運行客戶端SDK。

### 安裝

首先，從GitHub上克隆TaskingAI（社區版）倉庫。

```bash
git clone https://github.com/taskingai/taskingai.git
cd taskingai
```

在克隆的倉庫內，進入docker目錄並使用Docker Compose啟動服務。

```bash
cd docker
```

1. **將 `.env.example` 複製為 `.env`**：

   ```sh
   cp .env.example .env
   ```

2. **編輯 `.env` 文件**：
   使用您偏好的文字編輯器開啟 `.env` 文件，並更新必要的配置。確保所有必要的環境變數都設定正確。

3. **啟動 Docker Compose**：
   執行以下命令以啟動所有服務：
   ```sh
   docker-compose -p taskingai --env-file .env up -d
   ```

服務啟動後，通遀瀏覽器訪問 http://localhost:8080 進入 TaskingAI 控制台。預設的使用者名稱和密碼是 `admin` 和 `TaskingAI321`。

### 升級

如果您已經安裝了TaskingAI的早期版本，並希望升級到最新版本，首先更新存儲庫。

```bash
git pull origin master
```

然後停止當前的docker服務，通過拉取最新映像升級到最新版本，最後重新啟動服務。

```bash
cd docker
docker-compose -p taskingai down
docker-compose -p taskingai pull
docker-compose -p taskingai --env-file .env up -d
```

不用擔心數據丟失；如果有需要，您的數據將自動遷移到最新版本的架構。

### TaskingAI UI控制台

[![TaskingAI控制台演示](https://img.youtube.com/vi/4A5uQoawETU/maxresdefault.jpg)](https://youtu.be/4A5uQoawETU)

**_<p style="text-align: center; font-size: small; ">點擊上面的圖片查看TaskingAI控制台演示視頻。</p>_**

### TaskingAI客戶端SDK

控制台運行後，您可以使用TaskingAI客戶端SDK以程式方式與TaskingAI伺服器進行互動。

確保您已安裝Python 3.8或更高版本，並設置虛擬環境（可選但推薦）。

使用pip安裝TaskingAI Python客戶端SDK。

```bash
pip install taskingai
```

這是一個客戶端代碼示例：

```python
import taskingai
taskingai.init(api_key='YOUR_API_KEY', host='http://localhost:8080')

# 創建一個新的助手
assistant = taskingai.assistant.create_assistant(
    model_id="YOUR_MODEL_ID",
    memory="naive",
)

# 創建一個新的聊天
chat = taskingai.assistant.create_chat(
    assistant_id=assistant.assistant_id,
)

# 發送用戶消息
taskingai.assistant.create_message(
    assistant_id=assistant.assistant_id,
    chat_id=chat.chat_id,
    text="Hello!",
)

# 生成助手響應
assistant_message = taskingai.assistant.generate_message(
    assistant_id=assistant.assistant_id,
    chat_id=chat.chat_id,
)

print(assistant_message)
```

請注意，`YOUR_API_KEY` 和 `YOUR_MODEL_ID` 應替換為您在控制台中創建的實際API密鑰和聊天完成模型ID。

您可以在 [文檔](https://docs.tasking.ai/docs/guide/getting_started/self_hosting/overview)中了解更多。

## 資源

- [文檔](https://docs.tasking.ai)
- [API參考](https://docs.tasking.ai/api)
- [聯繫我們](https://www.tasking.ai/contact-us)

## 社區和貢獻

請查閱我們的[貢獔指南](../CONTRIBUTING.md)，了解如何對項目作出貢獻。

此外，我們很高興地宣布 TaskingAI 現已有官方 Discord 社群！🎊

[加入我們的 Discord 伺服器](https://discord.gg/RqwcD3vG3k)來：

    • 💬 參與有關 TaskingAI 的討論，分享想法，提供反饋。
    • 📚 從其他用戶和我們的團隊獲得支持、提示和最佳實踐。
    • 🚀 保持最新的消息、更新和功能發布。
    • 🤝 與對人工智能和任務自動化充滿熱情的同好建立聯繫。

## 許可證和行為準則

TaskingAI 在特定的 [TaskingAI開源許可證](./LICENSE)下發佈。通過為該項目做出貢獻，您同意遵守其條款。

## 支援和聯繫

有關支持, 請參閱我們的 [文档](https://docs.tasking.ai) 或通過 [support@tasking.ai](mailto:support@tasking.ai) 聯繫我們。
