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

[TaskingAI](https://www.tasking.ai) est une plateforme BaaS (Backend as a Service) pour le **développement et déploiement d'agents basés sur LLM**. Elle unifie l'intégration de centaines de modèles LLM et offre une interface utilisateur intuitive pour gérer les modules fonctionnels de votre application LLM, y compris les outils, les systèmes RAG, les assistants, l'historique des conversations, et bien plus encore.

### Caractéristiques Clés

1. **Plateforme LLM Tout-en-Un** : Accédez à des centaines de modèles IA avec des API unifiées.
2. **Améliorations Abondantes** : Améliorez les performances de l'agent LLM avec des centaines d'**outils** intégrés personnalisables et un système avancé de **Retrieval-Augmented Generation** (RAG).
3. **Flux de Travail Inspiré par le BaaS** : Séparez la logique IA (côté serveur) du développement produit (côté client), offrant un chemin clair du prototypage basé sur console à des solutions évolutives utilisant des API RESTful et des SDK client.
4. **Déploiement en un Clic** : Déployez vos agents IA en un clic en phase de production, et mettez-les à l'échelle facilement. Laissez TaskingAI s'occuper du reste.
5. **Efficacité Asynchrone** : Exploitez les fonctionnalités asynchrones de Python FastAPI pour des calculs concurrentiels haute-performance, améliorant la réactivité et la scalabilité des applications.
6. **Console UI Intuitive** : Simplifie la gestion de projet et permet les tests de workflow dans la console.

<p>
<img src="../static/img/console.png" alt="">
</p>

### Intégrations

**Modèles** : TaskingAI se connecte à des centaines de LLM de divers fournisseurs, dont OpenAI, Anthropic, et plus. Nous permettons également aux utilisateurs d'intégrer des modèles hôtes locaux via Ollama, LM Studio et Local AI.

<p>
<img src="../static/img/model_providers.png" alt="">
</p>

**Plugins** : TaskingAI prend en charge une large gamme de plugins intégrés pour renforcer vos agents IA, y compris la recherche Google, le lecteur de sites web, la récupération du marché boursier, et plus. Les utilisateurs peuvent également créer des outils personnalisés pour répondre à leurs besoins spécifiques.

<p>
<img src="../static/img/plugins.png" alt="">
</p>

---

## Pourquoi TaskingAI ?

### Problèmes des solutions existantes 🙁

**LangChain** est un framework d'outils pour le développement d'applications LLM, mais il présente des limitations pratiques :

- **Sans État** : Dépend de services client ou externes pour la gestion des données.
- **Défis de Scalabilité** : L'absence d'état impacte le traitement cohérent des données entre les sessions.
- **Dépendances Externes** : Dépend de ressources externes comme les SDK modèles et le stockage vectoriel.

**Assistant API d'OpenAI** excelle dans la fourniture de fonctionnalités de type GPT mais présente ses propres contraintes :

- **Fonctionnalités Liées** : Les intégrations comme les outils et les récupérations sont liées à chaque assistant, non adaptées pour des applications multi-locataires.
- **Limites Propriétaires** : Restreint aux modèles OpenAI, inappropriés pour des besoins divers.
- **Limites de Personnalisation**: Les utilisateurs ne peuvent pas personnaliser la configuration de l'agent comme le système de mémoire et de récupération.

### Comment TaskingAI résout le problème 😃

- **Prend en charge les usages avec ou sans état** : Que ce soit pour suivre et gérer l'historique des messages et les sessions de conversation de l'agent, ou simplement faire des demandes de complétion de chat sans état, TaskingAI couvre les deux.
- **Gestion modulaire découplée** : Gestion découplée des outils, des systèmes RAG, des modèles de langue de l'agent. Et permet la combinaison libre de ces modules pour créer un puissant agent IA.
- **Support Multi-Locataire** : TaskingAI prend en charge le déploiement rapide après le développement et peut être utilisé dans des scénarios multi-locataires. Pas besoin de se soucier des services cloud, concentrez-vous simplement sur le développement d'agents IA.
- **API Unifiée** : TaskingAI fournit des API unifiées pour tous les modules, y compris les outils, les systèmes RAG, les modèles de langue, et plus encore. Super facile à gérer et à modifier les configurations de l'agent IA.

## Ce que vous pouvez créer avec TaskingAI

- [x] **Démos d'Applications Interactives**
- [x] **Agents IA pour la Productivité en Entreprise**
- [x] **Applications Native-Multi-Locataire pour les Entreprises**

---

Merci de nous donner une **ÉTOILE GRATUITE 🌟** si vous le trouvez utile 😇

<p>
<img src="../static/img/star.gif" alt="">
</p>

---

## Démarrage rapide avec Docker

Un moyen simple de lancer l'édition communautaire autohébergée de TaskingAI est via [Docker](https://www.docker.com/).

### Conditions Préliminaires

- Docker et Docker Compose installés sur votre machine.
- Git installé pour cloner le dépôt.
- Environnement Python (au-dessus de Python 3.8) pour exécuter le SDK client.

### Installation

Tout d'abord, clonez le dépôt TaskingAI (version communautaire) depuis GitHub.

```bash
git clone https://github.com/taskingai/taskingai.git
cd taskingai
```

À l'intérieur du dépôt cloné, allez dans le répertoire docker et lancez les services avec Docker Compose.

```bash
cd docker
```

1. **Copiez `.env.example` en `.env`** :

   ```sh
   cp .env.example .env
   ```

2. **Éditez le fichier `.env`** :
   Ouvrez le fichier `.env` dans votre éditeur de texte préféré et mettez à jour les configurations nécessaires. Assurez-vous que toutes les variables d'environnement requises sont correctement définies.

3. **Lancez Docker Compose** :
   Exécutez la commande suivante pour démarrer tous les services :
   ```sh
   docker-compose -p taskingai --env-file .env up -d
   ```

Une fois le service lancé, accédez à la console TaskingAI via votre navigateur à l'URL http://localhost:8080. Le nom d'utilisateur et le mot de passe par défaut sont `admin` et `TaskingAI321`.

### Mise à Jour

Si vous avez déjà installé TaskingAI avec une version précédente et souhaitez mettre à jour vers la dernière version, mettez d'abord à jour le dépôt.

```bash
git pull origin master
```

Puis arrêtez le service docker actuel, mettez à niveau vers la dernière version en tirant l'image la plus récente, et enfin redémarrez le service.

```bash
cd docker
docker-compose -p taskingai down
docker-compose -p taskingai pull
docker-compose -p taskingai --env-file .env up -d
```

Ne vous inquiétez pas de la perte de données; vos données seront automatiquement migrées vers le nouveau schéma de version si nécessaire.

### Console UI TaskingAI

[![Démonstration de la Console TaskingAI](https://img.youtube.com/vi/4A5uQoawETU/maxresdefault.jpg)](https://youtu.be/4A5uQoawETU)

**_<p style="text-align: center; font-size: small; ">Cliquez sur l'image ci-dessus pour voir la vidéo de démo de la console TaskingAI.</p>_**

### SDK Client TaskingAI

Une fois la console opérationnelle, vous pouvez interagir de manière programmatique avec le serveur TaskingAI en utilisant le SDK client TaskingAI.

Assurez-vous d'avoir installé Python 3.8 ou une version supérieure, et configurez un environnement virtuel (optionnel mais recommandé).

Installez le SDK client Python TaskingAI en utilisant pip.

```bash
pip install taskingai
```

Voici un exemple de code client :

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

Notez que `YOUR_API_KEY` et `YOUR_MODEL_ID` doivent être remplacés par la clé API et l'ID du modèle de completion de chat réels que vous avez créés dans la console.

Vous pouvez en apprendre plus dans la [documentation](https://docs.tasking.ai/docs/guide/getting_started/self_hosting/overview).

## Ressources

- [Documentation](https://docs.tasking.ai)
- [Référence API](https://docs.tasking.ai/api)
- [Nous Contacter](https://www.tasking.ai/contact-us)

## Communauté et Contribution

Veuillez consulter nos [directives de contribution](../CONTRIBUTING.md) pour savoir comment contribuer au projet.

De plus, nous sommes ravis d'annoncer que TaskingAI possède désormais une communauté officielle sur Discord ! 🎊

[Rejoignez notre serveur Discord](https://discord.gg/RqwcD3vG3k) pour :

    • 💬 Engager des discussions sur TaskingAI, partager des idées et donner votre avis.
    • 📚 Obtenir de l'aide, des conseils et des meilleures pratiques de la part d'autres utilisateurs et de notre équipe.
    • 🚀 Restez informé des dernières nouvelles, mises à jour et sorties de fonctionnalités.
    • 🤝 Réseauter avec des individus partageant les mêmes intérêts, passionnés par l'IA et l'automatisation des tâches.

## Licence et Code de Conduite

TaskingAI est publié sous une [licence open source spécifique de TaskingAI](../LICENSE). En contribuant à ce projet, vous acceptez de respecter ses termes.

## Support et Contact

Pour le support, veuillez vous référer à notre [documentation](https://docs.tasking.ai) ou contactez-nous à [support@tasking.ai](mailto:support@tasking.ai).
