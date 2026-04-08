# smolagents Local Examples

This folder contains examples of how to use Hugging Face's `smolagents` with local LLM backends.

## Setup

1. **Create and activate the virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install smolagents mlx-lm llama-cpp-python python-dotenv
   ```

3. **Environment Variables:**
   The examples use `dotenv` to load model configurations. Ensure you have a `.env` file with:
   - `MODELS_DIR_PATH`: Path to your models directory
   - `MODEL_DIR_PATH`: Subdirectory for the model
   - `MODEL_FILE_PATH`: (For llama.cpp) The GGUF file name

## Included Examples

### 1. MLX (Highest Priority for Mac)
Uses the `mlx-lm` library to run models on Apple Silicon.
- **File:** `mlx_example.py`
- **Model:** Loads from `MODELS_DIR_PATH/MODEL_DIR_PATH` or falls back to ID.

### 2. llama.cpp (Direct Loader)
Uses `llama-cpp-python` to load GGUF models directly with Metal acceleration.
- **File:** `llama_cpp_example.py`
- **Model:** Loads from `MODELS_DIR_PATH/MODEL_DIR_PATH/MODEL_FILE_PATH`.

### 3. LM Studio
Uses the OpenAI-compatible API provided by LM Studio.
- **File:** `lm_studio_example.py`
- **Requirement:** LM Studio must be running with the "Local Server" started.

### 4. Ollama
Uses Ollama's OpenAI-compatible API.
- **File:** `ollama_example.py`
- **Requirement:** Ollama must be running.

## Running an Example

```bash
./venv/bin/python mlx_example.py
```
(Replace `mlx_example.py` with the desired file)
