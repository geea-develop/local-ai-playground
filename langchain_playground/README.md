# LangChain Playground with llama-cpp-python on macOS

## Overview

This project demonstrates how to use LangChain with the llama-cpp-python library to run local language model inference on macOS, leveraging the Metal backend for optimized performance on Apple Silicon chips.

## Installation Instructions

pip install -r requirements.txt

This installs both the example scripts and the FastAPI backend dependencies.

## Optional: Verify Metal Backend is Working

python -c "from llama_cpp import Llama; llm = Llama.from_pretrained(repo_id='TinyLlama/TinyLlama-1.1B-Chat-v0.4', n_ctx=2048, verbose=False); print('Metal loaded successfully')"

## Run the main script

python main.py

## Run the local OpenAI-compatible chat server

A small FastAPI backend in the `backend` package exposes the local MLX model
via an OpenAI-style `/v1/chat/completions` endpoint so tools like Claude Code
can talk to it as if it were the OpenAI API.

Start the server from the project root:

```bash
uvicorn backend.app:app --reload --host 127.0.0.1 --port 0
```

Basic health check:

```bash
curl http://127.0.0.1:8000/health
```

Example chat completion request:

```bash
curl http://127.0.0.1:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d ' {
    "model": "local-mlx",
    "messages": [
      {"role": "user", "content": "Say hello from the local MLX model."}
    ]
  }'
```

In Claude Code (or any OpenAI-compatible client), configure the base URL as
`http://127.0.0.1:8000` and use `local-mlx` (or any string) as the `model`
name when sending `chat.completions` requests.

## Run locally with Claude CLI

The same backend also exposes a minimal Anthropic-style Messages API at
`POST /v1/messages`.

Claude Code/CLI reads configuration from `~/.claude/settings.json` (or from
environment variables set in your shell).

1. **Start the server** (from the project root):

```bash
uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000
```

2. **Run Claude using environment variables** (recommended):

```bash
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 \
ANTHROPIC_AUTH_TOKEN=local-mlx \
ANTHROPIC_API_KEY=local-mlx \
ANTHROPIC_BASE_URL=http://127.0.0.1:8000 \
claude --model local-mlx
```

If you already have `ANTHROPIC_BASE_URL` set to an Ollama server
(for example `http://localhost:11434`) in `~/.claude/settings.json`, Claude will
keep using that unless you update it to `http://127.0.0.1:8000`.

The CLI should then send `POST /v1/messages` requests to `http://127.0.0.1:8000`,
and the backend will route them to the local MLX model.

### Latency tuning (recommended for Claude CLI)

Claude CLI can send large prompts and high `max_tokens` values by default,
which can slow down local MLX inference. The backend supports server-side caps:

- `MAX_PROMPT_CHARS`: max prompt size sent to the model (keeps latest text).
- `MAX_GENERATION_TOKENS`: hard cap for generated tokens.

Suggested values for responsive local usage:

```bash
MAX_PROMPT_CHARS=3500
MAX_GENERATION_TOKENS=256
```

Example run with tuning:

```bash
MAX_PROMPT_CHARS=3500 \
MAX_GENERATION_TOKENS=256 \
uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000
```

Tip: watch server logs (`backend.app` and `backend.model_loader`) to confirm
prompt truncation and per-request inference times.

## Key Technical Details for macOS Users

llama-metal: When you install llama-cpp-python on Apple Silicon (M1/M2/M3), it automatically builds the Metal backend. You do not need to manually specify GPU layers unless you are doing heavy fine-tuning; the -1 setting lets the library manage the CPU/GPU split optimally for inference speed.

Model Format: The example uses repo_id, which downloads a .gguf file (quantized model) from HuggingFace. This format is highly optimized for local execution and keeps file sizes small (e.g., 1.5GB vs several GBs for float models).

Where to get models: Search HuggingFace for "GGUF". Popular choices are Qwen2.5 (great reasoning), Llama-3, or Gemma.

Performance:
- M1/M2/M3 Macs: Expect ~10–20 tokens per second for small models, scaling up significantly with larger chips.
- Intel Macs: Performance will be slower as it relies purely on CPU without Metal acceleration support in the same way.

## Next Steps: Advanced Usage

If you want to take this further, try these modifications:

- Streaming Responses: To see text appear token-by-token (like typing), modify the chain to use llm(stream=True) and iterate over the result in a loop.
- Custom Quantization: Download specific quantized models (e.g., Q4_K_M.gguf) to balance speed and memory usage.
- RAG Integration: You can easily integrate this with LangChain Document Loaders to create a local RAG bot that answers questions about your own documents without sending data to the internet.

<!-- TODO: read about RAG types and tools -->
<!-- Read about using Goose, linux server, unsloth -->
<!-- Try to benchmark and run a local model and iteract with it using langchain for development -->

Reviewed by Goose 2026-04-07 16:05