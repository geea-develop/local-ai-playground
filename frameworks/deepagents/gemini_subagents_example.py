"""
DeepAgents - Multi-Subagent Orchestration with Google Gemini
=============================================================
Demonstrates how to build an orchestrator + specialist subagents pattern:

  Orchestrator (Gemini Flash)
    ├── researcher   – fetches & summarises web-like data
    └── writer       – turns research into polished prose

The orchestrator delegates tasks via the built-in `task` tool.
Each SubAgent is a TypedDict with at least {name, description, system_prompt}.

Requirements:
    pip install -r requirements.txt

Environment:
    GOOGLE_API_KEY=<your-key>   # already in .env
"""

import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from deepagents import SubAgent, create_deep_agent

load_dotenv()

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


def make_llm(model: str = GEMINI_MODEL) -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(model=model, google_api_key=GOOGLE_API_KEY)


# ---------------------------------------------------------------------------
# Shared tools available to all agents
# ---------------------------------------------------------------------------
def search_topic(topic: str) -> str:
    """Simulate a knowledge-base lookup for a given topic. Returns raw facts."""
    facts = {
        "quantum computing": (
            "Quantum computers use qubits that exploit superposition and entanglement. "
            "Google's Willow chip (2024) reached 105 physical qubits with below-threshold "
            "error correction. IBM's roadmap targets 100k+ qubits by 2033."
        ),
        "large language models": (
            "LLMs are transformer-based models trained on internet-scale text. "
            "Key milestones: GPT-4 (OpenAI, 2023), Gemini Ultra (Google, 2024), "
            "Claude 3 (Anthropic, 2024). Scaling laws suggest performance improves "
            "predictably with compute, data, and parameters."
        ),
        "renewable energy": (
            "Solar PV costs fell 90 % over the last decade. Wind + solar provided "
            "~12 % of global electricity in 2023. Battery storage capacity is growing "
            "at ~30 % CAGR. Key challenge: grid stability with variable generation."
        ),
    }
    key = topic.lower().strip()
    return facts.get(key, f"No data found for topic: '{topic}'. Try a different query.")


# ---------------------------------------------------------------------------
# Subagent specs
# ---------------------------------------------------------------------------
researcher: SubAgent = {
    "name": "researcher",
    "description": (
        "Specialist research agent. Use this to look up technical or factual information "
        "on a topic and return a structured summary of key findings."
    ),
    "system_prompt": (
        "You are a meticulous research analyst. When given a topic:\n"
        "1. Use the `search_topic` tool to gather raw facts.\n"
        "2. Organise findings into bullet points: Background, Key Facts, Trends.\n"
        "3. Be concise but thorough. Return ONLY the structured notes."
    ),
    "model": make_llm(),
    "tools": [search_topic],
}

writer: SubAgent = {
    "name": "writer",
    "description": (
        "Specialist writing agent. Use this to turn raw research notes into a polished, "
        "well-structured paragraph or short article suitable for a general audience."
    ),
    "system_prompt": (
        "You are a skilled science communicator. You receive structured research notes "
        "and must produce clear, engaging prose. Do NOT use jargon without explaining it. "
        "Keep the output under 200 words unless asked for more."
    ),
    "model": make_llm(),
    "tools": [],  # writer needs no tools – it works only with text
}

# ---------------------------------------------------------------------------
# Orchestrator agent
# ---------------------------------------------------------------------------
orchestrator = create_deep_agent(
    model=make_llm(),
    tools=[search_topic],          # also available directly to orchestrator
    subagents=[researcher, writer],
    system_prompt=(
        "You are an AI content production orchestrator.\n"
        "For research-heavy requests:\n"
        "  1. Delegate research to the 'researcher' subagent.\n"
        "  2. Pass the notes to the 'writer' subagent to produce final prose.\n"
        "  3. Return the polished output to the user."
    ),
)


def main() -> None:
    query = (
        "Write a short, accessible explainer about quantum computing "
        "for a non-technical blog audience."
    )
    print(f"User: {query}\n")
    print("Orchestrator is running (may invoke researcher → writer)...\n")

    result = orchestrator.invoke({"messages": [("user", query)]})
    final = result["messages"][-1].content
    print(f"Final output:\n{'-' * 60}\n{final}")


if __name__ == "__main__":
    main()
