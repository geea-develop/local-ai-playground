import os
from dotenv import load_dotenv
from deepagents import create_deep_agent
from langchain_ollama import ChatOllama

# Load environment variables
load_dotenv()

# Initialize the model
llm = ChatOllama(
    model=os.getenv("OLLAMA_MODEL", "llama3.2"),
    base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
)

def get_system_stat(stat_type: str) -> str:
    """Get a simulated system statistic."""
    if stat_type == "cpu":
        return "CPU Usage: 15%"
    elif stat_type == "memory":
        return "Memory Available: 8GB"
    return "Unknown statistic."

def main():
    # Initialize the deep agent
    agent = create_deep_agent(
        model=llm,
        tools=[get_system_stat],
        system_prompt="You are a helpful system monitor. Use tools to answer user queries about the system."
    )

    user_input = "Check the CPU usage and memory status for me."
    print(f"--- User Input ---\n{user_input}\n")

    # Run the agent
    # Note: DeepAgents typically returns a LangGraph app or similar
    # Using a simple sync invocation for example purposes
    response = agent.invoke({"messages": [("user", user_input)]})
    
    print("--- Agent Response ---")
    print(response["messages"][-1].content)

if __name__ == "__main__":
    main()
