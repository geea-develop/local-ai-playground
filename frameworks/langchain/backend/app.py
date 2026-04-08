from __future__ import annotations

import time
import uuid
import json
import logging
import os
from typing import Any, Dict, Iterable, Optional

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, StreamingResponse

# Load environment variables from .env file
load_dotenv()

from .anthropic_content import (
    message_content_to_prompt_text,
    parse_assistant_completion_to_content_blocks,
    system_to_prompt_prefix,
)
from .model_loader import run_inference, validate_model_path, get_model_path
from .schemas import (
    AnthropicMessageResponse,
    AnthropicMessagesRequest,
    AnthropicTextBlock,
    AnthropicToolUseBlock,
    AnthropicUsage,
    ChatCompletionChoice,
    ChatCompletionChoiceMessage,
    ChatCompletionRequest,
    ChatCompletionResponse,
    OllamaChatRequest,
    OllamaGenerateRequest,
    OllamaShowRequest,
)

# Determine logging level from environment, default to INFO
log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
log_level = getattr(logging, log_level_str, logging.INFO)

logging.basicConfig(
    level=log_level,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger(__name__)
# 0 or negative = do not truncate (preserves tool_use / system at start of prompt).
MAX_PROMPT_CHARS = int(os.getenv("MAX_PROMPT_CHARS", "0"))

app = FastAPI(title="Local MLX OpenAI-compatible Chat Server")

# Track model validation state
_model_valid = False
_model_error_msg: Optional[str] = None

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    """Validate model configuration on startup."""
    global _model_valid, _model_error_msg
    logger.info("=" * 80)
    logger.info("Backend startup - validating model configuration")
    logger.info("=" * 80)
    
    model_path = get_model_path()
    if model_path:
        logger.info(f"Configured MODEL_DIR_PATH: {os.getenv('MODEL_DIR_PATH')}")
        logger.info(f"Full model path: {model_path}")
    else:
        logger.warning("No model path configured")
    
    is_valid, error_msg = validate_model_path()
    _model_valid = is_valid
    _model_error_msg = error_msg
    
    if is_valid:
        logger.info("✓ Model path validation PASSED")
    else:
        logger.error(f"✗ Model path validation FAILED: {error_msg}")
    
    logger.info("=" * 80)


def _truncate_prompt(prompt: str, request_id: str) -> str:
    if MAX_PROMPT_CHARS <= 0:
        return prompt
    if len(prompt) <= MAX_PROMPT_CHARS:
        return prompt
    logger.warning(
        "prompt truncated request_id=%s original_chars=%d truncated_chars=%d",
        request_id,
        len(prompt),
        MAX_PROMPT_CHARS,
    )
    # Keep the tail because it typically contains the user's latest instruction.
    return prompt[-MAX_PROMPT_CHARS:]


@app.get("/health")
def health() -> Dict[str, Any]:
    return {"status": "ok"}


@app.get("/")
@app.head("/")
def root() -> Dict[str, Any]:
    # Some clients probe `/` with HEAD/GET.
    return {"status": "ok"}


# --- Ollama API compatibility (NDJSON streaming where applicable) ---


def _ollama_compat_version() -> str:
    # Clients may require a minimum Ollama server version (e.g. >= 0.6.4).
    default = "0.6.4"
    return os.getenv("OLLAMA_COMPAT_VERSION", default).strip() or default


def _ollama_created_at() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()) + "Z"


def _ollama_advertised_model_name() -> str:
    explicit = os.getenv("OLLAMA_MODEL_NAME", "").strip()
    if explicit:
        return explicit
    model_dir = os.getenv("MODEL_DIR_PATH", "local-mlx")
    short = model_dir.rstrip("/").split("/")[-1]
    return short if ":" in short else f"{short}:latest"


def _approx_token_count(s: str) -> int:
    return max(1, len(s.split()))


def _ollama_options_to_infer_kwargs(
    options: Optional[Dict[str, Any]],
) -> tuple[Optional[int], Optional[float]]:
    if not options:
        return None, None
    max_tokens = options.get("num_predict")
    if max_tokens is not None:
        max_tokens = int(max_tokens)
    temperature = options.get("temperature")
    if temperature is not None:
        temperature = float(temperature)
    return max_tokens, temperature


def _ollama_stream_default(explicit: Optional[bool]) -> bool:
    return True if explicit is None else bool(explicit)


def _ollama_generate_prompt(body: OllamaGenerateRequest) -> str:
    if body.raw:
        base = body.prompt or ""
        if body.suffix:
            base = base + (body.suffix or "")
        return base
    parts: list[str] = []
    if body.system:
        parts.append(f"system: {body.system}")
    p = body.prompt or ""
    if body.suffix:
        p = p + (body.suffix or "")
    if p:
        parts.append(f"user: {p}")
    if not parts:
        return ""
    return "\n".join(parts) + "\nassistant:"


def _ollama_message_content_str(content: Any) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        pieces: list[str] = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                pieces.append(str(item.get("text", "")))
            else:
                pieces.append(str(item))
        return " ".join(pieces)
    return str(content)


def _ollama_chat_prompt(body: OllamaChatRequest) -> str:
    lines: list[str] = []
    if body.tools:
        lines.append("tools: " + json.dumps(body.tools, ensure_ascii=False, default=str))
    for m in body.messages:
        lines.append(f"{m.role}: {_ollama_message_content_str(m.content)}")
    return "\n".join(lines) + "\nassistant:"


def _chunk_text_for_stream(text: str, chunk_size: int = 20) -> list[str]:
    if not text:
        return []
    return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]


@app.get("/api/version")
def ollama_version() -> Dict[str, str]:
    return {"version": _ollama_compat_version()}


@app.head("/api/version")
def ollama_version_head() -> Response:
    return Response()


@app.get("/api/tags")
def ollama_tags() -> Dict[str, Any]:
    name = _ollama_advertised_model_name()
    return {
        "models": [
            {
                "name": name,
                "model": name,
                "modified_at": _ollama_created_at(),
                "size": 0,
                "digest": "local",
                "details": {
                    "parent_model": "",
                    "format": "mlx",
                    "family": "local",
                    "families": ["local"],
                    "parameter_size": "",
                    "quantization_level": "",
                },
            }
        ]
    }


@app.post("/api/show")
def ollama_show(body: OllamaShowRequest) -> Dict[str, Any]:
    return {
        "modelfile": "",
        "parameters": "",
        "template": "",
        "details": {
            "parent_model": "",
            "format": "mlx",
            "family": "",
            "families": [],
            "parameter_size": "",
            "quantization_level": "",
        },
        "model_info": {},
    }


@app.post("/api/generate")
def ollama_generate(body: OllamaGenerateRequest) -> Any:
    request_id = uuid.uuid4().hex[:8]
    stream = _ollama_stream_default(body.stream)
    opt_max, opt_temp = _ollama_options_to_infer_kwargs(body.options)
    prompt = _ollama_generate_prompt(body)
    prompt = _truncate_prompt(prompt, request_id)
    logger.debug(f"[{request_id}] PROMPT:\n{prompt}")

    def ndjson_events() -> Iterable[str]:
        t0_ns = time.perf_counter_ns()
        infer_start_ns = time.perf_counter_ns()
        completion = run_inference(
            prompt,
            max_tokens=opt_max,
            temperature=opt_temp,
            request_id=request_id,
        )
        infer_ns = time.perf_counter_ns() - infer_start_ns
        logger.debug(f"[{request_id}] RESPONSE:\n{completion}")
        if stream:
            for piece in _chunk_text_for_stream(completion):
                ev = {
                    "model": body.model,
                    "created_at": _ollama_created_at(),
                    "response": piece,
                    "done": False,
                }
                yield json.dumps(ev, ensure_ascii=False) + "\n"
            total_ns = time.perf_counter_ns() - t0_ns
            final = {
                "model": body.model,
                "created_at": _ollama_created_at(),
                "response": "",
                "done": True,
                "total_duration": total_ns,
                "load_duration": 0,
                "prompt_eval_count": _approx_token_count(prompt),
                "prompt_eval_duration": 0,
                "eval_count": _approx_token_count(completion),
                "eval_duration": infer_ns,
            }
            yield json.dumps(final, ensure_ascii=False) + "\n"
        else:
            total_ns = time.perf_counter_ns() - t0_ns
            one = {
                "model": body.model,
                "created_at": _ollama_created_at(),
                "response": completion,
                "done": True,
                "total_duration": total_ns,
                "load_duration": 0,
                "prompt_eval_count": _approx_token_count(prompt),
                "prompt_eval_duration": 0,
                "eval_count": _approx_token_count(completion),
                "eval_duration": infer_ns,
            }
            yield json.dumps(one, ensure_ascii=False) + "\n"

    if stream:
        return StreamingResponse(ndjson_events(), media_type="application/x-ndjson")
    # Single JSON object (first and only line)
    return json.loads(next(iter(ndjson_events())))


@app.post("/api/chat")
def ollama_chat(body: OllamaChatRequest) -> Any:
    request_id = uuid.uuid4().hex[:8]
    stream = _ollama_stream_default(body.stream)
    opt_max, opt_temp = _ollama_options_to_infer_kwargs(body.options)
    prompt = _ollama_chat_prompt(body)
    prompt = _truncate_prompt(prompt, request_id)
    logger.debug(f"[{request_id}] PROMPT:\n{prompt}")

    def ndjson_events() -> Iterable[str]:
        t0_ns = time.perf_counter_ns()
        infer_start_ns = time.perf_counter_ns()
        completion = run_inference(
            prompt,
            max_tokens=opt_max,
            temperature=opt_temp,
            request_id=request_id,
        )
        infer_ns = time.perf_counter_ns() - infer_start_ns
        logger.debug(f"[{request_id}] RESPONSE:\n{completion}")
        if stream:
            for piece in _chunk_text_for_stream(completion):
                ev = {
                    "model": body.model,
                    "created_at": _ollama_created_at(),
                    "message": {"role": "assistant", "content": piece},
                    "done": False,
                }
                yield json.dumps(ev, ensure_ascii=False) + "\n"
            total_ns = time.perf_counter_ns() - t0_ns
            final = {
                "model": body.model,
                "created_at": _ollama_created_at(),
                "message": {"role": "assistant", "content": ""},
                "done": True,
                "total_duration": total_ns,
                "load_duration": 0,
                "prompt_eval_count": _approx_token_count(prompt),
                "prompt_eval_duration": 0,
                "eval_count": _approx_token_count(completion),
                "eval_duration": infer_ns,
            }
            yield json.dumps(final, ensure_ascii=False) + "\n"
        else:
            total_ns = time.perf_counter_ns() - t0_ns
            one = {
                "model": body.model,
                "created_at": _ollama_created_at(),
                "message": {"role": "assistant", "content": completion},
                "done": True,
                "total_duration": total_ns,
                "load_duration": 0,
                "prompt_eval_count": _approx_token_count(prompt),
                "prompt_eval_duration": 0,
                "eval_count": _approx_token_count(completion),
                "eval_duration": infer_ns,
            }
            yield json.dumps(one, ensure_ascii=False) + "\n"

    if stream:
        return StreamingResponse(ndjson_events(), media_type="application/x-ndjson")
    return json.loads(next(iter(ndjson_events())))


@app.get("/v1/models")
def list_models() -> Dict[str, Any]:
    """
    Minimal OpenAI-/Anthropic-style model listing.

    Many clients (including Claude CLI) call this to discover available models.
    Returns the actual configured MLX model if valid, otherwise shows a warning.
    """
    if not _model_valid:
        logger.warning(f"Model validation failed: {_model_error_msg}")
        # Still return models for compatibility, but only the generic ones
        return {
            "object": "list",
            "data": [
                {
                    "id": "local-mlx",
                    "object": "model",
                    "owned_by": "local",
                    "note": "Model path invalid - inference will fail",
                },
            ],
        }
    
    model_name = _ollama_advertised_model_name()
    return {
        "object": "list",
        "data": [
            {
                "id": model_name,
                "object": "model",
                "owned_by": "local",
            },
            # Also advertise these for compatibility
            {
                "id": "claude-3-5-sonnet-latest",
                "object": "model",
                "owned_by": "local",
                "note": "Routed to local MLX model",
            },
            {
                "id": "claude-haiku-4-5-20251001",
                "object": "model",
                "owned_by": "local",
                "note": "Routed to local MLX model",
            },
        ],
    }


@app.get("/v1/models/{model_id}")
def get_model(model_id: str) -> Dict[str, Any]:
    """
    Minimal model detail endpoint.
    """
    # Be permissive: some Claude Code flows may query model ids that are not
    # explicitly listed. We treat any model id as "available" and route it to
    # the same local backend.
    return {
        "id": model_id,
        "object": "model",
        "owned_by": "local",
    }


@app.post("/v1/messages", response_model=AnthropicMessageResponse)
def anthropic_messages(body: AnthropicMessagesRequest) -> AnthropicMessageResponse:
    request_id = uuid.uuid4().hex[:8]
    request_start = time.time()
    logger.info(
        "anthropic_messages start request_id=%s stream=%s model=%s messages=%d tools=%s max_tokens=%s temp=%s",
        request_id,
        body.stream,
        body.model,
        len(body.messages),
        len(body.tools) if body.tools else 0,
        body.max_tokens,
        body.temperature,
    )
    """
    Anthropic-style Messages API shim: flattens messages (including tool_use /
    tool_result blocks) into text for the local model, then maps completion
    text back to Anthropic content blocks when the model emits tool_use-shaped
    output.
    """
    t_prompt0 = time.perf_counter()
    prompt_parts: list[str] = []
    if body.system:
        prompt_parts.extend(system_to_prompt_prefix(body.system))
    if body.tools:
        # Format tools with explicit instructions on how to invoke them
        tools_text = "AVAILABLE TOOLS:\n\n"
        for tool in body.tools:
            tools_text += f"Tool: {tool['name']}\n"
            tools_text += f"Description: {tool['description']}\n"
            if 'input_schema' in tool:
                props = tool['input_schema'].get('properties', {})
                required = tool['input_schema'].get('required', [])
                tools_text += f"Parameters: {', '.join(props.keys())}\n"
                if required:
                    tools_text += f"Required: {', '.join(required)}\n"
            tools_text += "\n"
        
        tools_text += """TO USE A TOOL: Respond with ONLY a JSON code block like this:
```json
{"name": "tool_name", "arguments": {"param1": "value", "param2": "value"}}
```

Always use JSON code blocks for tool calls. Do NOT provide explanations before or after the tool call."""
        
        prompt_parts.append(tools_text)
    for msg in body.messages:
        line = f"{msg.role}: {message_content_to_prompt_text(msg.content)}"
        prompt_parts.append(line)

    prompt = "\n".join(prompt_parts) + "\nassistant:"
    prompt = _truncate_prompt(prompt, request_id)
    prompt_build_ms = (time.perf_counter() - t_prompt0) * 1000
    logger.info(
        "anthropic_messages prompt_ready request_id=%s prompt_build_ms=%.1f prompt_chars=%d max_prompt_chars=%s",
        request_id,
        prompt_build_ms,
        len(prompt),
        MAX_PROMPT_CHARS,
    )
    logger.debug(f"[{request_id}] PROMPT:\n{prompt}")

    def approx_tokens(s: str) -> int:
        # Very rough, but Claude Code expects non-null integers.
        return max(1, len(s.split()))

    input_tokens = approx_tokens(prompt)

    if body.stream:
        # Minimal Anthropic streaming: SSE with `data: {json}\n\n` events.
        message_id = f"msg-{uuid.uuid4().hex}"

        def sse(event_name: str, data_obj: Dict[str, Any]) -> str:
            payload = json.dumps(data_obj, ensure_ascii=False)
            return f"event: {event_name}\ndata: {payload}\n\n"

        def event_stream() -> Iterable[str]:
            # message_start
            yield sse(
                "message_start",
                {
                    "type": "message_start",
                    "message": {
                        "id": message_id,
                        "type": "message",
                        "role": "assistant",
                        "model": body.model,
                        "content": [],
                        "stop_reason": None,
                        "stop_sequence": None,
                        "usage": {"input_tokens": input_tokens, "output_tokens": 0},
                    },
                }
            )

            infer_start = time.perf_counter()
            completion_text = run_inference(
                prompt,
                max_tokens=body.max_tokens,
                temperature=body.temperature,
                request_id=request_id,
            )
            infer_ms = (time.perf_counter() - infer_start) * 1000
            logger.debug(f"[{request_id}] RESPONSE:\n{completion_text}")
            blocks = parse_assistant_completion_to_content_blocks(completion_text)
            has_tool = any(isinstance(b, AnthropicToolUseBlock) for b in blocks)
            logger.info(
                "anthropic_messages stream_inference_done request_id=%s infer_ms=%.1f chars=%d blocks=%d tool_use=%s",
                request_id,
                infer_ms,
                len(completion_text),
                len(blocks),
                has_tool,
            )

            idx = 0
            for block in blocks:
                if isinstance(block, AnthropicTextBlock):
                    yield sse(
                        "content_block_start",
                        {
                            "type": "content_block_start",
                            "index": idx,
                            "content_block": {"type": "text", "text": ""},
                        },
                    )
                    yield sse(
                        "content_block_delta",
                        {
                            "type": "content_block_delta",
                            "index": idx,
                            "delta": {"type": "text_delta", "text": block.text},
                        },
                    )
                    yield sse("content_block_stop", {"type": "content_block_stop", "index": idx})
                    idx += 1
                else:
                    yield sse(
                        "content_block_start",
                        {
                            "type": "content_block_start",
                            "index": idx,
                            "content_block": {
                                "type": "tool_use",
                                "id": block.id,
                                "name": block.name,
                                "input": block.input,
                            },
                        },
                    )
                    yield sse("content_block_stop", {"type": "content_block_stop", "index": idx})
                    idx += 1

            output_tokens = approx_tokens(completion_text)
            stop = "tool_use" if has_tool else "end_turn"
            # message_delta (stop_reason + usage)
            yield sse(
                "message_delta",
                {
                    "type": "message_delta",
                    "delta": {"stop_reason": stop, "stop_sequence": None},
                    "usage": {"output_tokens": output_tokens},
                },
            )
            # message_stop
            yield sse("message_stop", {"type": "message_stop"})
            logger.info(
                "anthropic_messages stream_done request_id=%s total_elapsed=%.2fs",
                request_id,
                time.time() - request_start,
            )

        return StreamingResponse(event_stream(), media_type="text/event-stream")

    infer_start = time.perf_counter()
    completion_text = run_inference(
        prompt,
        max_tokens=body.max_tokens,
        temperature=body.temperature,
        request_id=request_id,
    )
    infer_ms = (time.perf_counter() - infer_start) * 1000
    logger.debug(f"[{request_id}] RESPONSE:\n{completion_text}")
    blocks = parse_assistant_completion_to_content_blocks(completion_text)
    has_tool = any(isinstance(b, AnthropicToolUseBlock) for b in blocks)
    logger.info(
        "anthropic_messages nonstream_done request_id=%s infer_ms=%.1f total_ms=%.1f chars=%d blocks=%d tool_use=%s",
        request_id,
        infer_ms,
        (time.perf_counter() - request_start) * 1000,
        len(completion_text),
        len(blocks),
        has_tool,
    )

    output_tokens = approx_tokens(completion_text)
    usage = AnthropicUsage(input_tokens=input_tokens, output_tokens=output_tokens)
    stop = "tool_use" if has_tool else "end_turn"
    response = AnthropicMessageResponse(
        id=f"msg-{uuid.uuid4().hex}",
        model=body.model,
        content=blocks,
        stop_reason=stop,
        stop_sequence=None,
        usage=usage,
    )
    return response


@app.post("/v1/chat/completions", response_model=ChatCompletionResponse)
def chat_completions(body: ChatCompletionRequest) -> ChatCompletionResponse:
    request_id = uuid.uuid4().hex[:8]
    request_start = time.time()
    logger.info(
        "chat_completions start request_id=%s model=%s messages=%d max_tokens=%s temp=%s",
        request_id,
        body.model,
        len(body.messages),
        body.max_tokens,
        body.temperature,
    )
    # Simple strategy: join all messages into a single prompt, keeping roles.
    prompt_parts = [f"{m.role}: {m.content}" for m in body.messages]
    prompt = "\n".join(prompt_parts) + "\nassistant:"
    prompt = _truncate_prompt(prompt, request_id)
    logger.debug(f"[{request_id}] PROMPT:\n{prompt}")

    start = time.time()
    completion_text = run_inference(
        prompt,
        max_tokens=body.max_tokens,
        temperature=body.temperature,
        request_id=request_id,
    )
    elapsed = time.time() - start
    logger.debug(f"[{request_id}] RESPONSE:\n{completion_text}")
    logger.info(
        "chat_completions done request_id=%s infer_elapsed=%.2fs total_elapsed=%.2fs chars=%d",
        request_id,
        elapsed,
        time.time() - request_start,
        len(completion_text),
    )

    message = ChatCompletionChoiceMessage(content=completion_text)
    choice = ChatCompletionChoice(index=0, message=message)

    response = ChatCompletionResponse(
        id=f"chatcmpl-{uuid.uuid4().hex}",
        created=int(time.time()),
        model=body.model,
        choices=[choice],
        usage=None,
    )
    return response
