# 📂 AI Interfaces & Orchestration Platforms

This directory documents the research, tests, and configuration for evaluating open-source LLM interfaces and platforms. The goal is to establish a unified stack for local AI development with a focus on **Orchestration** and **RAG**.

---

## 🏆 Research Findings (Selection)

After evaluating multiple tools, the following conclusions were reached for the current project:

*   **Primary Orchestrator**: **FlowiseAI** (Selected for its superior balance of visibility, rapid node-based development, and granular control).
*   **Secondary Platform**: **Dify** (Selected for its professional app-deployment interface and robust built-in citation tracking).
*   **Best Chat Client**: **Open WebUI** (Selected for daily interaction and Ollama model management).

---

## 🛠 Evaluated Tools Summary

### 1. FlowiseAI (Verified Winner) ✅
- **Primary Use:** Visual, node-based orchestration for building complex agent chains.
- **Why it won:** Excellent visibility into the LangChain process.
- **Setup:** [GETTING_STARTED.md](./flowise/GETTING_STARTED.md)

### 2. Dify (Verified Platform) ✅
- **Primary Use:** A full-featured GenAI application platform for deploying multi-step autonomous agents.
- **Why use it:** Best-in-class UI for citations and RAG management.
- **Setup:** [GETTING_STARTED.md](./dify/GETTING_STARTED.md)

### 3. Open WebUI (Verified Interface) ✅
- **Primary Use:** Polished ChatGPT-style chat interface with Ollama model management.
- **Why use it:** Extremely stable and robust; the "Daily Driver" for local models.
- **Setup:** [GETTING_STARTED.md](./open_webui/GETTING_STARTED.md)

### 4. LobeChat (Verified Client) ✅
- **Primary Use:** Premium, sleek chat client focused on agent personas and local plugins.
- **Limitation:** Not suitable for complex logic/workflow orchestration.
- **Setup:** [GETTING_STARTED.md](./lobe_chat/GETTING_STARTED.md)

### 5. AnythingLLM (Document Research) 📂
- **Primary Use:** Workspace-based RAG and full-stack local document management.
- **Limitation:** Lacks the advanced agentic orchestration features found in Dify or Flowise.
- **Setup:** [INSTALL_GUIDE.md](./anything_llm/INSTALL_GUIDE.md)

---

## 🚀 Golden Stack Path
For a complete local experience, it is recommended to run **Ollama** as the backend, with **Flowise** as the logic engine and **Open WebUI** as the primary interactive portal.
