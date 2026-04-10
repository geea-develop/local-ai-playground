#!/bin/bash

MODELS_DIR_PATH="<models-path>"
MODEL_DIR_PATH="lmstudio-community/Qwen3-4B-Instruct-2507-MLX-4bit"

# Start the server
source venv/bin/activate && vllm-mlx serve "$MODELS_DIR_PATH/$MODEL_DIR_PATH"