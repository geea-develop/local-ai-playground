"""
LangChain `ChatMLX` example that explicitly builds `MLXPipeline` from a
locally stored MLX model directory.

This is useful when you already downloaded MLX model files to disk.
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
    model_dir = os.getenv("MODEL_DIR_PATH")
    if not models_dir or not model_dir:
        raise ValueError("Missing MODELS_DIR_PATH or MODEL_DIR_PATH in .env")

    model_dir_path = os.path.join(models_dir, model_dir)
    query = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "Could you explain what a function calling agent is?"
    )

    print(f"Loading MLX model from: {model_dir_path}")
    model, tokenizer = mlx.load(model_dir_path)

    llm = MLXPipelineNoFormatter(
        model=model, tokenizer=tokenizer, pipeline_kwargs={"max_tokens": 256}
    )
    chat_model = ChatMLX(llm=llm)

    res = chat_model.invoke([HumanMessage(content=query)])
    print(res.content)


if __name__ == "__main__":
    main()

