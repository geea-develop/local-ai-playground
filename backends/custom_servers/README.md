debug/
  README.md  [28]

llama-cpp-server/
  README.md  [19]

lm-studio-server/
  README.md  [4]

mlx-lm-server/
  scripts/
    start.sh  [7]
  README.md  [18]
  requirements.txt  [1]

mlx-openai-server/
  logs/
  scripts/
    start.sh  [10]
  README.md  [20]
  requirements.txt  [1]

ollama-server/
  README.md  [4]

vllm-mlx/
  scripts/
    start.sh  [7]
  README.md  [22]
  requirements.txt  [1]
  server.py  [0]

## Local AI Server Setup

This directory contains various local AI server implementations for different LLM backends:

- **debug/**: Contains debugging tools and configuration files
- **llama-cpp-server/**: Server for running llama.cpp-based models
- **lm-studio-server/**: Server for LM Studio-compatible models
- **mlx-lm-server/**: Server for running MLX-based models
- **mlx-openai-server/**: OpenAI-compatible server for MLX models
- **ollama-server/**: Ollama-compatible server for local model execution
- **vllm-mlx/**: vLLM-based server for MLX models

## Setup Instructions

1. Start the appropriate server based on your model needs:

```bash
# For debugging
cd debug && ./start.sh

# For llama-cpp models
cd llama-cpp-server && ./start.sh

# For MLX models
cd mlx-lm-server && ./start.sh

# For Ollama models
cd ollama-server && ./start.sh
```

2. Configure your client to connect to the appropriate server endpoint.

3. Test connectivity by sending a simple request to the server.

## Key Features

- Supports multiple LLM backends (llama.cpp, MLX, Ollama, vLLM)
- Provides OpenAI-compatible endpoints for easy integration
- Includes pre-configured scripts for quick deployment
- Each server includes its own configuration files and documentation

## Troubleshooting

- Ensure all dependencies are installed before starting servers
- Check logs in the `logs/` directory for error messages
- Verify network connectivity between client and server
- Ensure proper environment variables are set for authentication and model loading

Reviewed by Goose 2026-04-07 16:05