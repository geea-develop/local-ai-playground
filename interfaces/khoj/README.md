# 🔦 Khoj (The 'Second Brain' Aggregator)

Khoj is a personal AI assistant that allows you to search, chat, and reason over your personal knowledge base (Obsidian, Notion, GitHub, and local files). It is specifically evaluated here as a solution for **'Manual Ingestion Syndrome'**.

## 🚀 Quick Start (POC)

To run Khoj locally as a Docker-based interface:

1.  Ensure **Ollama** is running on your host machine.
2.  Setup environment variables (optional for local defaults):
    ```bash
    cp .env.example .env
    ```
3.  Start the Khoj stack:
    ```bash
    docker-compose up -d
    ```
3.  Access the web interface at [http://localhost:42110](http://localhost:42110).
4.  Configure your **Content Sources** (Notion, GitHub) in the settings.

## 🧠 Why Khoj?

Unlike AnythingLLM, which uses a Workspace-centric architecture requiring manual uploads or distinct folder syncing, Khoj acts as a **Background Aggregator**. 

### Key Features
- **Obsidian Plugin:** Direct integration that indexes your vault as you type.
- **Incremental Indexing:** Efficiently updates only what has changed.
- **Headless Search:** Shortcut-based (`Cmd+Shift+K`) interface for system-wide lookup.
- **Agentic Capability:** Can run code in a sandbox and perform web searches via SearxNG.

## 📂 Documentation & Reports
- **[Full Evaluation Report](./REPORTS/EVALUATION.md):** Detailed comparison between Khoj and AnythingLLM.

## 🛠 Tech Stack (POC)
- **Database:** Postgres + pgvector
- **Sandbox:** Terrarium (Python Code Execution)
- **Search:** SearxNG
- **LLM Interaction:** Ollama (via Localhost API)
