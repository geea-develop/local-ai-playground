"""
Local tool-calling loop with `mlx_lm`, with (optional) LangChain tool wrappers.

How it works:
1. Ask the model to emit a `<tool_call>...</tool_call>` block when it wants to use a tool.
2. Parse that tool call JSON, execute the referenced local Python tool.
3. Feed the tool result back to the model as the next "human" message.
4. Repeat until the model emits `<final>...</final>`.

Why parsing is still required:
`mlx_lm` (and LLMs in general) only return generated *text tokens* to Python.
To execute the right local function, we must convert that text back into:
`tool_name`
`arguments` (a dict)
So even with a "structured output" instruction, we still parse the `<tool_call>...</tool_call>` payload.
"""

import ast
import json
import logging
import os
import re
import sys
import time
from typing import Any, Callable, Dict, List, Optional, Tuple

import mlx_lm as mlx
from dotenv import load_dotenv

# LangChain is optional here: we use it only for the "tool" abstraction.
# If LangChain isn't installed, the example falls back to plain Python functions.
try:
    from langchain_core.tools import tool as lc_tool  # type: ignore
except Exception:  # pragma: no cover
    lc_tool = None


logger = logging.getLogger(__name__)


def tool_decorator(fn: Callable) -> Callable:
    """
    Wrap a Python function as a LangChain tool if available.

    LangChain is optional in this repo; if it isn't installed, we keep the
    plain function and attach a `.name` attribute for compatibility.
    """

    if lc_tool is None:
        # Provide a compatible `.name` attribute so we can build a tool map.
        setattr(fn, "name", fn.__name__)
        return fn
    return lc_tool(fn)  # type: ignore[misc]


def invoke_tool(tool_obj: Callable, tool_args: Dict[str, Any]) -> Any:
    """Invoke either a LangChain tool or a plain Python function."""

    # LangChain tools generally expose `.invoke(...)`.
    if hasattr(tool_obj, "invoke"):
        return tool_obj.invoke(tool_args)  # type: ignore[no-any-return]
    return tool_obj(**tool_args)


def extract_tag(text: str, tag: str) -> Optional[str]:
    """Extract the first <tag>...</tag> block contents."""

    m = re.search(rf"<{re.escape(tag)}>\s*(.*?)\s*</{re.escape(tag)}>", text, flags=re.DOTALL)
    return m.group(1) if m else None


def strip_think_tags(text: str) -> str:
    """Remove optional <think>...</think> sections before parsing tags."""
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


def parse_tool_call_payload(payload_str: str) -> Dict[str, Any]:
    """
    Parse the JSON payload inside <tool_call>...</tool_call>.

    Expected format:
      {"name": "...", "arguments": {...}}

Implementation notes:
    We try `json.loads()` first (fast path).
    If the model includes surrounding prose/markers, we fall back to extracting the
    first balanced `{ ... }` object and parsing that.
    There are additional "JSON-ish" recovery attempts for robustness.

If you want maximum speed, you can make this parser stricter (e.g. remove fallbacks),
but that will make the example more brittle when the model output deviates slightly.
    """

    s = payload_str.strip()

    # First try strict JSON.
    try:
        data = json.loads(s)
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError:
        pass

    # If the model included extra chat markers/prose around the JSON, extract
    # the first balanced `{ ... }` object and parse that.
    json_obj_str = extract_first_balanced_json_object(s)
    if json_obj_str:
        try:
            data = json.loads(json_obj_str)
            if isinstance(data, dict):
                return data
        except Exception:
            pass

        try:
            s2 = json_obj_str.replace("null", "None").replace("true", "True").replace("false", "False")
            data = ast.literal_eval(s2)
            if isinstance(data, dict):
                return data
        except Exception:
            pass

    # Then try to recover common "JSON-ish" variants via Python literals.
    try:
        # Normalize JSON literals to Python.
        s2 = s.replace("null", "None").replace("true", "True").replace("false", "False")
        data = ast.literal_eval(s2)
        if isinstance(data, dict):
            return data
    except Exception:
        pass

    preview = payload_str.strip().replace("\n", "\\n")
    if len(preview) > 300:
        preview = preview[:300] + "...(truncated)"
    raise ValueError(f"Could not parse tool_call payload as JSON: {preview!r}")


def extract_first_balanced_json_object(text: str) -> Optional[str]:
    """
    Extract the first balanced JSON object from `text`.

    This is a small heuristic for cases where the model emits:
      {"name": "...", "arguments": {...}}
    without surrounding `<tool_call>...</tool_call>` tags.

    This is intentionally heuristic (best-effort) rather than strict schema parsing.
    It helps recover from imperfect model formatting, but it is heavier than a
    simple tag-extract + `json.loads`.
    """

    # Prefer an object that looks like the expected tool payload.
    # We intentionally don't require exact formatting like `{"name": ...}`.
    name_idx = text.find('"name"')
    if name_idx == -1:
        return None

    start = text.rfind("{", 0, name_idx)
    if start == -1:
        return None

    depth = 0
    in_str = False
    escape = False

    for i in range(start, len(text)):
        ch = text[i]

        if in_str:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_str = False
            continue

        if ch == '"':
            in_str = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                candidate = text[start : i + 1]
                # Quick validation: parse via our existing parser.
                try:
                    json.loads(candidate)
                except Exception:
                    # Fallback: allow JSON-ish strings via parse_tool_call_payload later.
                    return candidate
                return candidate

    return None


def extract_tool_call_payload_any(text: str) -> Optional[Dict[str, Any]]:
    """
    Extract tool_call payload dict from either:
    - `<tool_call>{...}</tool_call>` tags, or
    - a raw JSON object in the output.

    This helper is intentionally tolerant because some templates/models may omit the
    exact wrapper tags. In the streaming loop (`mlx_generate_completion`) we gate
    when this function is called to keep latency down.
    """

    tool_call_payload = extract_tag(text, "tool_call")
    if tool_call_payload:
        return parse_tool_call_payload(tool_call_payload)

    json_obj = extract_first_balanced_json_object(text)
    if json_obj:
        payload = parse_tool_call_payload(json_obj)
        # Basic shape validation.
        if (
            isinstance(payload, dict)
            and (payload.get("name") or payload.get("function") or payload.get("tool"))
        ):
            return payload

    return None


def normalize_tool_call(payload: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    """Extract `(tool_name, arguments_dict)` from the parsed payload."""
    name = payload.get("name") or payload.get("function") or payload.get("tool")  # type: ignore[assignment]
    if not name or not isinstance(name, str):
        raise ValueError(f"tool_call payload missing string 'name': {payload!r}")

    args = payload.get("arguments") or payload.get("args") or payload.get("parameters")
    if args is None:
        args = {}
    if not isinstance(args, dict):
        raise ValueError(f"tool_call 'arguments' must be an object: {payload!r}")

    return name, args


def get_tool_name(tool_obj: Any) -> str:
    """
    Get a tool's name in a way that works for both:
    - plain Python functions (has `__name__`)
    - LangChain tools/StructuredTool (typically has `.name`)
    """

    name = getattr(tool_obj, "name", None)
    if isinstance(name, str) and name:
        return name

    name = getattr(tool_obj, "__name__", None)
    if isinstance(name, str) and name:
        return name

    raise ValueError(f"Could not determine tool name for object: {tool_obj!r}")


def build_prompt_messages(
    *,
    user_query: str,
    tool_defs_json: str,
    messages: Optional[List[Dict[str, str]]] = None,
) -> List[Dict[str, str]]:
    """
    Create the initial messages that instruct the model to tool-call.

    Using a `system` message keeps the tool contract separate from the actual user query,
    which is usually a more reliable structure for tool calling and code generation.
    """

    system_content = (
        "You are a function calling AI model.\n"
        "You are provided with function signatures within <tools></tools> XML tags.\n"
        "If you need to use a tool, output ONLY a single <tool_call>...</tool_call> block.\n"
        "The contents of <tool_call> must be a JSON object with this shape:\n"
        '{"name": "<tool_name>", "arguments": { ... }}\n'
        "You may optionally include an internal planning section wrapped in <think>...</think>.\n"
        "When you have enough information to answer the user, output ONLY a single <final>...</final> block.\n\n"
        f"Here are the available tools:<tools> {tool_defs_json} </tools>\n"
    )

    if messages is None:
        return [
            {"role": "system", "content": system_content},
            {"role": "human", "content": user_query},
        ]

    return messages


def build_tool_result_human_turn(tool_name: str, tool_result: Any) -> str:
    """Render the tool result back into the conversation."""
    return (
        "Tool execution result:\n"
        f"{tool_name} -> {tool_result}\n\n"
        "Continue the conversation.\n"
        "If you have enough information, output ONLY <final>...</final>.\n"
        "Otherwise, you may output another <tool_call>...</tool_call>."
    )


def mlx_generate_completion(
    *,
    model: Any,
    tokenizer: Any,
    prompt: str,
    max_tokens: int = 600,
) -> str:
    """
    Generate until we have enough structure to continue the loop.

    We stream and stop early when:
      - a `<final>...</final>` block is present, or
      - a parsable tool-call payload is detected.

    Latency note:
    Tool-call parsing is comparatively expensive (regex + JSON extraction).
    To keep streaming "early stop" effective, we avoid running the full parser on
    every single chunk; instead we only attempt parsing when the buffer has likely
    reached a complete `</tool_call>` (or when a likely JSON payload appears).
    """

    def try_parse_tool_call(text: str) -> Optional[Dict[str, Any]]:
        try:
            return extract_tool_call_payload_any(text)
        except Exception:
            return None

    tic = time.perf_counter()
    buffer = ""
    stop_reason: Optional[str] = None
    tool_call_parse_attempts = 0

    # `stream_generate` yields only newly generated text (not the prompt),
    # so we don't need to strip a prompt prefix here.
    for resp in mlx.stream_generate(
        model,
        tokenizer,
        prompt=prompt,
        verbose=False,
        max_tokens=max_tokens,
    ):
        chunk = resp.text or ""
        buffer += chunk

        # Fast path: avoid regex passes on every chunk.
        # We only stop when we see a complete `<final>...</final>` block.
        if "<final>" in buffer and "</final>" in buffer:
            stop_reason = "final_tag"
            break

        # Tool-call parsing is comparatively expensive (regex + JSON extraction),
        # so gate it behind either:
        #   - the presence of the closing `</tool_call>` tag, or
        #   - a likely raw JSON payload (contains `"name"`).
        if tool_call_parse_attempts < 2 and stop_reason is None:
            should_attempt_parse = ("</tool_call>" in buffer) or ('"name"' in buffer)
            if should_attempt_parse:
                tool_call_parse_attempts += 1
                cleaned = strip_think_tags(buffer)
                if try_parse_tool_call(cleaned) is not None:
                    stop_reason = "tool_call_parsed"
                    break

    elapsed = time.perf_counter() - tic
    logger.info(
        "mlx.stream_generate elapsed=%.2fs max_tokens=%s stop_reason=%s output_chars=%s",
        elapsed,
        max_tokens,
        stop_reason,
        len(buffer),
    )
    logger.debug("mlx.stream_generate stop_reason=%s (tool_call_parse_attempts=%s)", stop_reason, tool_call_parse_attempts)
    return buffer


def configure_logging() -> None:
    """Configure consistent logging for local debugging."""

    # Example: LOG_LEVEL=DEBUG python ...
    level_name = os.getenv("LOG_LEVEL", "INFO").upper().strip()
    level = getattr(logging, level_name, logging.INFO)

    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


def run_tool_call_loop(user_query: str) -> None:
    """
    Run a local tool-calling loop until `<final>` is produced.

    This is intentionally "no server / no API": tool calls execute locally in Python.
    """

    configure_logging()
    load_dotenv()

    models_dir = os.getenv("MODELS_DIR_PATH")
    model_dir = os.getenv("MODEL_DIR_PATH")
    if not models_dir or not model_dir:
        raise ValueError("Missing MODELS_DIR_PATH or MODEL_DIR_PATH in .env")

    model_dir_path = os.path.join(models_dir, model_dir)
    logger.info("Targeting model from .env: %s", model_dir_path)

    tic_load = time.perf_counter()
    model, tokenizer = mlx.load(model_dir_path)
    logger.info("Model load elapsed=%.2fs", time.perf_counter() - tic_load)

    # Tool-calling friendly fallback template.
    # This supports system/human/model roles so we can keep the tool contract in `system`.
    tokenizer.chat_template = (
        "{{ bos_token }}"
        "{% for message in messages %}"
        "{{ '<start_of_turn>' + message['role'] + '\\n' + message['content'] | trim + '<end_of_turn><eos>\\n' }}"
        "{% endfor %}"
        "{% if add_generation_prompt %}{{'<start_of_turn>model\\n'}}{% endif %}"
    )

    # ---- Tool functions (these are "local" Python tools; no external API calls). ----
    @tool_decorator
    def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
        """
        Convert currency using a tiny built-in rate table (demo only, not real FX).
        """

        rates = {
            # Base currency: USD
            "USD": 1.0,
            "EUR": 0.92,
            "GBP": 0.79,
            "JPY": 155.0,
        }

        from_currency = from_currency.upper().strip()
        to_currency = to_currency.upper().strip()
        if from_currency not in rates or to_currency not in rates:
            return f"Unsupported currency pair ({from_currency} -> {to_currency}) in demo rates."

        # Convert: amount in from_currency -> USD -> to_currency
        usd_amount = amount / rates[from_currency]
        target_amount = usd_amount * rates[to_currency]
        return f"{amount} {from_currency} ~= {target_amount:.2f} {to_currency}"

    # Very small city->(lat,lon) mapping for deterministic demo.
    _city_coords = {
        "san francisco": (37.7749, -122.4194),
        "new york": (40.7128, -74.0060),
        "los angeles": (34.0522, -118.2437),
        "london": (51.5074, -0.1278),
    }

    def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        from math import asin, cos, radians, sin, sqrt

        R = 6371.0  # Earth radius in km
        d_lat = radians(lat2 - lat1)
        d_lon = radians(lon2 - lon1)
        a = sin(d_lat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lon / 2) ** 2
        c = 2 * asin(sqrt(a))
        return R * c

    @tool_decorator
    def calculate_distance(start_location: str, end_location: str) -> str:
        """Calculate approximate distance between two known demo cities in km."""

        s = start_location.lower().strip()
        e = end_location.lower().strip()
        if s not in _city_coords or e not in _city_coords:
            return "Unknown locations for demo. Try: San Francisco, New York, Los Angeles, London."

        lat1, lon1 = _city_coords[s]
        lat2, lon2 = _city_coords[e]
        km = _haversine_km(lat1, lon1, lat2, lon2)
        return f"Approx distance between {start_location} and {end_location}: {km:.1f} km"

    tools = [convert_currency, calculate_distance]
    tools_by_name = {get_tool_name(t): t for t in tools}

    # ---- Tool schema for the model prompt (JSON Schema-ish). ----
    tool_defs = [
        {
            "type": "function",
            "function": {
                "name": "convert_currency",
                "description": "Convert from one currency to another (demo rates).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "amount": {"type": "number"},
                        "from_currency": {"type": "string"},
                        "to_currency": {"type": "string"},
                    },
                    "required": ["amount", "from_currency", "to_currency"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "calculate_distance",
                "description": "Calculate the distance between two locations (demo city mapping).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "start_location": {"type": "string"},
                        "end_location": {"type": "string"},
                    },
                    "required": ["start_location", "end_location"],
                },
            },
        },
    ]
    tool_defs_json = json.dumps(tool_defs)

    messages: List[Dict[str, str]] = build_prompt_messages(
        user_query=user_query,
        tool_defs_json=tool_defs_json,
        messages=None,
    )

    logger.debug("Initial user query: %s", user_query)

    max_rounds = 6
    for round_idx in range(max_rounds):
        logger.info("Round %s/%s", round_idx + 1, max_rounds)

        prompt = tokenizer.apply_chat_template(messages, add_generation_prompt=True, tokenize=False)

        assistant_text = mlx_generate_completion(
            model=model,
            tokenizer=tokenizer,
            prompt=prompt,
            max_tokens=256,
        )
        assistant_text = str(assistant_text)

        cleaned = strip_think_tags(assistant_text)
        if logger.isEnabledFor(logging.DEBUG):
            preview = cleaned[:1500] + ("...(truncated)" if len(cleaned) > 1500 else "")
            logger.debug("Raw model output (post <think> strip, truncated): %s", preview)

        payload = extract_tool_call_payload_any(cleaned)
        if payload:
            # Avoid prompt bloat: the model's raw output often includes extra chat markers
            # and repeated tool-call JSON. We only feed the parsed tool_call back.
            messages.append(
                {
                    "role": "model",
                    "content": f"<tool_call>\n{json.dumps(payload)}\n</tool_call>",
                }
            )

            tool_name, tool_args = normalize_tool_call(payload)

            logger.info("Parsed tool call: %s args=%s", tool_name, tool_args)

            tool_obj = tools_by_name.get(tool_name)
            if tool_obj is None:
                tool_result = f"Tool '{tool_name}' not found."
            else:
                tool_result = invoke_tool(tool_obj, tool_args)

            logger.debug("Tool result: %s", tool_result)

            # Feed tool result back into the conversation.
            messages.append(
                {"role": "human", "content": build_tool_result_human_turn(tool_name, tool_result)}
            )
            continue

        final_answer = extract_tag(cleaned, "final")
        if final_answer:
            final_answer = final_answer.strip()
            logger.info("Model returned <final>.")
            print(final_answer)
            return

        # If we didn't get a tool_call or final block, stop with the raw output.
        logger.warning("Model did not return <tool_call> or <final>. Stopping.")
        # Print the raw output to help you adjust the prompt/template.
        print("Model did not return <tool_call> or <final>. Raw output:\n")
        print(assistant_text)
        return

    logger.warning("Reached max_rounds without producing <final>.")
    print("Reached max_rounds without producing <final>. Last model output:\n")
    print(messages[-1]["content"])


if __name__ == "__main__":
    # Example: currency conversion (uses the demo USD->EUR rate table).
    #
    # Usage:
    #   LOG_LEVEL=DEBUG python mlx_lm_langchain_tool_call_example.py
    #   LOG_LEVEL=INFO  python mlx_lm_langchain_tool_call_example.py "Convert 500 USD to EUR"
    query = sys.argv[1] if len(sys.argv) > 1 else "Convert 500 USD to EUR. Then explain the result briefly."
    run_tool_call_loop(query)

