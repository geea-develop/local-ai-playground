# LangGraph
 
[LangGraph](https://langchain-ai.github.io/langgraph/) is a library for building stateful, multi-actor applications with LLMs. It is built on top of [LangChain](https://github.com/langchain-ai/langchain) and is designed to create complex agentic workflows with cycles, persistence, and human-in-the-loop capabilities.

## Key Features

- **Cycles & Recursion**: Unlike basic chains, LangGraph allows for cyclic graphs, which are essential for many agentic patterns.
- **Persistence**: Built-in support for saving and loading the state of your graph, allowing for long-running conversations.
- **Human-in-the-Loop**: Easily pause the graph and wait for human approval or input.
- **Streaming**: First-class support for streaming outputs from each node in the graph.

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

- **[ollama_example.py](./ollama_example.py)**: A simple graph using Ollama to process user input through a reasoning node.
