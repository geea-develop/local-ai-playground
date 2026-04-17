# Design Document: Mini-RAG System

## Overview
This system is designed to provide a local-first RAG (Retrieval-Augmented Generation) pipeline. It leverages **Ollama** for embeddings and LLM generation.

## Components
1. **Ingestor**: Fetches content. It is designed to be extensible for different protocols.
2. **Processor**: Performs text normalization.
3. **Storage**: Currently mocks a database connection. Future versions will integrate with **ChromaDB** or **Neo4j**.

## Key Relationships
The `main.py` controller manages the lifecycle of shared state between the `Processor` and `Storage` components.
