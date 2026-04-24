"""
DeepAgents - Basic Example with AWS Bedrock
===========================================
Demonstrates the simplest use of create_deep_agent with an AWS Bedrock model
and a custom tool.

DeepAgents gives the agent a built-in suite of tools by default:
  - write_todos, read_file, write_file, edit_file, ls, glob, grep, execute
  - task (for spawning subagents)

You can extend this with your own tools via the `tools=` parameter.

Requirements:
    pip install -r requirements.txt

Environment:
    AWS_ACCESS_KEY_ID=<your-id>
    AWS_SECRET_ACCESS_KEY=<your-secret>
    AWS_REGION=<your-region>
    BEDROCK_MODEL_ID=us.amazon.nova-pro-v1:0  # or anthropic.claude-3-5-sonnet-20240620-v1:0
"""

import os

from dotenv import load_dotenv
from langchain_aws import ChatBedrockConverse

from deepagents import create_deep_agent

load_dotenv()

# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------
# We use ChatBedrockConverse for modern tool-calling support.
# Note: Ensure the model is enabled in your AWS Console for the chosen region.
# Common IDs for eu-west-1: anthropic.claude-3-5-sonnet-20240620-v1:0
# Common IDs for us-east-1: us.amazon.nova-pro-v1:0, anthropic.claude-3-5-sonnet-20240620-v1:0
model_id = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20240620-v1:0")
region = os.getenv("AWS_REGION", "us-east-1")

print(f"Using Bedrock Model: {model_id} in {region}")

llm = ChatBedrockConverse(
    model_id=model_id,
    region_name=region,
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
