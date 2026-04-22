"""
DeepAgents - Basic Example with Ollama (Local LLM)
===================================================
Demonstrates create_deep_agent with a locally-running Ollama model and a
custom tool. No internet or API key required.

Pre-requisites:
    ollama pull qwen2.5:7b   (or another model that supports tool-calling)

Requirements:
    pip install -r requirements.txt

Environment:
    OLLAMA_BASE_URL=http://localhost:11434
    OLLAMA_MODEL=qwen2.5:7b
"""

import os

from dotenv import load_dotenv
from langchain_ollama import ChatOllama

from deepagents import create_deep_agent

load_dotenv()

# ---------------------------------------------------------------------------
# Model – Ollama must be running locally
# ---------------------------------------------------------------------------
llm = ChatOllama(
    model=os.getenv("OLLAMA_MODEL", "qwen2.5:7b"),
    base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
)


# ---------------------------------------------------------------------------
# Custom tools – plain Python functions; docstrings become tool descriptions
# ---------------------------------------------------------------------------
def get_cpu_usage() -> str:
    """Return the current CPU usage percentage of the local machine."""
    try:
        import psutil  # noqa: PLC0415

        usage = psutil.cpu_percent(interval=0.5)
        return f"CPU usage: {usage}%"
    except ImportError:
        return "CPU usage: 23%  (psutil not installed – returning mock value)"


def get_memory_info() -> str:
    """Return total and available RAM on the local machine."""
    try:
        import psutil  # noqa: PLC0415

        vm = psutil.virtual_memory()
        return (
            f"Total RAM: {vm.total // (1024**3)} GB | "
            f"Available: {vm.available // (1024**3)} GB | "
            f"Used: {vm.percent}%"
        )
    except ImportError:
        return "Memory: 16 GB total, 8 GB available  (psutil not installed – returning mock value)"


# ---------------------------------------------------------------------------
# Agent
# ---------------------------------------------------------------------------
agent = create_deep_agent(
    model=llm,
    tools=[get_cpu_usage, get_memory_info],
    system_prompt=(
        "You are a local system monitor assistant. "
        "Use the provided tools to report on system resource usage. "
        "Be concise and present data in a clear format."
    ),
)


def main() -> None:
    query = "Check the current CPU usage and available memory for me."
    print(f"User: {query}\n")

    result = agent.invoke({"messages": [("user", query)]})
    final_message = result["messages"][-1]
    print(f"Agent: {final_message.content}")


if __name__ == "__main__":
    main()
