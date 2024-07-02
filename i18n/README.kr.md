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

[TaskingAI](https://www.tasking.ai) 는 **LLM 기반 에이전트 개발 및 배포**를 위한 BaaS(Backend as a Service) 플랫폼입니다. 수백 개의 LLM 모델 통합을 통일하고, 툴, RAG 시스템, 어시스턴트, 대화 히스토리 등 LLM 애플리케이션의 기능 모듈을 관리할 수 있는 직관적인 사용자 인터페이스를 제공합니다.

### 주요 기능

1. **올인원 LLM 플랫폼**: 통합 API를 통해 수백 개의 AI 모델에 접근할 수 있습니다.
2. **풍부한 확장 기능**: 수백 개의 맞춤형 내장 **툴**과 고급 **검색 강화 생성**(RAG) 시스템을 사용하여 LLM 에이전트 성능을 향상시킵니다.
3. **BaaS 기반 워크플로**: AI 로직(서버 측)과 제품 개발(클라이언트 측)을 분리하여, 콘솔 기반 프로토타이핑에서 RESTful API 및 클라이언트 SDK를 사용하는 확장 가능한 솔루션까지 명확한 경로를 제공합니다.
4. **원클릭 프로덕션 배포**: AI 에이전트를 원클릭으로 프로덕션 단계에 배포하고, 쉽게 확장할 수 있습니다. 나머지는 TaskingAI가 처리합니다.
5. **비동기 효율성**: Python FastAPI의 비동기 기능을 활용하여 고성능, 동시 계산을 수행하며 애플리케이션의 응답성과 확장성을 향상시킵니다.
6. **직관적인 UI 콘솔**: 프로젝트 관리가 간소화되고 콘솔 내에서 워크플로 테스트를 수행할 수 있습니다.

<p>
<img src="static/img/console.png" alt="">
</p>

### 통합

**모델**: TaskingAI는 OpenAI, Anthropic 등 다양한 제공업체의 수백 개의 LLM과 연결됩니다. 또한 Ollama, LM Studio, Local AI를 통해 로컬 호스트 모델을 통합할 수 있습니다.

<p>
<img src="../static/img/model_providers.png" alt="">
</p>

**플러그인**: TaskingAI는 Google 검색, 웹사이트 리더, 주식 시장 검색 등 다양한 내장 플러그인을 지원하여 AI 에이전트를 강화합니다. 사용자 맞춤형 툴도 제작하여 특정 요구 사항을 충족할 수 있습니다.

<p>
<img src="../static/img/plugins.png" alt="">
</p>

---

## 왜 TaskingAI를 선택해야 하나요?

### 기존 솔루션의 문제점 🙁

**LangChain** 은 LLM 애플리케이션 개발을 위한 도구 프레임워크이지만, 다음과 같은 실제 제한이 있습니다:

- **무상태성**: 데이터 관리를 클라이언트 측이나 외부 서비스에 의존합니다.
- **확장성 문제**: 무상태성은 세션 간의 데이터 일관성 처리를 어렵게 만듭니다.
- **외부 종속성**: 모델 SDK 및 벡터 저장소와 같은 외부 리소스에 의존합니다.

**OpenAI의 어시스턴트 API** 는 GPT와 같은 기능을 제공하는 데 뛰어나지만, 다음과 같은 제약이 있습니다:

- **기능의 결합**: 툴과 검색 같은 통합 기능은 각 어시스턴트에 결합되어 있어 멀티 테넌트 애플리케이션에 적합하지 않습니다.
- **전용 제한**: OpenAI 모델에 한정되어 있어 다양한 요구에 적합하지 않습니다.
- **맞춤화 제한**: 사용자들은 에이전트의 구성(메모리 및 검색 시스템 등)을 맞춤화할 수 없습니다.

### TaskingAI가 문제를 해결하는 방법 😃

- **무상태 및 유상태 사용 지원**: 메시지 기록과 에이전트 대화 세션을 추적 및 관리하거나, 무상태 채팅 완료 요청만 수행하는 경우 모두 지원합니다.
- **모듈화된 관리**: 툴, RAG 시스템, 언어 모델의 관리를 에이전트에서 분리하여, 이러한 모듈을 자유롭게 결합하여 강력한 AI 에이전트를 구성할 수 있습니다.
- **멀티 테넌트 지원**: TaskingAI는 개발 후 빠른 배포를 지원하며, 멀티 테넌트 시나리오에서도 사용할 수 있습니다. 클라우드 서비스에 대해 걱정할 필요 없이 AI 에이전트 개발에 집중할 수 있습니다.
- **통합 API**: TaskingAI는 모든 모듈(툴, RAG 시스템, 언어 모델 등)에 대한 통합 API를 제공하여, AI 에이전트의 구성을 쉽게 관리하고 변경할 수 있습니다.

## TaskingAI로 무엇을 구축할 수 있나요?

- [x] **인터랙티브 애플리케이션 데모**
- [x] **기업 생산성을 위한 AI 에이전트**
- [x] **비즈니스를 위한 멀티 테넌트 AI 네이티브 애플리케이션**

---

유용하다고 생각되면 **무료 스타🌟**를 주세요 😇

<p>
<img src="static/img/star.gif" alt="">
</p>

---

## Docker로 빠른 시작

자체 호스팅 TaskingAI 커뮤니티 에디션을 시작하는 간단한 방법은 [Docker](https://www.docker.com/)를 사용하는 것입니다.

### 사전 요구사항

- Docker 및 Docker Compose가 설치된 기기.
- 리포지토리를 클론하기 위한 Git의 설치.
- 클라이언트 SDK를 실행하기 위한 Python 환경(Python 3.8 이상).

### 설치

먼저, GitHub에서 TaskingAI(커뮤니티 에디션) 리포지토리를 클론합니다.

```bash
git clone https://github.com/taskingai/taskingai.git
cd taskingai
```

클론한 리포지토리 내부에서 docker 디렉토리로 이동하여 Docker Compose를 사용하여 서비스를 시작합니다.

```bash
cd docker
```

1. **`.env.example`을 `.env`로 복사하세요**:

   ```sh
   cp .env.example .env
   ```

2. **`.env` 파일을 편집하세요**:
   선호하는 텍스트 편집기에서 `.env` 파일을 열고 필요한 설정을 업데이트하세요. 필요한 모든 환경 변수가 정확하게 설정되어 있는지 확인하세요.

3. **Docker Compose를 시작하세요**:
   다음 명령어를 실행하여 모든 서비스를 시작하세요:
   ```sh
   docker-compose -p taskingai --env-file .env up -d
   ```

서비스가 실행되면, 브라우저를 통해 http://localhost:8080 주소로 TaskingAI 콘솔에 접속하세요. 기본 사용자 이름과 비밀번호는 `admin`과 `TaskingAI321`입니다.

### 업그레이드

이전 버전의 TaskingAI를 이미 설치한 경우, 최신 버전으로 업그레이드하려면 먼저 리포지토리를 업데이트합니다.

```bash
git pull origin master
```

그런 다음, 현재의 docker 서비스를 중지하고 최신 이미지를 풀하여 업그레이드한 후, 서비스를 다시 시작합니다.

```bash
cd docker
docker-compose -p taskingai down
docker-compose -p taskingai pull
docker-compose -p taskingai --env-file .env up -d
```

데이터 손실에 대해 걱정하지 마세요. 필요에 따라 데이터는 자동으로 최신 버전 스키마로 마이그레이션됩니다.

### TaskingAI UI 콘솔

[![TaskingAI 콘솔 데모](https://img.youtube.com/vi/4A5uQoawETU/maxresdefault.jpg)](https://youtu.be/4A5uQoawETU)

**_<p style="text-align: center; font-size: small;">위의 이미지를 클릭하여 TaskingAI 콘솔 데모 비디오를 시청하십시오.</p>_**

### TaskingAI 클라이언트 SDK

콘솔이 실행되면, TaskingAI 클라이언트 SDK를 사용하여 프로그래밍 방식으로 TaskingAI 서버와 상호 작용할 수 있습니다.

Python 3.8 이상이 설치되어 있고, 가상 환경을 설정하십시오(선택 사항이지만 권장됩니다).

pip를 사용하여 TaskingAI Python 클라이언트 SDK를 설치합니다.

```bash
pip install taskingai
```

다음은 클라이언트 코드 예제입니다:

```python
import taskingai
taskingai.init(api_key='YOUR_API_KEY', host='http://localhost:8080')

# 새로운 어시스턴트 생성
assistant = taskingai.assistant.create_assistant(
    model_id="YOUR_MODEL_ID",
    memory="naive",
)

# 새로운 채팅 생성
chat = taskingai.assistant.create_chat(
    assistant_id=assistant.assistant_id,
)

# 사용자 메시지 전송
taskingai.assistant.create_message(
    assistant_id=assistant.assistant_id,
    chat_id=chat.chat_id,
    text="Hello!",
)

# 어시스턴트 응답 생성
assistant_message = taskingai.assistant.generate_message(
    assistant_id=assistant.assistant_id,
    chat_id=chat.chat_id,
)

print(assistant_message)
```

`YOUR_API_KEY` 와 `YOUR_MODEL_ID` 는 콘솔에서 생성한 실제 API 키와 채팅 완료 모델 ID로 대체해야 합니다.

자세한 내용은 [문서](https://docs.tasking.ai/docs/guide/getting_started/self_hosting/overview)에서 확인할 수 있습니다.

## 리소스

- [문서](https://docs.tasking.ai)
- [API 참조](https://docs.tasking.ai/api)
- [문의하기](https://www.tasking.ai/contact-us)

## 커뮤니티와 기여

프로젝트에 기여하는 방법에 대해 알아보려면 [기여 지침](../CONTRIBUTING.md)을 확인해 주세요.

또한, TaskingAI가 공식 디스코드 커뮤니티를 개설했다는 소식을 전하게 되어 기쁩니다! 🎊

[저희 디스코드 서버에 가입하세요](https://discord.gg/RqwcD3vG3k)하시고 다음과 같은 활동에 참여하세요:

    • 💬 TaskingAI에 대한 토론을 하고, 아이디어를 공유하며, 피드백을 제공하세요.
    • 📚 다른 사용자 및 저희 팀으로부터 지원, 팁, 및 최고의 실천 방법을 얻으세요.
    • 🚀 최신 뉴스, 업데이트 및 기능 릴리스에 대해 최신 정보를 유지하세요.
    • 🤝 인공지능과 작업 자동화에 열정을 가진 사람들과 네트워킹을 하세요.

## 라이선스 및 행동 규범

TaskingAI는 특정의 [TaskingAI 오픈 소스 라이선스](./LICENSE) 하에 배포됩니다. 이 프로젝트에 기여함으로써 해당 조건을 준수하는 데 동의하게 됩니다.

## 지원 및 연락처

지원이 필요하면, [문서](https://docs.tasking.ai)를 참조하거나 [support@tasking.ai](mailto:support@tasking.ai)로 연락하십시오.
