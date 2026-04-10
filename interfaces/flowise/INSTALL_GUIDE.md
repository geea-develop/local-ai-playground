# 🌊 FlowiseAI POC Setup Guide

Flowise is a low-code tool for building customized LLM orchestration flows using LangChain. It is particularly powerful for visual-first developers who want to see how data moves between prompts, models, and tools.

---

## 🛠 Prerequisites

- **Docker Desktop**
- **LM Studio** (or Ollama) running locally.

---

## 📦 Installation Steps

### 1. Prepare Environment
Ensure you have the `.env` file ready. By default, Flowise sits on port `3001`.
```bash
cd interfaces/flowise
mkdir -p data
```

### 2. Launch Flowise
```bash
docker compose up -d
```

### 3. Access the UI
Open your browser and navigate to: **[http://localhost:3001](http://localhost:3001)**

---

## 🧪 Testing with LM Studio (Simple Example)

Since you want a simple example that doesn't rely on embeddings, try the **Self-Critique Chain**:

1. **Dashboard**: Click **Add New** to create a blank Chatflow.
2. **Nodes**:
   - Add a **Chat LocalAI** node (this works for LM Studio).
     - **Base Path**: `http://host.docker.internal:1234/v1`
     - **Model Name**: (Use the name loaded in LM Studio, e.g., `luna-ai-llama2`)
   - Add a **Buffer Memory** node.
   - Add a **Conversation Chain** node.
3. **Connect**: Link the Model and Memory to the Conversation Chain.
4. **Chat**: Ask it to perform a task. 

> [!TIP]
> To get **Embeddings** working later:
> 1. Load `nomic-embed-text-v1.5` in LM Studio.
> 2. In Flowise, add a **LocalAI Embeddings** node.
> 3. Point it to the same `host.docker.internal:1234/v1` base path.
