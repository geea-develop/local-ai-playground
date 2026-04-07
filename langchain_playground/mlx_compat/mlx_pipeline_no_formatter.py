from __future__ import annotations

from typing import Any, List, Optional

from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_community.llms.mlx_pipeline import MLXPipeline


class MLXPipelineNoFormatter(MLXPipeline):
    """Work around `mlx-lm` vs `langchain-community` incompatibility.

    Some `mlx-lm` versions don't accept `formatter=` passed by
    `langchain-community`'s `MLXPipeline._call()`.
    """

    def _call(  # type: ignore[override]
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        from mlx_lm import generate
        from mlx_lm.sample_utils import make_logits_processors, make_sampler

        pipeline_kwargs = kwargs.get("pipeline_kwargs", self.pipeline_kwargs) or {}

        temp: float = pipeline_kwargs.get("temp", 0.0)
        max_tokens: int = pipeline_kwargs.get("max_tokens", 100)
        verbose: bool = pipeline_kwargs.get("verbose", False)

        # NOTE: intentionally ignore `formatter` to avoid passing it to mlx_lm.
        repetition_penalty: Optional[float] = pipeline_kwargs.get(
            "repetition_penalty", None
        )
        repetition_context_size: Optional[int] = pipeline_kwargs.get(
            "repetition_context_size", None
        )
        top_p: float = pipeline_kwargs.get("top_p", 1.0)
        min_p: float = pipeline_kwargs.get("min_p", 0.0)
        min_tokens_to_keep: int = pipeline_kwargs.get("min_tokens_to_keep", 1)

        sampler = make_sampler(temp, top_p, min_p, min_tokens_to_keep)
        logits_processors = make_logits_processors(
            None, repetition_penalty, repetition_context_size
        )

        return generate(
            model=self.model,
            tokenizer=self.tokenizer,
            prompt=prompt,
            max_tokens=max_tokens,
            verbose=verbose,
            sampler=sampler,
            logits_processors=logits_processors,
        )

