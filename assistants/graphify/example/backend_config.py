"""
Backend configurations for the Mini-RAG system.
Defines connection parameters for Ollama and other local services.
"""

OLLAMA_CONFIG = {
    "host": "http://localhost:11434",
    "model": "llama3",
    "embedding_model": "nomic-embed-text"
}

NEO4J_CONFIG = {
    "uri": "bolt://localhost:7687",
    "user": "neo4j",
    "password": "password"
}
