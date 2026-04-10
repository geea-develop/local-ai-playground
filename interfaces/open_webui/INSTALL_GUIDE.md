# 🌐 Open WebUI POC Setup Guide

Open WebUI is the definitive community-driven interface for local LLMs, particularly Ollama. It strikes a balance between a simple chat interface and a powerful extensible platform via Python "Functions."

---

## 🛠 Prerequisites

- **Docker Desktop**
- **Ollama** running locally on your Mac.

---

## 📦 Installation Steps

### 1. Launch Open WebUI
```bash
cd interfaces/open_webui
mkdir -p data
docker compose up -d
```

### 2. Access the UI
Open your browser and navigate to: **[http://localhost:3000](http://localhost:3000)**

### 3. Account Setup
1.  **Sign Up**: Create your first account (this will automatically be the Admin account).
2.  **Connection**: By default, it will look for Ollama at `http://host.docker.internal:11434`.
3.  **Model Selection**: Click the model selector at the top; your `mistral:v0.3` should be there immediately!

---

## 🏗 Advanced Orchestration (Workspace)

Open WebUI has a **Workspace** section where you can discover:
- **Models**: Create "ModelFiles" (similar to personas).
- **Functions**: Import Python scripts that can act as orchestrators.
- **Tools**: Connect your model to external scripts.

> [!TIP]
> Use Open WebUI when you want the **fastest** and most **stable** connection to Ollama, with the option to write code-based orchestration later.
