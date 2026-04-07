from __future__ import annotations

import os
import logging
from threading import Lock
from time import perf_counter
from typing import Optional

import mlx_lm as mlx
from dotenv import load_dotenv
from langchain.messages import HumanMessage  # type: ignore[import-not-found]
from langchain_community.chat_models.mlx import ChatMLX  # type: ignore[import-not-found]

from mlx_compat.mlx_pipeline_no_formatter import MLXPipelineNoFormatter

# Load environment variables from .env file
load_dotenv()

_model_load_lock = Lock()
_inference_lock = Lock()
logger = logging.getLogger(__name__)
_cached_chat_model: Optional[ChatMLX] = None


def validate_model_path() -> tuple[bool, Optional[str]]:
    """
    Validate that the model path is correctly configured and accessible.
    Returns (is_valid, error_message).
    """
    models_dir = os.getenv("MODELS_DIR_PATH")
    model_dir = os.getenv("MODEL_DIR_PATH")
    
    if not models_dir:
        msg = "MODELS_DIR_PATH not set in .env - model will fail to load"
        logger.warning(msg)
        return False, msg
    
    if not model_dir:
        msg = "MODEL_DIR_PATH not set in .env - model will fail to load"
        logger.warning(msg)
        return False, msg
    
    model_dir_path = os.path.join(models_dir, model_dir)
    if not os.path.isdir(model_dir_path):
        msg = f"Model directory not found at {model_dir_path}"
        logger.warning(msg)
        return False, msg
    
    logger.info(f"Model path validation successful: {model_dir_path}")
    return True, None


def get_model_path() -> Optional[str]:
    """
    Get the full path to the model directory if valid, otherwise None.
    """
    models_dir = os.getenv("MODELS_DIR_PATH")
    model_dir = os.getenv("MODEL_DIR_PATH")
    
    if models_dir and model_dir:
        return os.path.join(models_dir, model_dir)
    return None


def get_chat_model() -> ChatMLX:
    """
    Load and cache the MLX-based ChatMLX model using environment variables.

    Expected env vars:
    - MODELS_DIR_PATH: base directory that contains the model directory
    - MODEL_DIR_PATH: name of the specific model directory under MODELS_DIR_PATH
    """

    models_dir = os.getenv("MODELS_DIR_PATH")
    model_dir = os.getenv("MODEL_DIR_PATH")
    if not models_dir or not model_dir:
        msg = "Missing MODELS_DIR_PATH or MODEL_DIR_PATH in .env"
        logger.error(msg)
        raise ValueError(msg)

    model_dir_path = os.path.join(models_dir, model_dir)
    if not os.path.isdir(model_dir_path):
        msg = f"MLX model directory not found at: {model_dir_path}"
        logger.error(msg)
        raise FileNotFoundError(msg)

    global _cached_chat_model
    if _cached_chat_model is not None:
        return _cached_chat_model

    # MLX/Metal init is not safe under concurrent startup requests.
    # Guard load so only one thread initializes GPU resources.
    with _model_load_lock:
        # Double-check after acquiring lock to avoid duplicate loads.
        if _cached_chat_model is not None:
            return _cached_chat_model
        logger.info("Loading MLX model for backend from: %s", model_dir_path)
        model, tokenizer = mlx.load(model_dir_path)

        llm = MLXPipelineNoFormatter(
            model=model, tokenizer=tokenizer, pipeline_kwargs={"max_tokens": 256}
        )
        _cached_chat_model = ChatMLX(llm=llm)

    return _cached_chat_model


def run_inference(
    prompt: str,
    max_tokens: Optional[int] = None,
    temperature: Optional[float] = None,
    *,
    request_id: Optional[str] = None,
) -> str:
    """Helper to run a single-turn inference with the cached chat model."""
    infer_start = perf_counter()
    if request_id:
        logger.debug(f"run_inference starting request_id={request_id}")
    
    try:
        chat_model = get_chat_model()
        logger.debug(f"Model loaded successfully for request_id={request_id}")
    except (ValueError, FileNotFoundError) as e:
        logger.error(f"Failed to load model for request_id={request_id}: {e}")
        raise
    
    pipeline_kwargs = dict(getattr(chat_model.llm, "pipeline_kwargs", {}) or {})
    # Upper bound on completion length; raise via MAX_GENERATION_TOKENS if answers
    # or tool/skill JSON truncate (client max_tokens is clamped to this).
    max_generation_tokens = int(os.getenv("MAX_GENERATION_TOKENS", "2048"))
    if max_tokens is not None:
        pipeline_kwargs["max_tokens"] = min(max(1, int(max_tokens)), max_generation_tokens)
    else:
        pipeline_kwargs["max_tokens"] = min(
            int(pipeline_kwargs.get("max_tokens", 256)), max_generation_tokens
        )
    if temperature is not None:
        pipeline_kwargs["temp"] = float(temperature)

    # Serialize inference calls to avoid Metal command-buffer assertion crashes
    # when multiple requests arrive concurrently.
    wait_start = perf_counter()
    with _inference_lock:
        wait_elapsed = perf_counter() - wait_start
        if wait_elapsed > 0.05:
            logger.debug("Inference waited %.2fs for lock", wait_elapsed)
        res = chat_model.invoke(
            [HumanMessage(content=prompt)],
            pipeline_kwargs=pipeline_kwargs,
        )
    total_elapsed = perf_counter() - infer_start
    if request_id:
        logger.info(
            "Inference completed request_id=%s in %.2fs (max_tokens=%s temp=%s prompt_chars=%d)",
            request_id,
            total_elapsed,
            pipeline_kwargs.get("max_tokens"),
            pipeline_kwargs.get("temp"),
            len(prompt),
        )
    else:
        logger.info(
            "Inference completed in %.2fs (max_tokens=%s temp=%s prompt_chars=%d)",
            total_elapsed,
            pipeline_kwargs.get("max_tokens"),
            pipeline_kwargs.get("temp"),
            len(prompt),
        )
    return res.content

