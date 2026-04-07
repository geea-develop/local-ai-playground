# Llama.cpp HTTP Server Summary

Llama.cpp HTTP Server is a lightweight, pure C/C++ HTTP server for running large language models (LLMs) using the llama.cpp library. It provides OpenAI-compatible API endpoints for chat completions, completions, embeddings, and reranking. Key features include:

- Support for F16 and quantized models on GPU and CPU
- OpenAI API compatible chat completions, responses, and embeddings routes
- Anthropic Messages API compatible chat completions
- Parallel decoding with multi-user support
- Continuous batching for high throughput
- Multimodal support (experimental)
- Speculative decoding
- Built-in tools support for file system access
- Monitoring and metrics endpoints
- Schema-constrained JSON response format
- Function calling and tool use support

The server supports various sampling parameters, context management, and can be configured for different use cases including embeddings, reranking, and multimodal models. It includes a web UI and supports SSL for secure deployments.

https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md

Reviewed by Goose 2026-04-07 16:05