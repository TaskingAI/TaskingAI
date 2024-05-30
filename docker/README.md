# Quick Start TaskingAI with Docker

`docker-compose.yml` is a simple example of Docker Compose setup for TaskingAI. For more information about docker setup, please refer to the [TaskingAI Documentation](https://docs.tasking.ai/docs/guide/self-hosting-with-docker).

## Steps to Get Started

1. **Copy `.env.example` to `.env`**:

   ```sh
   cp .env.example .env
   ```

2. **Edit the `.env` file**:
   Open the `.env` file in your favorite text editor and update the necessary configurations. Ensure all required environment variables are set correctly.

3. **Start Docker Compose**:
   Run the following command to start all services:
   ```sh
   docker-compose -p taskingai --env-file .env up -d
   ```
