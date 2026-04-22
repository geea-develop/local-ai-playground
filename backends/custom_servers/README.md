# 🖥️ Custom Servers — Apple Silicon & Specialized Inference

This directory provides pre-configured server implementations for running LLMs with hardware-optimized backends. Each subdirectory is a self-contained server targeting a specific inference engine or hardware configuration.

---

## 📦 Contents

| Server | Engine | Best For | API Style |
|---|---|---|---|
| **[ollama-server/](./ollama-server)** | Ollama | General-purpose local LLMs | Ollama-native + OpenAI-compat. |
| **[mlx-lm-server/](./mlx-lm-server)** | MLX-LM | Apple Silicon (M-series) native inference | OpenAI-compatible |
| **[mlx-openai-server/](./mlx-openai-server)** | MLX + OpenAI Proxy | Connect OpenAI clients to local MLX | OpenAI-compatible |
| **[llama-cpp-server/](./llama-cpp-server)** | llama.cpp | GGUF model files with Metal acceleration | OpenAI-compatible |
| **[lm-studio-server/](./lm-studio-server)** | LM Studio | GUI-based model management | OpenAI-compatible |
| **[vllm-mlx/](./vllm-mlx)** | vLLM + MLX | High-throughput batch inference | OpenAI-compatible |
| **[debug/](./debug)** | — | Connectivity testing & endpoint debugging | — |

---

## 🚀 Quick Start

All servers follow the same pattern:

```bash
# 1. Enter the server directory
cd <server-name>

# 2. Start the server
./scripts/start.sh
# Or: python server.py (for Python-based servers)
```

### Server Endpoints (Defaults)

| Server | Default Port | Base URL |
|---|---|---|
| `ollama-server` | 11434 | `http://localhost:11434` |
| `mlx-lm-server` | 8080 | `http://localhost:8080` |
| `mlx-openai-server` | 8000 | `http://localhost:8000` |
| `llama-cpp-server` | 8000 | `http://localhost:8000` |
| `lm-studio-server` | 1234 | `http://localhost:1234` |
| `vllm-mlx` | 8000 | `http://localhost:8000` |

---

## 🔌 Connecting to Frameworks

All custom servers expose **OpenAI-compatible** `/v1/chat/completions` endpoints. Set the appropriate base URL in the framework's `.env` file:

```bash
# Example for LangChain connecting to mlx-openai-server
OPENAI_API_BASE=http://localhost:8000/v1
OPENAI_API_KEY=local  # Any non-empty string works
```

---

## 🍎 Apple Silicon Notes

- **MLX servers** (`mlx-lm-server`, `mlx-openai-server`) leverage Apple's unified memory and Metal GPU — significantly faster than CPU-only inference.
- **llama.cpp** automatically uses the Metal backend on M-series chips; no manual GPU layer configuration is needed.
- **vLLM-MLX** is suited for high-throughput use cases where you need to serve multiple concurrent requests locally.

---

## 🐛 Debugging

Use the `debug/` subdirectory to:
- Test basic connectivity to any server endpoint
- Verify model loading and response format
- Check log outputs from running servers

```bash
cd debug
# Follow the README.md inside debug/ for specific debugging scripts
```

---

## 🔧 Troubleshooting

- **Server won't start**: Check that all dependencies in `requirements.txt` are installed in the correct virtual environment.
- **Model not found**: Ensure the model path or model ID in the server config points to a valid local file or Ollama model name.
- **Port conflict**: Change the port in `scripts/start.sh` and update your client's base URL accordingly.
- **Slow inference**: Verify Metal acceleration is active (check for `ggml_metal_init` in logs for llama.cpp; use `--device metal` for MLX).