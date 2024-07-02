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

[TaskingAI](https://www.tasking.ai) ist eine BaaS (Backend as a Service) Plattform für die **Entwicklung und Bereitstellung von LLM-basierten Agenten**. Es integriert hunderte von LLM-Modellen und bietet eine intuitive Benutzeroberfläche zur Verwaltung der Funktionalmodule Ihrer LLM-Anwendung, einschließlich Tools, RAG-Systeme, Assistenten, Konversationshistorie und mehr.

### Wichtige Funktionen

1. **All-In-One-LLM-Plattform**: Zugriff auf hunderte von KI-Modellen mit einheitlichen APIs.
2. **Reiche Erweiterungen**: Verbessern Sie LLM-Agentenleistungen mit hunderten anpassbaren integrierten **Tools** und einem fortschrittlichen **Retrieval-Augmented Generation** (RAG) System.
3. **BaaS-inspirierter Workflow**: Trennt die KI-Logik (serverseitig) von der Produktentwicklung (clientseitig) und bietet einen klaren Weg von der Prototypenerstellung auf Konsolenbasis zu skalierbaren Lösungen mittels RESTful APIs und Client-SDKs.
4. **Ein-Klick zur Produktion**: Stellen Sie Ihre KI-Agenten mit einem Klick in die Produktionsphase und skalieren Sie sie einfach. Lassen Sie TaskingAI den Rest erledigen.
5. **Asynchrone Effizienz**: Nutzen Sie die asynchronen Funktionen von Python FastAPI für hochleistungsfähige, gleichzeitige Berechnungen, um die Reaktionsfähigkeit und Skalierbarkeit der Anwendungen zu verbessern.
6. **Intuitive UI-Konsole**: Vereinfacht das Projektmanagement und ermöglicht Workflow-Tests in der Konsole.

<p>
<img src="../static/img/console.png" alt="">
</p>

### Integrationen

**Modelle**: TaskingAI verbindet sich mit hunderten LLMs von verschiedenen Anbietern, einschließlich OpenAI, Anthropic und mehr. Wir ermöglichen Benutzern auch die Integration lokaler Host-Modelle über Ollama, LM Studio und Local AI.

<p>
<img src="../static/img/model_providers.png" alt="">
</p>

**Plugins**: TaskingAI unterstützt eine breite Palette integrierter Plugins, um Ihre KI-Agenten zu stärken, einschließlich Google-Suche, Webseitenleser, Aktienmarktabruf und mehr. Benutzer können auch benutzerdefinierte Tools erstellen, um ihre spezifischen Anforderungen zu erfüllen.

<p>
<img src="../static/img/plugins.png" alt="">
</p>

---

## Warum TaskingAI?

### Probleme mit bestehenden Lösungen 🙁

**LangChain** ist ein Werkzeug-Framework für die LLM-Anwendungsentwicklung, stößt jedoch auf praktische Einschränkungen:

- **Zustandslosigkeit**: Abhängig von clientseitigen oder externen Diensten für das Datenmanagement.
- **Skalierbarkeitsprobleme**: Zustandslosigkeit beeinträchtigt die konsistente Datenhandhabung über Sitzungen hinweg.
- **Externe Abhängigkeiten**: Abhängigkeit von externen Ressourcen wie Modell-SDKs und Vektorspeichern.

**OpenAIs Assistant API** ist hervorragend in der Bereitstellung von GPT-ähnlichen Funktionen, hat aber eigene Einschränkungen:

- **Gebundene Funktionalitäten**: Integrationen wie Tools und Retrievals sind an jeden Assistenten gebunden und nicht für Multi-Tenant-Anwendungen geeignet.
- **Proprietäre Einschränkungen**: Beschränkt auf OpenAI-Modelle, ungeeignet für vielfältige Anforderungen.
- **Anpassungsgrenzen**: Benutzer können die Agentenkonfiguration wie Speicher- und Retrievalsysteme nicht anpassen.

### Wie TaskingAI das Problem löst 😃

- **Unterstützt sowohl Zustands- als auch zustandslose Verwendungen**: Ob Nachrichtenhistorien und Agentenkonversationssitzungen nachverfolgt und verwaltet werden sollen oder nur zustandslose Chat-Abschlussanfragen gestellt werden sollen, TaskingAI deckt beide ab.
- **Entkoppelte modulare Verwaltung**: Entkoppelte Verwaltung von Tools, RAGs-Systemen, Sprachmodellen vom Agenten. Und ermöglicht die freie Kombination dieser Module, um einen leistungsstarken KI-Agenten zu erstellen.
- **Multi-Tenant-Unterstützung**: TaskingAI unterstützt schnelle Bereitstellung nach der Entwicklung und kann in Multi-Tenant-Szenarien verwendet werden. Keine Sorge um Cloud-Dienste, konzentrieren Sie sich einfach auf die Entwicklung von KI-Agenten.
- **Einheitliche API**: TaskingAI bietet einheitliche APIs für alle Module, einschließlich Tools, RAGs-Systeme, Sprachmodelle und mehr. Super einfach zu verwalten und Änderungen an den Konfigurationen des KI-Agenten vorzunehmen.

## Was können Sie mit TaskingAI erstellen?

- [x] **Interaktive Anwendungsdemos**
- [x] **KI-Agenten für Unternehmensproduktivität**
- [x] **Multi-Tenant-KI-native Anwendungen für Unternehmen**

---

Bitte geben Sie uns einen **GRATIS STERN 🌟**, wenn Sie es hilfreich finden 😇

<p>
<img src="../static/img/star.gif" alt="">
</p>

---

## Schnellstart mit Docker

Eine einfache Möglichkeit, die selbst gehostete TaskingAI Community Edition zu starten, ist über [Docker](https://www.docker.com/).

### Voraussetzungen

- Docker und Docker Compose auf Ihrem Rechner installiert.
- Git installiert zum Klonen des Repository.
- Python-Umgebung (ab Python 3.8) zum Ausführen des Client-SDK.

### Installation

Zuerst klonen Sie das TaskingAI (Community Edition) Repository von GitHub.

```bash
git clone https://github.com/taskingai/taskingai.git
cd taskingai
```

Wechseln Sie innerhalb des geklonten Repositorys in das Docker-Verzeichnis und starten Sie die Dienste mit Docker Compose.

```bash
cd docker
```

1. **Kopiere `.env.example` zu `.env`**:

   ```sh
   cp .env.example .env
   ```

2. **Bearbeite die `.env` Datei**:

   Öffne die `.env`-Datei in deinem bevorzugten Texteditor und aktualisiere die notwendigen Konfigurationen. Stelle sicher, dass alle erforderlichen Umgebungsvariablen korrekt gesetzt sind.

3. **Starte Docker Compose**:
   Führe den folgenden Befehl aus, um alle Dienste zu starten:
   ```sh
   docker-compose -p taskingai --env-file .env up -d
   ```

Sobald der Dienst läuft, kannst du über deinen Browser mit der URL http://localhost:8080 auf die TaskingAI-Konsole zugreifen. Der Standardbenutzername und das Standardpasswort sind `admin` und `TaskingAI321`.

### Upgrade

Wenn Sie TaskingAI bereits mit einer vorherigen Version installiert haben und auf die neueste Version upgraden möchten, aktualisieren Sie zuerst das Repository.

```bash
git pull origin master
```

Stoppen Sie dann den aktuellen Docker-Dienst, aktualisieren Sie auf die neueste Version, indem Sie das neueste Image ziehen, und starten Sie den Dienst schließlich neu.

```bash
cd docker
docker-compose -p taskingai down
docker-compose -p taskingai pull
docker-compose -p taskingai --env-file .env up -d
```

Keine Sorge wegen Datenverlust; Ihre Daten werden automatisch auf das neueste Schema migriert, falls erforderlich.

### TaskingAI UI-Konsole

[![TaskingAI Console Demo](https://img.youtube.com/vi/4A5uQoawETU/maxresdefault.jpg)](https://youtu.be/4A5uQoawETU)

**<p style="text-align: center; font-size: small; ">Klicken Sie auf das obige Bild, um das TaskingAI Console Demo Video anzusehen.</p>**

### TaskingAI Client SDK

Sobald die Konsole läuft, können Sie programmgesteuert über das TaskingAI Client SDK mit dem TaskingAI-Server interagieren.

Stellen Sie sicher, dass Python 3.8 oder höher installiert ist, und richten Sie eine virtuelle Umgebung ein (optional, aber empfohlen).

Installieren Sie das TaskingAI Python Client SDK mit pip.

```bash
pip install taskingai
```

Hier ist ein Beispiel für Client-Code:

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

Bitte ersetzen Sie `YOUR_API_KEY` und `YOUR_MODEL_ID` durch den tatsächlichen API-Schlüssel und die Chat-Vervollständigungs-Modell-ID, die Sie in der Konsole erstellt haben.

Weitere Informationen finden Sie in der [Dokumentation](https://docs.tasking.ai/docs/guide/getting_started/self_hosting/overview).

## Ressourcen

- [Dokumentation](https://docs.tasking.ai)
- [API-Referenz](https://docs.tasking.ai/api)
- [Kontaktieren Sie uns](https://www.tasking.ai/contact-us)

## Community und Beitrag

Bitte beachten Sie unsere [Beitragsrichtlinien](../CONTRIBUTING.md), um zu erfahren, wie Sie zum Projekt beitragen können.

Außerdem freuen wir uns, ankündigen zu können, dass TaskingAI jetzt eine offizielle Discord-Community hat! 🎊

[Treten Sie unserem Discord-Server bei](https://discord.gg/RqwcD3vG3k), um:

    • 💬 Diskussionen über TaskingAI zu führen, Ideen auszutauschen und Feedback zu geben.
    • 📚 Unterstützung, Tipps und bewährte Methoden von anderen Nutzern und unserem Team zu erhalten.
    • 🚀 Auf dem Laufenden über die neuesten Nachrichten, Updates und Feature-Veröffentlichungen zu bleiben.
    • 🤝 Mit Gleichgesinnten zu vernetzen, die eine Leidenschaft für KI und Aufgabenautomatisierung teilen.

## Lizenz und Verhaltenskodex

TaskingAI wird unter einer spezifischen [TaskingAI Open Source License](../LICENSE) veröffentlicht. Mit Ihrem Beitrag zu diesem Projekt stimmen Sie zu, sich an dessen Bedingungen zu halten.

## Unterstützung und Kontakt

Für Unterstützung lesen Sie bitte unsere [Dokumentation](https://docs.tasking.ai) oder kontaktieren Sie uns unter [support@tasking.ai](mailto:support@tasking.ai).

```

```
