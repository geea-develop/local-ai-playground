# smolagents Local Examples

This folder contains examples of how to use Hugging Face's `smolagents` with local LLM backends.

## Set Up

1. **Create and activate the virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variables:**
   The examples use `dotenv` to load configuration. You can copy `.env.example` to `.env`.
   - `OLLAMA_API_BASE`: (Default: http://localhost:11434)
   - `LLM_MODEL`: The LLM to use (e.g., `mistral:v0.3`, `llama3`)
   - `EMBED_MODEL`: The embedding model for RAG (e.g., `nomic-embed-text`)

---

## Included Examples

### 1. Ollama RAG (PDF Search) 🌟
This implementation uses a direct context-to-prompt approach. While `smolagents` supports multi-step agents, local models like Mistral and Llama 3 often struggle with consistent JSON tool-calling formats. This version provides the most reliable performance for RAG tasks.
- **File:** `ollama_rag_example.py`
- **Features:** 
  - Uses `langchain` for PDF processing and FAISS indexing.
  - Manual context retrieval for maximum stability with local backends.
- **Run:** `python ollama_rag_example.py`

### 2. MLX (Highest Priority for Mac)
Uses the `mlx-lm` library to run models on Apple Silicon.
- **File:** `mlx_example.py`

### 3. llama.cpp (Direct Loader)
Uses `llama-cpp-python` to load GGUF models directly with Metal acceleration.
- **File:** `llama_cpp_example.py`

### 4. LM Studio
Uses the OpenAI-compatible API provided by LM Studio.
- **File:** `lm_studio_example.py`

### 5. Ollama (Basic Chat)
A simple example using Ollama's OpenAI-compatible API.
- **File:** `ollama_example.py`

---

## Running an Example

Ensure you are in the virtual environment:

```bash
python <example_file.py>
```
(e.g., `python ollama_rag_example.py`)

