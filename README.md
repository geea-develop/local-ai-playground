# 🚀 Local AI Playground

Welcome to the **Local AI Playground**! This repository is a curated collection of local AI backends, graphical interfaces, agentic frameworks, and developer assistants. It serves as a unified environment for experimenting with, developing, and deploying AI models—all running locally on your hardware.

---

## 🏗️ Project Architecture

The project is organized into five logical pillars to ensure clarity and scalability as the local AI ecosystem evolves:

| Pillar | Description | Key Components |
| :--- | :--- | :--- |
| **[`/backends`](./backends)** | Inference engines & model servers | Ollama, LM Studio, MLX, LocalAI |
| **[`/interfaces`](./interfaces)** | Dashboards & Orchestration | Open WebUI, Dify, Onyx, FlowiseAI |
| **[`/frameworks`](./frameworks)** | Agentic SDKs & Libraries | LangChain, LangGraph, DeepAgents, smolagents |
| **[`/assistants`](./assistants)** | AI Coding Companions | Goose, Claude CLI |
| **[`/docs`](./docs)** | Ecosystem Documentation | Architecture Blueprints, Cheat Sheets |

For a detailed breakdown of the terminology and organization, see **[STRUCTURE.md](./STRUCTURE.md)**.

---

## 🎯 Quick Start

1.  **Select a Backend**: Navigate to [`backends/`](./backends) and launch your preferred inference engine (e.g., Ollama or MLX).
2.  **Launch an Interface**: Choose a UI in [`interfaces/`](./interfaces) (e.g., Open WebUI) and connect it to your backend's API.
3.  **Explore Agents**: Dive into [`frameworks/`](./frameworks) to build autonomous workflows or use [`assistants/`](./assistants) for AI-powered development.

---

## 🛣️ Roadmap: The Unified Dashboard

Our vision is to consolidate these isolated tools into a unified **Local AI Control Center**. We are currently moving towards using **Open WebUI** as the primary orchestration layer to manage chats, RAG, and multi-agent systems across all local backends.

> [!TIP]
> Check out the **[Architectural Blueprint](./docs/DASHBOARD.md)** to see how we're unifying the experience.

---

## 📜 Recent Updates

- **[2026-04-12]**: Integrated **LangGraph**, **DeepAgents**, and **Onyx** (Enterprise Search) to the ecosystem.
- **[2026-04-10]**: Refactored project structure to include a dedicated `docs/` directory and modernized the main entry point.
- **[2026-04-08]**: Initialized `smolagents` playground with cross-backend support.
- **[2026-04-07]**: Standardized audit trails across all READMEs.

*Full history available in [CHANGELOG.md](./CHANGELOG.md).*

---

> [!NOTE]  
> This project is optimized for performance on **Apple Silicon** (M-series), leveraging MLX and native inference where possible.

