# 🚀 Dify POC Setup Guide

Dify is an open-source LLM application development platform. It integrates the concepts of Backend-as-a-Service and [LLMOps](https://docs.dify.ai/en/getting-started/readme/what-is-llmops), allowing developers to quickly build and iterate on generative AI applications with a visual interface.

> [!CAUTION]
> Dify consists of numerous microservices (Postgres, Redis, Weaviate, Sandbox, etc.). The initial deployment will pull several large images. Ensure you have a stable connection and at least 5GB of free disk space.

---

## 🛠 Prerequisites

- **Docker Desktop** (or Docker with Compose)
- **Git** installed on your system
- **Open Ports**: Port `80` must be available on your machine (or modified in `.env`).

---

## 📦 Installation Steps

<!-- Based on official docs: https://docs.dify.ai/en/self-host/quick-start/docker-compose -->

### 1. Clone the Repository
If you haven't already, clone the Dify source into the local `src` directory.
```bash
cd interfaces/dify
git clone git@github.com:langgenius/dify.git src
```

### 2. Initialize Configuration
Navigate to the Docker setup folder and initialize the environment variables.
```bash
cd src/docker
cp .env.example .env
```

### 3. Launch Services
Start the orchestrated containers in the background. This process handles the database migrations and internal networking.
```bash
docker compose up -d
```
> [!NOTE]
> This stage may take 3–10 minutes as it pulls base images for the API, Worker, and several database engines.

### 4. Verify Health
Ensure all containers are running gracefully:
```bash
docker compose ps
```

---

## 🧪 Next Steps & Testing

Once the containers are healthy:

1. **Access the Console**: Open your browser and go to **[http://localhost/install](http://localhost/install)**.
2. **Admin Setup**: Create your local administrator account.
3. **Connectivity**: 
   - Go to **Settings > Model Provider**.
   - Connect to your local backends (MLX, Ollama, or LM Studio) using `host.docker.internal` as the endpoint.

> [!TIP]
> Let me know when you reach the main workspace! We can then proceed to build your first **Agent Workflow** using your local models.
