# 💎 Onyx Setup Guide (formerly Danswer)

Onyx is an open-source enterprise search and RAG platform. It allows you to connect your local models to your company data (Slack, GitHub, Confluence, etc.) and perform complex document retrieval and question answering.

> [!CAUTION]
> Onyx is a heavyweight platform with many microservices (Postgres, Redis, Vespa, Background workers). Ensure you have at least **16GB of RAM** and enough disk space for the initial image pulls.

---

## 🛠 Prerequisites

- **Docker Desktop** (or Docker with Compose)
- **Git**
- **Resources**: High CPU/RAM recommended for vector search indexing.

---

## 📦 Installation Steps

Onyx provides a guided script which is the recommended way to manage the complex environment variables and versioning.

### 1. Run the Guided Installation
You can use the official installation script which will handle the configuration for you. Run this from your terminal:

```bash
curl -fsSL https://onyx.app/install_onyx.sh | bash
```

Alternatively, you can manually clone the repository if you want full control:

### 2. Manual Clone (Optional)
```bash
cd interfaces/onyx
git clone https://github.com/onyx-dot-app/onyx.git src
cd src/deployment/docker_compose
cp env.template .env
```

### 3. Launch Services
If you went the manual route, start the containers:

```bash
docker compose up -d
```

> [!NOTE]
> The first run can take **5-15 minutes** as it needs to pull the base images and initialize the Vespa vector database.

---

## 🧪 Post-Installation

Once the services are healthy:

1. **Access the UI**: Open **[http://localhost:3000](http://localhost:3000)**.
2. **Setup Admin**: Follow the on-screen instructions to create the first admin account.
3. **Connect Local LLM**: 
   - Navigate to **Admin Panel > LLM Configuration**.
   - Select **Ollama** or **Custom** for local backends.
   - Use `http://host.docker.internal:11434` for Ollama connection from within Docker.

> [!TIP]
> Use the **Lite Mode** during the guided install if you are running on a machine with limited resources (e.g., < 16GB RAM).
