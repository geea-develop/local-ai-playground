"""
DeepAgents - Basic Example with Google Gemini
==============================================
Demonstrates the simplest use of create_deep_agent with a Gemini model
and a custom tool.

DeepAgents gives the agent a built-in suite of tools by default:
  - write_todos, read_file, write_file, edit_file, ls, glob, grep, execute
  - task (for spawning subagents)

You can extend this with your own tools via the `tools=` parameter.

Requirements:
    pip install -r requirements.txt

Environment:
    GOOGLE_API_KEY=<your-key>   # already in .env
"""

import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from deepagents import create_deep_agent

load_dotenv()

# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------
# We use gemini-3-flash-preview as it's the current state-of-the-art in this environment
llm = ChatGoogleGenerativeAI(
    model=os.getenv("GEMINI_MODEL", "gemini-3-flash-preview"),
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)


# ---------------------------------------------------------------------------
# Custom tool – plain Python function; docstring becomes tool description
# ---------------------------------------------------------------------------
def get_weather(city: str) -> str:
    """Return a simulated weather report for the given city."""
    weather_db = {
        "tel aviv": "☀️  Sunny, 28 °C, light sea breeze.",
        "london": "🌧️  Overcast with light rain, 14 °C.",
        "new york": "⛅  Partly cloudy, 22 °C, moderate wind.",
        "tokyo": "🌸  Clear sky, 19 °C, pleasant.",
    }
    return weather_db.get(city.lower(), f"No weather data available for '{city}'.")


# ---------------------------------------------------------------------------
# Agent
# ---------------------------------------------------------------------------
agent = create_deep_agent(
    model=llm,
    tools=[get_weather],
    system_prompt="You are a friendly travel assistant. Use the weather tool to answer questions.",
)


def main() -> None:
    query = "What's the weather like in Tel Aviv and Tokyo right now?"
    print(f"User: {query}\n")

    result = agent.invoke({"messages": [("user", query)]})

    # Extract text from the last AI message
    for message in reversed(result["messages"]):
        if message.type == "ai" and message.content:
            content = message.content
            # Handle list of content blocks (common in newer models)
            if isinstance(content, list):
                text_parts = [block.get("text", "") for block in content if isinstance(block, dict) and block.get("type") == "text"]
                text_content = " ".join(text_parts).strip()
                if text_content:
                    print(f"Agent: {text_content}")
                    return
            # Handle string content
            elif isinstance(content, str) and content.strip():
                print(f"Agent: {content.strip()}")
                return
    
    # Fallback if no text found
    last_msg = result["messages"][-1]
    print(f"Agent: (No text response found. Last message type: {last_msg.type})")


if __name__ == "__main__":
    main()
