"""
DeepAgents - Persistent Memory with Google Gemini
==================================================
Demonstrates MemoryMiddleware with a FilesystemBackend so the agent can:
  1. Load context from an AGENTS.md file at startup.
  2. Write new learnings back to that file using the built-in `edit_file` tool.

This pattern is great for assistants that should remember user preferences,
project conventions, or recurring facts across sessions.

Directory layout after first run:
    .local/
        AGENTS.md           ← memory file (auto-created if missing)

Requirements:
    pip install -r requirements.txt

Environment:
    GOOGLE_API_KEY=<your-key>   # already in .env

Usage:
    python gemini_memory_example.py
    # Then ask it to remember something, e.g.:
    #   "Remember that I prefer metric units."
    # On the next run it will already know that preference.
"""

import os
import textwrap
from pathlib import Path

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from deepagents import MemoryMiddleware, create_deep_agent
from deepagents.backends import FilesystemBackend

load_dotenv()

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
HERE = Path(__file__).parent
LOCAL_DIR = HERE / ".local"
LOCAL_DIR.mkdir(exist_ok=True)

MEMORY_FILE = LOCAL_DIR / "AGENTS.md"

# Seed the memory file with initial project context if it doesn't exist
if not MEMORY_FILE.exists():
    MEMORY_FILE.write_text(
        textwrap.dedent("""\
        # Agent Memory

        ## User Preferences
        (No preferences saved yet.)

        ## Project Context
        This is the local_ai_playground project — a Python workspace for evaluating
        local and cloud AI frameworks (LangChain, LangGraph, DeepAgents, Smolagents, …).
        """),
        encoding="utf-8",
    )

# ---------------------------------------------------------------------------
# Backend – FilesystemBackend roots the agent in a real directory
# ---------------------------------------------------------------------------
backend = FilesystemBackend(root_dir=str(HERE))

# ---------------------------------------------------------------------------
# Memory middleware
# ---------------------------------------------------------------------------
memory = MemoryMiddleware(
    backend=backend,
    sources=[".local/AGENTS.md"],   # path is relative to backend root_dir
)

# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------
llm = ChatGoogleGenerativeAI(
    model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)

# ---------------------------------------------------------------------------
# Agent
# ---------------------------------------------------------------------------
agent = create_deep_agent(
    model=llm,
    middleware=[memory],
    system_prompt=(
        "You are a persistent personal assistant with access to a memory file. "
        "When the user asks you to remember something, update `.local/AGENTS.md` "
        "using the `edit_file` tool BEFORE replying."
    ),
    backend=backend,
)


def chat(query: str) -> str:
    """Send a single message and return the agent's reply."""
    result = agent.invoke({"messages": [("user", query)]})
    return result["messages"][-1].content


def main() -> None:
    print("DeepAgents Memory Example (type 'quit' to exit)\n")
    print(f"Memory file: {MEMORY_FILE}\n")

    # Two-turn demo showing memory persistence within a session
    turns = [
        "What do you know about this project?",
        "Please remember that I prefer concise bullet-point answers.",
    ]

    for query in turns:
        print(f"User: {query}")
        reply = chat(query)
        print(f"Agent: {reply}\n")

    print("(Run again to see the agent recall the saved preference.)")


if __name__ == "__main__":
    main()
