# DeepAgents
 
[DeepAgents](https://github.com/langchain-ai/deepagents) is an open-source "agent harness" designed to build autonomous, long-running, and complex AI agents. It is built on top of LangChain and LangGraph, providing a robust architecture for agents that can handle long-horizon tasks.

## Key Features

- **Built-in Planning**: Encourages agents to decompose complex problems into subtasks.
- **Virtual Filesystem**: Provides a way for agents to manage large amounts of data without cluttering the context window.
- **Stateful Execution**: Leverages LangGraph for persistence and durable execution.
- **Subagent Delegation**: Allows complex agents to spawn specialized subagents for specific tasks.

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
   # Edit .env with your local settings
   ```

## Examples

- **[ollama_example.py](./ollama_example.py)**: A basic deep agent implementation using Ollama.
