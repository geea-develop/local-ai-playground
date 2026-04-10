# 🚀 FlowiseAI Getting Started: Local RAG

This guide documents the "Golden Path" for setting up a fully private, local Retrieval-Augmented Generation (RAG) system using Flowise and Ollama. This setup was successfully validated in the POC phase.

---

## 🛠 1. Backend Requirements (Ollama)

Before starting the flow, ensure your local Ollama server has the following models pulled:

```bash
# Main Chat & Logic Model
ollama pull mistral:v0.3

# Specialized Embedding Model (Required for RAG)
ollama pull nomic-embed-text
```

---

## 📐 2. The "Knowledge Base" Flow Architecture

To chat with your local documents, build your Chatflow using the following node configuration:

### A. The Engine
- **Chain:** `Conversational Retrieval QA Chain`
- **Chat Model:** `Ollama` 
  - Base URL: `http://host.docker.internal:11434`
  - Model: `mistral:v0.3`

### B. The Memory & Retrieval
- **Vector Store:** `In-Memory Vector Store`
- **Embeddings:** `Ollama Embeddings`
  - Base URL: `http://host.docker.internal:11434`
  - Model: `nomic-embed-text`

### C. The Data Ingestion
- **Document Loader:** `File Loader` (PDF, Text, or Docx)
- **Text Splitter:** `Recursive Character Text Splitter`
  - Chunk Size: `1000`
  - Chunk Overlap: `200`

---

## 🔗 3. Wiring Diagram

1. Connect **Ollama (Chat)** $\rightarrow$ **Conversational Retrieval QA Chain** (`Chat Model` input).
2. Connect **Ollama (Embeddings)** $\rightarrow$ **In-Memory Vector Store** (`Embeddings` input).
3. Connect **File Loader** $\rightarrow$ **In-Memory Vector Store** (`Document` input).
4. Connect **In-Memory Vector Store** $\rightarrow$ **Conversational Retrieval QA Chain** (`Vector Store Retriever` input).
5. Connect **Text Splitter** $\rightarrow$ **File Loader** (`Text Splitter` input).

---

## 🧪 4. Testing the POC

1. **Save** the Chatflow.
2. **Upload** a document in the `File Loader` node.
3. Open the **Chat Settings** and ensure the flow is using the `Conversational Retrieval QA Chain`.
4. Ask: *"What are the key points of the document I just uploaded?"*

> [!TIP]
> **Performance Tip:** If the response is slow, check Docker Desktop's CPU/Memory usage. Ensure at least 8GB of RAM is allocated to Docker for the orchestrated services.

---

## 📌 Maintenance Notes
- **Persistence:** Since this uses the `In-Memory Vector Store`, the knowledge index is cleared whenever the Docker container restarts. For permanent storage, consider switching to `ChromaDB` or `Pinecone`.
- **Base URL:** Always use `http://host.docker.internal:11434` inside Docker to talk to your Mac's Ollama instance.
