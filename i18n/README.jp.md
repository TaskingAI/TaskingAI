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

[TaskingAI](https://www.tasking.ai) は、**LLMベースのエージェント開発とデプロイメント**のためのBaaS（Backend as a Service）プラットフォームです。数百のLLMモデルの統合を統一し、ツール、RAGシステム、アシスタント、会話履歴など、LLMアプリケーションの機能モジュールを管理する直感的なユーザーインターフェイスを提供します。

### 主な特徴

1. **オールインワンLLMプラットフォーム**：数百のAIモデルに統一APIでアクセスできます。
2. **豊富な拡張機能**：数百のカスタマイズ可能な内蔵**ツール**と高度な**リトリーバル強化生成**(RAG)システムでLLMエージェントのパフォーマンスを向上させます。
3. **BaaSインスパイアのワークフロー**：AIロジック（サーバー側）と製品開発（クライアント側）を分離し、コンソールベースのプロトタイピングからスケーラブルなソリューションへの明確な経路を提供します。
4. **ワンクリックで本番導入**：AIエージェントをワンクリックで本番段階にデプロイし、簡単にスケールアップします。TaskingAIが残りの処理を行います。
5. **非同期効率**：Python FastAPIの非同期機能を利用して高性能な並列計算を行い、アプリケーションの応答性とスケーラビリティを向上させます。
6. **直感的なUIコンソール**：プロジェクト管理を簡素化し、コンソール内でワークフローをテストできます。

<p>
<img src="static/img/console.png" alt="">
</p>

### 統合

**モデル**：TaskingAIは、OpenAIやAnthropicなど、さまざまなプロバイダーから数百のLLMを接続します。また、Ollama、LM Studio、Local AIを介してローカルホストモデルを統合することも可能です。

<p>
<img src="../static/img/model_providers.png" alt="">
</p>

**プラグイン**：TaskingAIは、Google検索、ウェブサイトリーダー、株式市場検索など、多くの内蔵プラグインをサポートしており、AIエージェントを強化します。ユーザーは特定のニーズに合わせたカスタムツールも作成できます。

<p>
<img src="../static/img/plugins.png" alt="">
</p>

---

## なぜ TaskingAI を選ぶのか？

### 既存のソリューションの問題点 🙁

**LangChain** はLLMアプリケーション開発のためのツールフレームワークですが、実際の制約があります：

- **ステートレス**：データ管理にクライアントサイドや外部サービスに依存しています。
- **スケーラビリティの課題**：ステートレス性がセッション間でのデータの一貫した取り扱いに影響を与えます。
- **外部依存性**：モデルSDKやベクトルストレージなどの外部リソースに依存しています。

**OpenAIのAssistant API** はGPTのような機能を提供することに優れているものの、以下の制約があります：

- **機能の結びつき**：ツールや検索の統合が各アシスタントに結びついていて、マルチテナントアプリケーションには適していません。
- **専有の制限**：OpenAIモデルに限定されており、多様なニーズには適していません。
- **カスタマイズの制約**：ユーザーはエージェントの構成をカスタマイズできません（メモリや検索システムなど）。

### TaskingAIなら解決できる 😃

- **ステートフルおよびステートレスの両方をサポート**：メッセージ履歴やエージェント会話セッションを追跡および管理するか、またはステートレスなチャット完了リクエストを行うだけか、どちらも対応できます。
- **モジュールの分離管理**：ツール、RAGシステム、言語モデルの管理をエージェントから分離し、これらのモジュールを自由に組み合わせて強力なAIエージェントを構築できます。
- **マルチテナントサポート**：開発後の迅速なデプロイをサポートし、マルチテナントのシナリオでも利用可能です。クラウドサービスについて心配する必要はなく、AIエージェントの開発に専念できます。
- **統一API**：タスクごとに統一されたAPIを提供し、ツール、RAGシステム、言語モデルなどの構成を簡単に管理および変更できます。

## TaskingAIで何が作れるか？

- [x] **インタラクティブアプリのデモ**
- [x] **企業の生産性向上のためのAIエージェント**
- [x] **ビジネス用のマルチテナントAIネイティブアプリケーション**

---

これが役立つと感じたなら、ぜひ **無料スター🌟** をください 😇

<p>
<img src="static/img/star.gif" alt="">
</p>

---

## Dockerで簡単スタート

自ホストのTaskingAIコミュニティエディションを起動する簡単な方法は [Docker](https://www.docker.com/) を利用することです。

### 前提条件

- DockerとDocker Composeがインストールされたマシン。
- リポジトリをクローンするためのGitのインストール。
- クライアントSDKを実行するためのPython環境（Python 3.8以上）。

### インストール

まず、GitHubからTaskingAI（コミュニティエディション）をクローンします。

```bash
git clone https://github.com/taskingai/taskingai.git
cd taskingai
```

クローンしたリポジトリの中でdockerディレクトリに移動し、Docker Composeを使ってサービスを起動します。

```bash
cd docker
```

1. **`.env.example`を`.env`にコピーします**：

   ```sh
   cp .env.example .env
   ```

2. **`.env`ファイルを編集します**：
   お好みのテキストエディタで`.env`ファイルを開き、必要な設定を更新してください。必要な環境変数が正しく設定されていることを確認してください。

3. **Docker Composeを起動します**：
   以下のコマンドを実行して、すべてのサービスを開始します：
   ```sh
   docker-compose -p taskingai --env-file .env up -d
   ```

サービスが起動したら、URL http://localhost:8080 をブラウザで開いてTaskingAIコンソールにアクセスします。デフォルトのユーザー名とパスワードは`admin`と`TaskingAI321`です。

### アップグレード

既に以前のバージョンのTaskingAIをインストールしていて、最新バージョンにアップグレードしたい場合は、まずリポジトリを更新します。

```bash
git pull origin master
```

次に、現在のdockerサービスを停止し、最新のイメージをプルしてアップグレードし、最後にサービスを再起動します。

```bash
cd docker
docker-compose -p taskingai down
docker-compose -p taskingai pull
docker-compose -p taskingai --env-file .env up -d
```

データ損失の心配はありません。必要に応じて、データは自動的に最新バージョンスキーマに移行されます。

### TaskingAI UIコンソール

[![TaskingAIコンソールデモ](https://img.youtube.com/vi/4A5uQoawETU/maxresdefault.jpg)](https://youtu.be/4A5uQoawETU)

**_<p style="text-align: center; font-size: small;">上の画像をクリックして、TaskingAIコンソールデモビデオを視聴してください。</p>_**

### TaskingAIクライアントSDK

コンソールが起動したら、TaskingAIクライアントSDKを使用してプログラム的にTaskingAIサーバーと対話します。

Python 3.8以上がインストールされていることを確認し、仮想環境を設定します（任意ですが推奨）。

pipを使用してTaskingAI PythonクライアントSDKをインストールします。

```bash
pip install taskingai
```

以下はクライアントのコード例です：

```python
import taskingai
taskingai.init(api_key='YOUR_API_KEY', host='http://localhost:8080')

# 新しいアシスタントを作成
assistant = taskingai.assistant.create_assistant(
    model_id="YOUR_MODEL_ID",
    memory="naive",
)

# 新しいチャットを作成
chat = taskingai.assistant.create_chat(
    assistant_id=assistant.assistant_id,
)

# ユーザーのメッセージを送信
taskingai.assistant.create_message(
    assistant_id=assistant.assistant_id,
    chat_id=chat.chat_id,
    text="Hello!",
)

# アシスタントの応答を生成
assistant_message = taskingai.assistant.generate_message(
    assistant_id=assistant.assistant_id,
    chat_id=chat.chat_id,
)

print(assistant_message)
```

`YOUR_API_KEY` と `YOUR_MODEL_ID` は、コンソールで作成した実際のAPIキーとチャット完了モデルIDに置き換えてください。

詳細は[ドキュメント](https://docs.tasking.ai/docs/guide/getting_started/self_hosting/overview)をご覧ください。

## リソース

- [ドキュメント](https://docs.tasking.ai)
- [APIリファレンス](https://docs.tasking.ai/api)
- [お問い合わせ](https://www.tasking.ai/contact-us)

## コミュニティと貢献

プロジェクトへの貢献方法については、[貢献ガイドライン](../CONTRIBUTING.md)をご覧ください。

また、TaskingAIに公式Discordコミュニティができたことをお知らせいたします！ 🎊

[Discordサーバーに参加する](https://discord.gg/RqwcD3vG3k)ことで：

    • 💬 TaskingAIについての議論に参加し、アイデアを共有し、フィードバックを提供。
    • 📚 他のユーザーや私たちのチームからのサポート、ヒント、ベストプラクティスを受け取る。
    • 🚀 最新のニュース、アップデート、機能リリースを常に更新。
    • 🤝 AIとタスク自動化に情瞭のある同じ志を持つ人々とネットワーキング。

## ライセンスと行動規範

TaskingAIは特定の[TaskingAIオープンソースライセンス](./LICENSE)の下でリリースされています。このプロジェクトに貢献することで、その条項に従うことに同意したことになります。

## サポートとお問い合わせ

サポートについては、[ドキュメント](https://docs.tasking.ai)を参照するか、[support@tasking.ai](mailto:support@tasking.ai)までお問い合わせください。
