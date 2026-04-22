# DeepAgents

[DeepAgents](https://github.com/langchain-ai/deepagents) is an open-source "agent harness" designed to build autonomous, long-running, and complex AI agents. It is built on top of LangChain and LangGraph, providing a robust architecture for agents that can handle long-horizon tasks.

## Key Features

- **Built-in Planning**: Encourages agents to decompose complex problems into subtasks.
- **Virtual Filesystem**: Provides a way for agents to manage large amounts of data without cluttering the context window.
- **Stateful Execution**: Leverages LangGraph for persistence and durable execution.
- **Subagent Delegation**: Allows complex agents to spawn specialized subagents for specific tasks.
- **Middleware Architecture**: Intercepts requests to inject context, manage memory, and filter tools.

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your Google API Key or Ollama settings
   ```

## Examples

### ☁️ Cloud (Google Gemini)
- **[gemini_basic_example.py](./gemini_basic_example.py)**: Simple tool-calling agent using Gemini Flash.
- **[gemini_subagents_example.py](./gemini_subagents_example.py)**: Orchestrator-worker pattern using multiple subagents (Researcher + Writer).
- **[gemini_memory_example.py](./gemini_memory_example.py)**: Persistent memory using `MemoryMiddleware` and `FilesystemBackend` to remember user preferences across runs.

### 🏠 Local (Ollama)
- **[ollama_example.py](./ollama_example.py)**: Basic deep agent implementation using local Ollama models (e.g., Qwen 2.5) for system monitoring.
