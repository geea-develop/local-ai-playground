# MLX-LM HTTP Server Summary

The MLX LM HTTP Server provides an OpenAI-compatible API for text generation using MLX models. It's designed to be similar to the OpenAI chat API and supports various sampling parameters and model configurations.

Key features:
- OpenAI-compatible chat completions API
- Support for streaming responses
- Configurable sampling parameters (temperature, top_p, top_k, min_p, etc.)
- Repetition, presence, and frequency penalties
- Logit bias support
- Log probabilities for generated tokens
- Model switching and adapter support
- Speculative decoding with draft models
- Role mapping for custom prompt formatting

The server supports conversation history through messages array, stop sequences, and various generation controls. It's primarily focused on text generation with MLX language models.

https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/SERVER.md

Reviewed by Goose 2026-04-07 16:05