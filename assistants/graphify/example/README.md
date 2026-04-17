# Mini-RAG Example Project

This is a sample project designed to demonstrate how **Graphify** indexes a multi-module Python application.

## 🏗 Structure

- `main.py`: The entry point that orchestrates the data flow.
- `src/`: Core logic modules.
  - `ingestor.py`: Fetches raw data (Web/File).
  - `processor.py`: Text cleaning and preparation.
  - `storage.py`: Persistence layer simulation.
- `backend_config.py`: Configuration for local AI backends like Ollama and Neo4j.

## 🔍 Try Graphify on this!

To see how Graphify maps the relationships between these modules, run the following from the root of the playground:

```bash
/graphify ./assistants/graphify/example
```

Graphify will extract:
1. **Dependencies**: `main.py` -> `src/storage.py`, etc.
2. **Concepts**: Links between "Storage" and "Neo4j" based on the `backend_config.py` definitions.
3. **Architecture**: A clear view of the Ingest-Process-Store pipeline.
