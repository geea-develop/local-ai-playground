# 🦙 Ollama Backend

[Ollama](https://ollama.com) is the primary inference backend for this playground. It provides a simple CLI and REST API for downloading, managing, and running open-source LLMs locally — with native support for Apple Silicon via Metal acceleration.

---

## 🚀 Quick Start

### 1. Install Ollama

```bash
# macOS (recommended)
brew install ollama

# Or download from https://ollama.com/download
```

### 2. Start the Server

```bash
ollama serve
# Runs on http://localhost:11434 by default
```

### 3. Pull Models

```bash
# Recommended "Golden Path" models for this playground
ollama pull mistral:v0.3        # Best general-purpose local LLM
ollama pull llama3              # Meta's Llama 3
ollama pull nomic-embed-text    # Embedding model for RAG
ollama pull phi3                # Lightweight, fast model for tasks
```

### 4. Verify

```bash
ollama list       # Show downloaded models
ollama run mistral:v0.3   # Interactive chat session
```

---

## 📡 API Usage

Ollama exposes an **OpenAI-compatible REST API** at `http://localhost:11434/v1`, making it compatible with any OpenAI SDK client.

### Python (Native Ollama SDK)

```python
import ollama

response = ollama.chat(
    model='mistral:v0.3',
    messages=[{'role': 'user', 'content': 'Explain RAG in one paragraph.'}]
)
print(response['message']['content'])
```

### Python (OpenAI-compatible SDK)

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

response = client.chat.completions.create(
    model="mistral:v0.3",
    messages=[{"role": "user", "content": "Hello from the Ollama OpenAI API!"}]
)
print(response.choices[0].message.content)
```

### Streaming Response

```python
import ollama

for chunk in ollama.chat(
    model='mistral:v0.3',
    messages=[{'role': 'user', 'content': 'Write a haiku about local AI.'}],
    stream=True
):
    print(chunk['message']['content'], end='', flush=True)
```

---

## 🧩 Integration with This Playground

Ollama is the default backend for **all** frameworks and interfaces in this repo:

| Consumer | Configuration Key | Default Value |
|---|---|---|
| LangChain | `OLLAMA_BASE_URL` | `http://localhost:11434` |
| smolagents | `OLLAMA_API_BASE` | `http://localhost:11434` |
| LangGraph | `OLLAMA_BASE_URL` | `http://localhost:11434` |
| Cognee | `LLM_API_BASE` | `http://localhost:11434/v1` |
| Open WebUI | Configured in UI | `http://localhost:11434` |
| Khoj | `OLLAMA_HOST` | `http://localhost:11434` |

---

## 📦 Source Files

| File | Description |
|---|---|
| `src/` | Python utilities and Ollama client wrappers |
| `src/ollama_client.py` | Reusable client class with streaming and history support |
| `src/example.py` | Basic chat example using the client |

---

## 🔑 Key Parameters

| Parameter | Description |
|---|---|
| `model` | Model name (e.g., `mistral:v0.3`, `llama3`) |
| `messages` | List of `{"role": "user"/"assistant"/"system", "content": "..."}` |
| `stream` | `True` for streaming token output |
| `temperature` | Randomness control (0.0–1.0, default 0.7) |
| `num_predict` | Max tokens to generate |

---

## 📚 Resources

- [Ollama Official Site](https://ollama.com)
- [Ollama Python SDK](https://github.com/ollama/ollama-python)
- [Available Models (Ollama Library)](https://ollama.com/library)
- [OpenAI Compatibility Docs](https://github.com/ollama/ollama/blob/main/docs/openai.md)