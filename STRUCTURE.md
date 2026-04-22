# STRUCTURE — Local AI Playground

> **Last updated:** 2026-04-21

This document describes the top-level organization of the `local_ai_playground` repository. For a detailed visual map with component status tables, see **[docs/WORKSPACE_MAP.md](./docs/WORKSPACE_MAP.md)**.

---

## Top-Level Files

| File | Description |
|---|---|
| `README.md` | Primary landing page with quick-start and architecture overview |
| `STRUCTURE.md` | This file — directory layout and naming conventions |
| `CHANGELOG.md` | Chronological log of all notable changes |
| `LICENSE.md` | Apache 2.0 license |
| `.github/` | GitHub Actions workflows and Dependabot configuration |
| `.gitignore` | Git ignore rules |
| `.gooseignore` | Goose agent ignore rules |
| `.vscode/` | VS Code workspace settings |

---

## Top-Level Directories (Five Pillars)

### `/backends/`
Inference engines and model servers. These are responsible for running LLMs locally and exposing APIs to the rest of the stack.

- `ollama/` — Ollama configuration, model management, and usage guides
- `localai/` — LocalAI API emulation for multi-model serving
- `llm_runner/` — High-performance inference orchestration helpers
- `custom_servers/` — Apple Silicon-optimized servers (MLX-LM, mlx-openai, llama-cpp, LM Studio, vLLM, Ollama wrapper, debug)

### `/interfaces/`
Dashboards, chat UIs, and orchestration platforms. These connect to backends via API and provide user-facing capabilities.

- `open_webui/` — Primary daily-driver chat interface (Ollama-native)
- `flowise/` — Visual node-based agent orchestration (primary orchestrator)
- `dify/` — GenAI app deployment platform (secondary platform)
- `khoj/` — Personal AI aggregator / second-brain (solves Manual Ingestion Syndrome)
- `onyx/` — Enterprise search & RAG across 50+ data sources
- `lobe_chat/` — Premium chat client with agent personas
- `anything_llm/` — Workspace-based document RAG (evaluated)

### `/frameworks/`
Agentic SDKs and Python libraries used to build autonomous workflows, RAG pipelines, and semantic memory systems.

- `langchain/` — LangChain with MLX, llama.cpp, Ollama, and RAG examples
- `langgraph/` — Stateful multi-actor graphs built on LangChain
- `smolagents/` — HuggingFace smolagents with multi-backend support
- `deepagents/` — Autonomous long-running agent harness (built on LangGraph)
- `cognee/` — Semantic memory layer and knowledge graphs for AI agents
- `docling/` — Document conversion (PDF, DOCX, HTML → Markdown/JSON)

### `/assistants/`
Pre-built AI coding companions and specialized developer tools.

- `goose/` — Goose open-source AI agent configuration and documentation
- `claude/` — Claude agent integrations
  - `claude-cli/` — Claude CLI custom skills and plugins
  - `claude-lm-studio/` — Claude connected to local LM Studio inference
- `graphify/` — Codebase knowledge graph tool (AST extraction, graph querying)
- `gemini-cli/` — Gemini CLI integration *(in progress)*
- `opencode/` — Opencode AI coding assistant *(in progress)*
- `github-copilot-cli/` — GitHub Copilot CLI *(in progress)*

### `/docs/`
Ecosystem documentation, architectural blueprints, and guides.

- `DASHBOARD.md` — Unified Local AI Control Center architectural blueprint
- `WORKSPACE_MAP.md` — Full structural map with Mermaid diagrams and component status
- `GOOSE.md` — Goose assistant quick-start guide
- `LOCAL.md` — Notes on local development setup

---

## Naming Conventions

| Convention | Example |
|---|---|
| Directories use `snake_case` | `open_webui/`, `llm_runner/` |
| Hyphenated names for server/CLI tools | `llama-cpp-server/`, `claude-cli/` |
| Environment config files | `.env` (local secrets), `.env.example` (committed template) |
| Per-directory README | Every tool directory contains a `README.md` |
| Guides use SCREAMING_SNAKE_CASE | `GETTING_STARTED.md`, `INSTALL_GUIDE.md` |
