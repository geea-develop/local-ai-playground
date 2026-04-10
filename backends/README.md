# Local AI Backends & Inference Servers

This directory centralizes the setup, configuration, and optimization of local execution engines and model runners.

## Purpose
The **backends** are the heartbeat of the playground. They are responsible for downloading models, performing inference, and serving the models via APIs (usually OpenAI-compatible or Ollama-native) to the `interfaces/` and `frameworks/`.

## Contents

- **[ollama/](./ollama)**: Native Ollama configurations and model management.
- **[localai/](./localai)**: API emulation and multi-model serving using LocalAI.
- **[llm_runner/](./llm_runner)**: Specialized orchestration for high-performance inference.
- **[custom_servers/](./custom_servers)**: Hardware-specific configurations (e.g., Apple Silicon optimizations via `mlx-lm`, `vLLM`).

## When to use these
Modify these configurations when you need to add new models, optimize inference speed for your specific hardware, or change how models are exposed via the local network.
