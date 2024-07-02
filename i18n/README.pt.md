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

[TaskingAI](https://www.tasking.ai) é uma plataforma BaaS (Backend as a Service) para o **Desenvolvimento e Implantação de Agentes baseados em LLM**. Ela unifica a integração de centenas de modelos LLM e fornece uma interface de usuário intuitiva para gerenciar os módulos funcionais de sua aplicação LLM, incluindo ferramentas, sistemas RAG, assistentes, histórico de conversas e mais.

### Características Principais

1. **Plataforma LLM Tudo-em-Um**: Acesse centenas de modelos de IA com APIs unificadas.
2. **Ricas Melhoria**: Melhore o desempenho dos agentes LLM com centenas de ferramentas integradas personalizáveis e um sistema avançado de **Geração Aumentada por Recuperação** (RAG).
3. **Fluxo de Trabalho Inspirado em BaaS**: Separe a lógica de IA (lado do servidor) do desenvolvimento de produto (lado do cliente), oferecendo um caminho claro desde a criação de protótipos baseada em console até soluções escaláveis usando APIs RESTful e SDKs para clientes.
4. **Implantação com um Clique**: Implemente seus agentes de IA com um único clique na fase de produção, e escale-os com facilidade. Deixe que TaskingAI cuide do resto.
5. **Eficiência Assíncrona**: Utilize os recursos assíncronos do Python FastAPI para computação concorrente de alto desempenho, melhorando a capacidade de resposta e a escalabilidade das aplicações.
6. **Console de UI Intuitivo**: Simplifica a gestão de projetos e permite testes de fluxo de trabalho no console.

<p>
<img src="../static/img/console.png" alt="">
</p>

### Integrações

**Modelos**: TaskingAI se conecta a centenas de LLMs de vários provedores, incluindo OpenAI, Anthropic e mais. Também permitimos que os usuários integrem modelos locais através do Ollama, LM Studio e Local AI.

<p>
<img src="../static/img/model_providers.png" alt="">
</p>

**Plugins**: TaskingAI suporta uma ampla gama de plugins integrados para potencializar seus agentes de IA, incluindo busca no Google, leitor de sites, recuperação do mercado de ações e mais. Os usuários também podem criar ferramentas personalizadas para atender às suas necessidades específicas.

<p>
<img src="../static/img/plugins.png" alt="">
</p>

---

## Por que TaskingAI?

### Problemas com soluções existentes ??

**LangChain** é um framework de ferramentas para desenvolvimento de aplicação LLM, mas enfrenta limitações práticas:

- **Sem Estado**: Depende de serviços do cliente ou externos para gerenciamento de dados.
- **Desafios de Escalabilidade**: A ausência de estado impacta o manuseio consistente de dados entre sessões.
- **Dependências Externas**: Depende de recursos externos como SDKs de modelos e armazenamento vetorial.

**API de Assistente da OpenAI** se destaca na entrega de funcionalidades semelhantes ao GPT, mas tem suas próprias limitações:

- **Funcionalidades Vinculadas**: Integrações como ferramentas e recuperações estão vinculadas a cada assistente, inadequadas para aplicações multi-inquilinos.
- **Limitações Proprietárias**: Restrito a modelos OpenAI, inadequado para necessidades diversificadas.
- **Limites de Personalização**: Os usuários não podem personalizar a configuração do agente, como sistema de memória e recuperação.

### Como TaskingAI resolve o problema ??

- **Suporta usos com e sem estado**: Seja para acompanhar e gerenciar históricos de mensagens e sessões de conversação do agente, ou simplesmente fazer solicitações de conclusão de chat sem estado, TaskingAI cobre os dois casos.
- **Gestão Modular Desacoplada**: Separou a gestão de ferramentas, sistemas RAG, modelos de linguagem do agente. E permite a livre combinação desses módulos para construir um poderoso agente de IA.
- **Suporte Multi-inquilino**: TaskingAI suporta implantação rápida após o desenvolvimento e pode ser usado em cenários multi-inquilinos. Não se preocupe com os serviços em nuvem, concentre-se apenas no desenvolvimento do agente de IA.
- **API Unificada**: TaskingAI fornece APIs unificadas para todos os módulos, incluindo ferramentas, sistemas RAG, modelos de linguagem e mais. Super fácil de gerenciar e mudar as configurações do agente de IA.

## O que você pode construir com TaskingAI?

- [x] **Demonstrações Interativas de Aplicações**
- [x] **Agentes de IA para Produtividade Empresarial**
- [x] **Aplicações Nativas Multi-inquilino para Negócios**

---

Por favor, deixe-nos uma **ESTRELA GRATUITA ??** se achar útil ??

<p>
<img src="../static/img/star.gif" alt="">
</p>

---

## Início Rápido com Docker

Uma maneira simples de iniciar a edição comunitária auto-hospedada do TaskingAI é através do [Docker](https://www.docker.com/).

### Pré-requisitos

- Docker e Docker Compose instalados na sua máquina.
- Git instalado para clonar o repositório.
- Ambiente Python (acima do Python 3.8) para executar o SDK do cliente.

### Instalação

Primeiro, clone o repositório TaskingAI (edição comunitária) do GitHub.

```bash
git clone https://github.com/taskingai/taskingai.git
cd taskingai
```

Dentro do repositório clonado, vá para o diretório docker e inicie os serviços usando Docker Compose.

```bash
cd docker
```

1. **Copie `.env.example` para `.env`**:

   ```sh
   cp .env.example .env
   ```

2. **Edite o arquivo `.env`**:
   Abra o arquivo `.env` no seu editor de texto preferido e atualize as configurações necessárias. Certifique-se de que todas as variáveis de ambiente necessárias estejam configuradas corretamente.

3. **Inicie o Docker Compose**:
   Execute o seguinte comando para iniciar todos os serviços:
   ```sh
   docker-compose -p taskingai --env-file .env up -d
   ```

Uma vez que o serviço esteja ativo, acesse o console do TaskingAI pelo seu navegador utilizando a URL http://localhost:8080. O nome de usuário e senha padrões são `admin` e `TaskingAI321`.

### Atualização

Se você já instalou TaskingAI com uma versão anterior e deseja atualizar para a versão mais recente, primeiro atualize o repositório.

```bash
git pull origin master
```

Depois pare o serviço docker atual, atualize para a versão mais recente puxando a imagem mais nova e finalmente reinicie o serviço.

```bash
cd docker
docker-compose -p taskingai down
docker-compose -p taskingai pull
docker-compose -p taskingai --env-file .env up -d
```

Não se preocupe com a perda de dados; seus dados serão automaticamente migrados para o esquema da versão mais recente, se necessário.

### Console de UI do TaskingAI

[![Demonstração do Console TaskingAI](https://img.youtube.com/vi/4A5uQoawETU/maxresdefault.jpg)](https://youtu.be/4A5uQoawETU)

**_<p style="text-align: center; font-size: small; ">Clique na imagem acima para ver o vídeo de demonstração do Console do TaskingAI.</p>_**

### SDK Cliente do TaskingAI

Uma vez que o console esteja ativo, você pode interagir programaticamente com o servidor TaskingAI usando o SDK cliente do TaskingAI.

Certifique-se de ter Python 3.8 ou superior instalado e configurar um ambiente virtual (opcional, mas recomendado).

Instale o SDK cliente do TaskingAI usando pip.

```bash
pip install taskingai
```

Aqui está um exemplo de código cliente:

```python
import taskingai
taskingai.init(api_key='YOUR_API_KEY', host='http://localhost:8080')

# Create a new assistant
assistant = taskingai.assistant.create_assistant(
    model_id="YOUR_MODEL_ID",
    memory="naive",
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

Note que `YOUR_API_KEY` e `YOUR_MODEL_ID` devem ser substituídos pela chave API real e ID do modelo de conclusão de chat que você criou no console.

Você pode aprender mais na [documentação](https://docs.tasking.ai/docs/guide/getting_started/self_hosting/overview).

## Recursos

- [Documentação](https://docs.tasking.ai)
- [Referência API](https://docs.tasking.ai/api)
- [Entre em contato](https://www.tasking.ai/contact-us)

## Comunidade e Contribuição

Por favor, consulte nossas [diretrizes de contribuição](../CONTRIBUTING.md) para saber como contribuir para o projeto.

Além disso, estamos entusiasmados em anunciar que o TaskingAI agora tem uma comunidade oficial no Discord! 🎊

[Junte-se ao nosso servidor do Discord](https://discord.gg/RqwcD3vG3k) para:

    • 💬 Participar de discussões sobre o TaskingAI, compartilhar ideias e fornecer feedback.
    • 📚 Obter suporte, dicas e melhores práticas de outros usuários e nossa equipe.
    • 🚀 Manter-se atualizado sobre as últimas notícias, atualizações e lançamentos de recursos.
    • 🤝 Conectar-se com indivíduos com interesses similares apaixonados por IA e automação de tarefas.

## Licença e Código de Conduta

TaskingAI é publicado sob uma [Licença Open Source Específica do TaskingAI](../LICENSE). Ao contribuir para este projeto, você concorda em seguir seus termos.

## Suporte e Contato

Para suporte, por favor consulte nossa [documentação](https://docs.tasking.ai) ou entre em contato conosco em [support@tasking.ai](mailto:support@tasking.ai).
