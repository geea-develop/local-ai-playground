# 🌐 Open WebUI Getting Started: The Daily Driver

Open WebUI is the most robust and popular interface for local LLM users. It provides a ChatGPT-like experience with deep integration for Ollama and support for powerful Python-based "Functions."

---

## 🛠 1. Prerequisites (Ollama)

Ensure your local Ollama server is running. Open WebUI automatically detects all models available in your Ollama instance.

```bash
ollama pull mistral:v0.3
```

---

## 🏗 2. Launching Open WebUI

Navigate to the directory and start the container. It maps port `3000` on your Mac to port `8080` inside the container.

```bash
cd interfaces/open_webui
mkdir -p data
docker compose up -d
```

---

## ⚙️ 3. Initial Configuration

1.  **Go to**: **[http://localhost:3000](http://localhost:3000)**.
2.  **Admin Account**: Sign up with any email/password. The first user created is automatically the Administrator.
3.  **Connection**: Open WebUI should auto-detect Ollama via the `host.docker.internal:11434` bridge set in the `docker-compose.yml`.
4.  **Verification**: Click the model selector at the top; your `mistral:v0.3` should appear.

---

## 🚀 Key Features to Explore

### A. ModelFiles (Custom Personas)
You can create "ModelFiles" in the **Workspace** section. These are similar to Dify personas—they allow you to "bottle" a specific system prompt, temperature, and toolset into a single selectable model name.

### B. RAG (Documents)
- Click the **+** (Plus) icon in the chat input.
- Upload a file.
- Open WebUI handles the chunking and embedding (via its internal engine or your local Ollama embeddings).

### C. Functions & Actions
In the **Workspace** $\rightarrow$ **Functions** section, you can discover or write Python scripts that can:
- Intercept messages.
- Add external tool data.
- Automate complex responses.

---

## 📌 Maintenance Notes
- **Persistence:** All chat history and documents are saved in the `interfaces/open_webui/data` folder on your Mac.
- **Updates:** To update Open WebUI, run `docker compose pull && docker compose up -d`.
