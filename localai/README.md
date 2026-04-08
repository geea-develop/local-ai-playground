# LocalAI

LocalAI is a free, open-source alternative to OpenAI, functioning as a drop-in replacement REST API for local inferencing. It allows you to run LLMs, generate images, and produce audio locally.

Official Documentation: [https://localai.io/](https://localai.io/)

## Quickstart with Docker

The easiest way to run LocalAI is via Docker:

```bash
# Start LocalAI with CPU support
docker run -p 8080:8080 --name local-ai -ti localai/localai:latest-cpu
```

Once running, the API will be available at `http://localhost:8080`.

## Installing Models

You can install models via the Web UI at `http://localhost:8080` or via the CLI:

```bash
# Example: Install Llama 3.2 1B
docker exec -it local-ai local-ai models install llama-3.2-1b-instruct:q4_k_m
```

## Using the API

Since LocalAI is OpenAI-compatible, you can use the official `openai` Python library.

### 1. Setup Environment
```bash
pip install openai python-dotenv
```

### 2. Run the Example
Check `localai_example.py` in this folder.