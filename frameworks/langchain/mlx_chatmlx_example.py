"""
Minimal LangChain `ChatMLX` example.

This variant uses `ChatMLX` with `MLXPipeline`.

If a local model directory exists at `MODELS_DIR_PATH/MODEL_DIR_PATH`, it
loads it directly (no HuggingFace download). Otherwise it falls back to
`MLXPipeline.from_model_id()` (which may download).
"""

from __future__ import annotations

import os
import sys

import mlx_lm as mlx
from dotenv import load_dotenv
from langchain.messages import HumanMessage  # type: ignore[import-not-found]
from langchain_community.chat_models.mlx import ChatMLX  # type: ignore[import-not-found]
from mlx_compat.mlx_pipeline_no_formatter import MLXPipelineNoFormatter


def main() -> None:
    load_dotenv()

    models_dir = os.getenv("MODELS_DIR_PATH")
    model_id_or_dir = os.getenv("MODEL_DIR_PATH")
    if not models_dir and not model_id_or_dir:
        raise ValueError("Missing MODELS_DIR_PATH / MODEL_DIR_PATH in .env")
    if not model_id_or_dir:
        raise ValueError("Missing MODEL_DIR_PATH in .env")

    local_model_dir_path = (
        os.path.join(models_dir, model_id_or_dir) if models_dir else None
    )

    query = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "What is the capital of France? Answer in one sentence."
    )

    pipeline_kwargs = {"max_tokens": 256, "temp": 0.1}

    # Prefer a locally downloaded MLX model directory:
    # - If `MODELS_DIR_PATH/model_dir_path` exists, use `mlx_lm.load()` (no HF download).
    # - Otherwise fall back to `MLXPipeline.from_model_id()` (may download from HuggingFace).
    if local_model_dir_path and os.path.isdir(local_model_dir_path):
        print(f"Loading MLX model locally from: {local_model_dir_path}")
        model, tokenizer = mlx.load(local_model_dir_path)
        llm = MLXPipelineNoFormatter(
            model=model, tokenizer=tokenizer, pipeline_kwargs=pipeline_kwargs
        )
    else:
        print(f"Loading MLXPipeline from model id (may download): {model_id_or_dir}")
        llm = MLXPipelineNoFormatter.from_model_id(
            model_id_or_dir,
            pipeline_kwargs=pipeline_kwargs,
        )

    chat_model = ChatMLX(llm=llm)
    res = chat_model.invoke([HumanMessage(content=query)])
    print(res.content)


if __name__ == "__main__":
    main()

