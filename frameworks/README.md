# 🧪 Agentic Frameworks & SDKs

This directory contains Python-based frameworks used to build autonomous workflows, RAG pipelines, and semantic memory systems — all running locally against the backends defined in [`/backends`](../backends).

---

## 🗂️ Contents

| Framework | Type | Key Capability | Primary Example |
|---|---|---|---|
| **[langchain/](./langchain)** | SDK | Chains, RAG, local model routing | `ollama_rag_chat_example.py` |
| **[langgraph/](./langgraph)** | Stateful Graphs | Cyclic graphs, persistence, human-in-loop | `ollama_example.py` |
| **[smolagents/](./smolagents)** | Lightweight Agents | Multi-backend agent loops | `ollama_rag_example.py` |
| **[deepagents/](./deepagents)** | Autonomous Agents | Long-horizon planning, subagent delegation | `ollama_example.py` |
| **[cognee/](./cognee)** | Semantic Memory | Knowledge graphs + vector DB memory layer | `ollama_memory_example.py` |
| **[docling/](./docling)** | Document Processing | PDF/DOCX → Markdown/JSON for RAG ingest | `convert_document_example.py` |

---

## 🏗️ Framework Overview

### 🔗 LangChain
The foundational SDK for building LLM-powered applications. Used throughout this playground for RAG chains, document loaders, embeddings, and local model connections (Ollama, llama.cpp, MLX).

- **Best for:** Pipelines, RAG, custom chains
- **Setup:** [`langchain/README.md`](./langchain/README.md)

### 📊 LangGraph
Extends LangChain with support for **cyclic, stateful graphs**. Essential for agentic workflows where the agent needs to loop, branch, or wait for human input.

- **Best for:** Multi-step agents, human-in-the-loop flows
- **Setup:** [`langgraph/README.md`](./langgraph/README.md)

### 🤗 smolagents
HuggingFace's lightweight agent library. Designed for simplicity and cross-backend portability — works with Ollama, llama.cpp, LM Studio, and MLX.

- **Best for:** Quick agent experiments, local RAG with PDF
- **Setup:** [`smolagents/README.md`](./smolagents/README.md)

### 🕵️ DeepAgents
An autonomous agent harness built on LangGraph. Provides built-in planning, a virtual filesystem, and subagent delegation for complex, long-running tasks.

- **Best for:** Complex autonomous tasks, multi-agent systems
- **Setup:** [`deepagents/README.md`](./deepagents/README.md)

### 🧬 Cognee
A semantic memory framework that goes beyond basic RAG by combining **Knowledge Graphs** with vector databases. Implements a "learn once, recall always" memory pattern for AI agents.

- **Best for:** Persistent agent memory, relationship-aware retrieval
- **Setup:** [`cognee/README.md`](./cognee/README.md)

> [!WARNING]
> Cognee requires Python 3.10–3.13. Ensure your virtual environment uses a compatible version.

### 📄 Docling
A powerful document conversion tool that transforms PDFs, DOCX, HTML, and PPTX into structured Markdown or JSON. The ideal pre-processing step for RAG pipelines.

- **Best for:** Document ingestion, table extraction, RAG preparation
- **Setup:** [`docling/README.md`](./docling/README.md)

---

## 🚀 Recommended Setup Pattern

Each framework uses a **self-contained virtual environment**:

```bash
# 1. Enter the framework directory
cd frameworks/<framework_name>

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your local settings (Ollama URL, model names, etc.)

# 5. Run an example
python <example_name>.py
```

> [!TIP]
> All examples default to **Ollama** as the backend. Ensure Ollama is running before executing any example: `ollama serve`
