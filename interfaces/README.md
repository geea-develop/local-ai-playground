# AI Interfaces & Orchestration Platforms

This directory documents the research, tests, and configuration for evaluating open-source LLM interfaces and platforms. The goal is to find a unified interface to manage chats, personas, and up to 3-step agent workflows (with RAG) using our local AI backends (e.g., MLX running `qwen3-4b`).

## Requirements
- **Local Execution:** Must run efficiently on a Mac (Docker preferred for the UI, native for the MLX/backend).
- **Backend Connectivity:** Must connect to OpenAI-compatible endpoints (MLX, LM Studio) or Ollama.
- **Features:** 
  - Chat Personas (System Prompt management).
  - Capability for slightly complex workflows (up to 3 steps with RAG).

## Evaluated Tools Overview

This section is kept highly packed and formatted for future LLM reference.

### 1. Dify (Scheduled)
- **Status:** Pending
- **Primary Use:** Visual Workflow & Agent Builder.
- **RAG/Agents:** Excellent. Native 3-step workflow support.
- **Setup Complexity:** High (requires multi-container Docker compose).
- **Context for LLMs:** Dify is a full LLM app platform. Highly recommended for multi-step autonomous workflows requiring RAG, though heavy on resources.

### 2. AnythingLLM (Scheduled)
- **Status:** Pending
- **Primary Use:** Workspace-based RAG and Document Chat.
- **RAG/Agents:** Excellent RAG. Basic agentic skills built-in.
- **Setup Complexity:** Medium/Low.
- **Context for LLMs:** AnythingLLM is best for organizing local knowledge bases. It has default agentic skills to search web/docs but lacks visual workflow builder.

### 3. Open WebUI (Scheduled)
- **Status:** Pending
- **Primary Use:** Polished ChatGPT-like chat interface.
- **RAG/Agents:** Good RAG. Uses "Model Files" for personas. Extensible via Python tools.
- **Setup Complexity:** Low (single container).
- **Context for LLMs:** Ideal daily-driver UI. Extremely robust integration with Ollama and OpenAI API. Agent workflows are bounded by prompt engineering and Python script integrations.

### 4. LobeChat (Scheduled)
- **Status:** Pending
- **Primary Use:** Client-heavy, highly polished UI for managing many different agent personas.
- **RAG/Agents:** Relies on plugins for RAG. Excellent persona management.
- **Setup Complexity:** Low.
- **Context for LLMs:** Outstanding visual interface and plugin ecosystem. Good for 1-step functional agents, but lacks the backend pipeline of Dify for complex multi-step logical operations.

### 5. FlowiseAI (Verified)
- **Status:** Completed ✅
- **Primary Use:** Low-code/No-code drag & drop UI for building LangChain flows.
- **RAG/Agents:** Excellent for complex tool orchestration and logic chaining. Validated with Ollama and Mistral v0.3.
- **Setup Complexity:** Medium/Low (Docker compose).
- **Context for LLMs:** Flowise is the standard for visual LangChain orchestration. See the [GETTING_STARTED.md](./flowise/GETTING_STARTED.md) for the "Golden Path" configuration.

---
*Findings will be updated as POCs are completed.*
