"""
Simple local tool-calling "agent" loop with `mlx_lm`.

This keeps the flow deliberately small and clear:
1) The model emits exactly one `<tool_call>...</tool_call>` block (JSON).
2) Python executes the referenced local tool.
3) Tool result is fed back to the model.
4) The model continues until it emits a `<final>...</final>` block.

Tools in this example are fully local (no network calls).
"""

from __future__ import annotations

import ast
import json
import logging
import os
import re
import sys
from typing import Any, Dict, Optional

import mlx_lm as mlx
from dotenv import load_dotenv

from langchain.tools import tool

logger = logging.getLogger(__name__)

RATES: dict[str, float] = {
    "USD": 1.0,
    "EUR": 0.92,
    "GBP": 0.79,
    "JPY": 155.0,
}

CITY_COORDS: dict[str, tuple[float, float]] = {
    "san francisco": (37.7749, -122.4194),
    "new york": (40.7128, -74.0060),
    "los angeles": (34.0522, -118.2437),
    "london": (51.5074, -0.1278),
}


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Approximate distance between two lat/lon points in kilometers."""
    from math import asin, cos, radians, sin, sqrt

    R = 6371.0  # Earth radius in km
    d_lat = radians(lat2 - lat1)
    d_lon = radians(lon2 - lon1)
    a = sin(d_lat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return R * c


@tool
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """
    Convert currency using demo FX rates.

    Supported: USD, EUR, GBP, JPY.
    """
    from_currency = from_currency.upper().strip()
    to_currency = to_currency.upper().strip()

    if from_currency not in RATES or to_currency not in RATES:
        return (
            f"Unsupported currency pair ({from_currency} -> {to_currency}) in demo rates."
        )

    usd_amount = amount / RATES[from_currency]
    target_amount = usd_amount * RATES[to_currency]
    return f"{amount} {from_currency} ~= {target_amount:.2f} {to_currency}"


@tool
def calculate_distance(start_location: str, end_location: str) -> str:
    """
    Calculate approximate distance between two known demo cities in km.

    Known cities: San Francisco, New York, Los Angeles, London.
    """
    s = start_location.lower().strip()
    e = end_location.lower().strip()

    if s not in CITY_COORDS or e not in CITY_COORDS:
        return (
            "Unknown locations for demo. Try: San Francisco, New York, Los Angeles, London."
        )

    lat1, lon1 = CITY_COORDS[s]
    lat2, lon2 = CITY_COORDS[e]
    km = _haversine_km(lat1, lon1, lat2, lon2)
    return f"Approx distance between {start_location} and {end_location}: {km:.1f} km"


def configure_logging() -> None:
    level_name = os.getenv("LOG_LEVEL", "INFO").upper().strip()
    level = getattr(logging, level_name, logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


def extract_tag(text: str, tag: str) -> Optional[str]:
    """Extract the first `<tag>...</tag>` contents."""
    m = re.search(
        rf"<{re.escape(tag)}>\s*(.*?)\s*</{re.escape(tag)}>",
        text,
        flags=re.DOTALL,
    )
    return m.group(1) if m else None


def strip_think_tags(text: str) -> str:
    """Remove optional `<think>...</think>` sections."""
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


def parse_tool_call_payload(payload_str: str) -> Dict[str, Any]:
    """
    Parse the JSON inside `<tool_call>...</tool_call>`.

    The prompt encourages strict JSON, but this includes a tiny fallback for
    common "JSON-ish" outputs (True/False/null).
    """
    s = payload_str.strip()
    try:
        data = json.loads(s)
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError:
        pass

    s2 = s.replace("null", "None").replace("true", "True").replace("false", "False")
    data = ast.literal_eval(s2)
    if not isinstance(data, dict):
        raise ValueError(f"tool_call payload must be a JSON object, got: {type(data)}")
    return data


def mlx_generate_until_tags(
    *, model: Any, tokenizer: Any, prompt: str, max_tokens: int = 256
) -> str:
    """Stream tokens and stop early when `<tool_call>` or `<final>` appears."""
    buffer = ""
    for resp in mlx.stream_generate(
        model,
        tokenizer,
        prompt=prompt,
        max_tokens=max_tokens,
    ):
        chunk = resp.text or ""
        buffer += chunk

        if "<final>" in buffer and "</final>" in buffer:
            break
        if "<tool_call>" in buffer and "</tool_call>" in buffer:
            break

    return buffer


def build_system_prompt(*, tool_defs_json: str) -> str:
    return (
        "You are a function calling AI model.\n"
        "You are provided with function signatures within <tools></tools> XML tags.\n"
        "If you need to use a tool, output ONLY a single <tool_call>...</tool_call> block.\n"
        "The contents of <tool_call> must be a JSON object with this shape:\n"
        '{"name": "<tool_name>", "arguments": { ... }}\n'
        "You may optionally include an internal planning section wrapped in <think>...</think>.\n"
        "When you have enough information to answer the user, output ONLY a single <final>...</final> block.\n\n"
        f"Here are the available tools:<tools> {tool_defs_json} </tools>\n"
    )


# Static tool schema included in the model prompt.
TOOL_DEFS = [
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
SYSTEM_PROMPT = build_system_prompt(tool_defs_json=json.dumps(TOOL_DEFS))


def build_tool_result_turn(tool_name: str, tool_result: Any) -> str:
    return (
        "Tool execution result:\n"
        f"{tool_name} -> {tool_result}\n\n"
        "Continue the conversation.\n"
        "If you have enough information, output ONLY <final>...</final>.\n"
        "Otherwise, you may output another <tool_call>...</tool_call>."
    )


def run_agent(query: str) -> None:
    configure_logging()
    load_dotenv()

    models_dir = os.getenv("MODELS_DIR_PATH")
    model_dir = os.getenv("MODEL_DIR_PATH")
    if not models_dir or not model_dir:
        raise ValueError("Missing MODELS_DIR_PATH or MODEL_DIR_PATH in .env")

    model_dir_path = os.path.join(models_dir, model_dir)
    logger.info("Targeting model from .env: %s", model_dir_path)

    model, tokenizer = mlx.load(model_dir_path)

    # Tool-calling friendly chat template (supports system/human/model roles).
    tokenizer.chat_template = (
        "{{ bos_token }}"
        "{% for message in messages %}"
        "{{ '<start_of_turn>' + message['role'] + '\\n' + message['content'] | trim + '<end_of_turn><eos>\\n' }}"
        "{% endfor %}"
        "{% if add_generation_prompt %}{{'<start_of_turn>model\\n'}}{% endif %}"
    )

    tools_by_name = {
        "convert_currency": convert_currency,
        "calculate_distance": calculate_distance,
    }
    messages: list[Dict[str, str]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "human", "content": query},
    ]

    max_rounds = 4
    for round_idx in range(max_rounds):
        logger.info("Round %s/%s", round_idx + 1, max_rounds)

        prompt = tokenizer.apply_chat_template(
            messages, add_generation_prompt=True, tokenize=False
        )
        assistant_text = mlx_generate_until_tags(
            model=model, tokenizer=tokenizer, prompt=prompt, max_tokens=256
        )
        assistant_text = str(assistant_text)
        cleaned = strip_think_tags(assistant_text)

        tool_call_payload_str = extract_tag(cleaned, "tool_call")
        if tool_call_payload_str:
            payload = parse_tool_call_payload(tool_call_payload_str)
            tool_name = payload.get("name")
            tool_args = (
                payload.get("arguments")
                or payload.get("args")
                or payload.get("parameters")
                or {}
            )
            if not isinstance(tool_name, str):
                raise ValueError(f"tool_call payload missing string 'name': {payload!r}")
            if not isinstance(tool_args, dict):
                raise ValueError(
                    f"tool_call payload 'arguments' must be an object: {payload!r}"
                )

            tool_obj = tools_by_name.get(tool_name)
            if tool_obj is None:
                tool_result = f"Tool '{tool_name}' not found."
            else:
                tool_result = tool_obj.invoke(tool_args)

            # Keep tool feedback compact (just the tool call JSON + the tool result).
            messages.append(
                {
                    "role": "model",
                    "content": f"<tool_call>\n{json.dumps({'name': tool_name, 'arguments': tool_args})}\n</tool_call>",
                }
            )
            messages.append(
                {"role": "human", "content": build_tool_result_turn(tool_name, tool_result)}
            )
            continue

        final_answer = extract_tag(cleaned, "final")
        if final_answer:
            print(final_answer.strip())
            return

        logger.warning("Model did not return <tool_call> or <final>. Stopping.")
        print("Raw model output:\n")
        print(assistant_text)
        return

    logger.warning("Reached max_rounds without producing <final>.")
    print("Last assistant output (truncated):")
    print(cleaned[:1200])


if __name__ == "__main__":
    query = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "Convert 500 USD to EUR, then answer in one sentence."
    )
    run_agent(query)

