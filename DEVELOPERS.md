# Developing TaskingAI

Welcome to the TaskingAI development community! Your contributions are essential for the growth and improvement of our project. This document will guide you through setting up and navigating our development environment.

- [Developing TaskingAI](#developing-taskingai)
  - [Getting Started](#getting-started)
  - [Install Dependencies](#install-dependencies)
  - [Local Development](#local-development)
    - [Fork the Repository](#fork-the-repository)
    - [Clone the Repository](#clone-the-repository)
    - [Inference](#inference)
    - [Plugin](#plugin)
    - [Backend](#backend)
    - [Frontend](#frontend)
  - [Submitting a Pull Request](#submitting-a-pull-request)
  - [Handling Issues](#handling-issues)
- [Common Development Tasks](#common-development-tasks)
  - [Implementing & Updating Inference and Plugins](#implementing--updating-inference-and-plugins)
- [Engaging with the Community](#engaging-with-the-community)
- [Acknowledging Contributors](#acknowledging-contributors)

## Getting Started

Thank you for your interest in [TaskingAI](https://www.tasking.ai) and your readiness to contribute! We encourage you to review our [code of conduct](https://github.com/TaskingAI/TaskingAI/blob/master/.github/CODE_OF_CONDUCT.md) and familiarize yourself with the existing [issues](https://github.com/TaskingAI/TaskingAI/issues) that you can help resolve. This guide will assist you in setting up your development environment.

### Install Dependencies

To set up TaskingAI on your system, you'll need the following tools:

- [Git](http://git-scm.com/)
- [Docker](https://docs.docker.com/get-docker/) (for running the studio locally)

For frontend:

- [Node.js v18.x (LTS)](http://nodejs.org) or higher
- [npm](https://www.npmjs.com/) version 10.1.0 or higher

For backend/inference/plugin:

- [Python 3.8+](https://www.python.org/downloads/)

## Local Development

We recommend using a local development environment to test and contribute to TaskingAI. Follow these steps to set up the project on your machine.

### Fork the Repository

Begin by forking the [TaskingAI repository](https://github.com/TaskingAI/TaskingAI).

### Clone the Repository

1. Clone your fork:

   ```sh
   git clone https://github.com/<your_github_username>/TaskingAI.git
   ```

2. Navigate to the TaskingAI directory:

   ```sh
   cd TaskingAI
   ```

### Inference

1. To develop for inference module, navigate to the `inference` directory:

   ```sh
   cd inference
   ```

2. Install the required packages:

   ```sh
    pip install -r requirements.txt
   ```

3. Copy the `.env.example` file to `.env`:

   ```sh
   cp .env.example .env
   ```

   After that you should fill in some of your own keys as you need.

4. Run the inference module:

   ```sh
   PYTHONPATH=$(pwd) python app/main.py
   ```

   Now you can develop and debug the `inference` module.

### Plugin

1. To develop for plugin module, navigate to the `plugin` directory:

   ```sh
   cd plugin
   ```

2. Install the required packages:

   ```sh
   pip install -r requirements.txt
   ```

3. Copy the `.env.example` file to `.env`:

   ```sh
   cp .env.example .env
   ```

   After that you should fill in some of your own keys as you need.

4. Run the plugin module:

   ```sh
   PYTHONPATH=$(pwd) python app/main.py
   ```

   Now you can develop and debug the `plugin` module.

### Backend

Before you start, you need to have 2 running instances of the inference and plugin modules. You can follow the steps above to run them. Also, you need to have 2 running instances of Postgres and Redis. You can use docker to run them. Make sure you have their ports exposed and you can access them from the backend module.

1. To develop for backend module, navigate to the `backend` directory:

   ```sh
   cd backend
   ```

2. Install the required packages:

   ```sh
   pip install -r requirements.txt
   ```

3. Copy the `.env.example` file to `.env`:

   ```sh
   cp .env.example .env
   ```

   Make sure the `TASKINGAI_INFERENCE_URL`, `TASKINGAI_PLUGIN_URL`, `POSTGRES_URL`, `REDIS_URL` are correctly set to the running instances of the inference, plugin, postgres and redis respectively.

4. Run the backend module:

   ```sh
   PYTHONPATH=$(pwd) python app/main.py
   ```

   Now you can develop and debug the `backend` module.

### Frontend

Before you start, you need to have the instances of `backend`, `inference`, `plugin`, `postgres` and `redis` running. You can follow the steps above to run them.

1. To develop for frontend module, navigate to the `frontend` directory:

   ```sh
   cd frontend
   ```

2. Install the required packages:

   ```sh
   npm install
   ```

3. Run the frontend module:

   ```sh
   npm run dev
   ```

Now you can develop and debug the `frontend` module.

## Submitting a Pull Request

After making changes, submit a pull request for review. Your contribution will be evaluated and potentially merged, adding you to our [list of contributors](https://github.com/TaskingAI/TaskingAI/graphs/contributors).

## Handling Issues

Feel free to tackle any open issues. If you see ongoing work by another contributor, consider collaborating with them.

## Common Development Tasks

### Implementing & Updating Inference and Plugins

The models and plugins are essential components of TaskingAI. You can contribute by implementing new models/plugins or updating existing ones.

For example, models can be added to the `inference/providers` directory, and plugins can be added to the `plugin/bundles` directory.

## Engaging with the Community

Join our [Discord Server](https://discord.gg/J3J2YySV) or [Forum](https://forum.tasking.ai) to connect with other contributors and users. Share your ideas, ask questions, and collaborate with the community.

## Acknowledging Contributors

View all contributors and their impact on our project [here](https://github.com/TaskingAI/TaskingAI/graphs/contributors).

This comprehensive guide is designed to assist you in becoming an active participant and contributor to TaskingAI. We're excited to see what you'll bring to the community!
