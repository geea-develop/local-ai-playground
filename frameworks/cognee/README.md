# Cognee Framework

[Cognee](https://github.com/topoteretes/cognee) is an open-source Python framework that implements a semantic memory layer for AI agents. It goes beyond basic RAG by utilizing **Knowledge Graphs** and **Vector Databases** to create a persistent, queryable memory system that understands relationships between entities.

> [!WARNING]
> **Python Version Compatibility**: Cognee currently requires **Python 3.10 to 3.13**. It does not officially support Python 3.14+ yet. Please ensure you use a compatible virtual environment.

## Features

- **Knowledge Graphs**: Automatically builds graphs from ingested data.
- **Persistent Memory**: Implements a "learn once, recall always" pattern.
- **Modular Storage**: Supports LanceDB, Qdrant, Neo4j, and more.
- **Local-First**: Works seamlessly with local backends like Ollama and local storage engines.
- **Cognify Pipeline**: A built-in ECL (Extract, Cognify, Load) pipeline for processing data.

## Getting Started

### 1. Set up Environment
```bash
# Create and activate virtual environment (Must be Python 3.10-3.13)
python3.13 -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Local LLM (Ollama)
Ensure Ollama is running and you have pulled the required models:
```bash
ollama pull llama3
ollama pull nomic-embed-text
```

### 3. Setup Environment Variables
```bash
cp .env.example .env
# Edit .env to match your local setup
```

## Examples

- `ollama_memory_example.py`: Demonstrates the core `remember`, `cognify`, and `search` loop using local Ollama models.

## Usage Example

```python
import cognee
import asyncio

async def main():
    # Store information
    await cognee.add("The capital of France is Paris.")
    
    # Process and build memory (Graph + Vector)
    await cognee.cognify()
    
    # Recall based on semantics and relationships
    results = await cognee.search("What is the capital of France?")
    print(results)

if __name__ == "__main__":
    asyncio.run(main())
```

## Resources
- [Official Repository](https://github.com/topoteretes/cognee)
- [Documentation](https://docs.cognee.ai/)
