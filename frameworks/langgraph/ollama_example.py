import os
from typing import TypedDict, Annotated
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END

# Load environment variables
load_dotenv()

# Define the state schema
class State(TypedDict):
    input: str
    response: str
    thought: str

# Initialize the model
llm = ChatOllama(
    model=os.getenv("OLLAMA_MODEL", "llama3.2"),
    base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
)

def reason_node(state: State):
    """Reason about the input."""
    prompt = f"Think carefully about how to answer this: {state['input']}"
    response = llm.invoke(prompt)
    return {"thought": response.content}

def answer_node(state: State):
    """Provide the final answer."""
    prompt = f"Based on these thoughts: {state['thought']}, provide a concise answer to: {state['input']}"
    response = llm.invoke(prompt)
    return {"response": response.content}

# Build the graph
workflow = StateGraph(State)

workflow.add_node("reason", reason_node)
workflow.add_node("answer", answer_node)

workflow.add_edge(START, "reason")
workflow.add_edge("reason", "answer")
workflow.add_edge("answer", END)

# Compile the graph
app = workflow.compile()

def main():
    user_input = "What is the capital of France and why is it famous?"
    print(f"--- User Input ---\n{user_input}\n")
    
    # Run the graph
    for output in app.stream({"input": user_input}):
        for key, value in output.items():
            print(f"--- Node: {key} ---")
            print(f"{value}\n")

if __name__ == "__main__":
    main()
