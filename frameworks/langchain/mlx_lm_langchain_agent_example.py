"""
LangChain-style tool-calling example using `mlx_lm` locally.

This mirrors `langchain_agent_example.py` conceptually:
- Define a local LangChain tool (no network calls).
- Ask a question.
- Have the model emit a structured tool call.
- Execute the tool locally.
- Feed the result back and ask for the final answer.

Unlike the llama-cpp LangChain wrapper, `mlx_lm` doesn't provide a drop-in
`bind_tools()` interface, so this script uses a small prompt + parsing loop.
"""

from __future__ import annotations

import ast
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional

import mlx_lm as mlx
from dotenv import load_dotenv
from langchain.tools import tool


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

    The prompt encourages strict JSON, but includes a small fallback for
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
        raise ValueError(f"tool_call payload must be a dict, got: {type(data)}")
    return data


def mlx_generate_until_tags(
    *,
    model: Any,
    tokenizer: Any,
    prompt: str,
    max_tokens: int = 256,
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


def build_tool_result_turn(tool_name: str, tool_result: Any) -> str:
    return (
        "Tool execution result:\n"
        f"{tool_name} -> {tool_result}\n\n"
        "Continue the conversation.\n"
        "If you have enough information, output ONLY <final>...</final>.\n"
        "Otherwise, you may output another <tool_call>...</tool_call>."
    )


@tool
def validate_user(user_id: int, addresses: List[str]) -> bool:
    """
    Validate user using historical addresses.

    Args:
        user_id: the user ID.
        addresses: Previous addresses as a list of strings.
    """
    # Demo tool: always returns True.
    return True


def run_agent(query: str) -> None:
    load_dotenv()

    models_dir = os.getenv("MODELS_DIR_PATH")
    model_dir = os.getenv("MODEL_DIR_PATH")
    if not models_dir or not model_dir:
        raise ValueError("Missing MODELS_DIR_PATH or MODEL_DIR_PATH in .env")

    model_dir_path = os.path.join(models_dir, model_dir)
    print(f"Targeting model from .env: {model_dir_path}\n")

    model, tokenizer = mlx.load(model_dir_path)

    # Tool-calling friendly chat template (supports system/human/model roles).
    # Copied from the existing MLX example to match the same tokenizer expectations.
    tokenizer.chat_template = (
        "{{ bos_token }}"
        "{% for message in messages %}"
        "{{ '<start_of_turn>' + message['role'] + '\\n' + message['content'] | trim + '<end_of_turn><eos>\\n' }}"
        "{% endfor %}"
        "{% if add_generation_prompt %}{{'<start_of_turn>model\\n'}}{% endif %}"
    )

    tool_defs = [
        {
            "type": "function",
            "function": {
                "name": "validate_user",
                "description": "Validate user using historical addresses.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "integer"},
                        "addresses": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                    },
                    "required": ["user_id", "addresses"],
                },
            },
        }
    ]
    system_prompt = build_system_prompt(tool_defs_json=json.dumps(tool_defs))

    tools_by_name = {
        "validate_user": validate_user,
    }

    messages: List[Dict[str, str]] = [
        {"role": "system", "content": system_prompt},
        {"role": "human", "content": query},
    ]

    # 1) Ask for a tool call (or final).
    prompt = tokenizer.apply_chat_template(messages, add_generation_prompt=True, tokenize=False)
    assistant_text = mlx_generate_until_tags(
        model=model,
        tokenizer=tokenizer,
        prompt=prompt,
        max_tokens=256,
    )
    cleaned = strip_think_tags(str(assistant_text))

    tool_call_payload_str = extract_tag(cleaned, "tool_call")
    final_answer = extract_tag(cleaned, "final")

    # If the model answers immediately, just print it.
    if final_answer:
        print(final_answer.strip())
        return

    if not tool_call_payload_str:
        print("Model did not return <tool_call> or <final>.\n")
        print("Raw model output:\n")
        print(assistant_text)
        return

    payload = parse_tool_call_payload(tool_call_payload_str)
    tool_name = payload.get("name")
    tool_args = payload.get("arguments") or payload.get("args") or {}

    if not isinstance(tool_name, str):
        raise ValueError(f"tool_call payload missing string 'name': {payload!r}")
    if not isinstance(tool_args, dict):
        raise ValueError(f"tool_call payload 'arguments' must be an object: {payload!r}")

    # Be defensive about minor shape mismatches from the model.
    # (e.g., `addresses` sometimes comes back as a single string.)
    if "user_id" in tool_args and isinstance(tool_args["user_id"], str):
        s = tool_args["user_id"].strip()
        if s.isdigit():
            tool_args["user_id"] = int(s)

    if "addresses" in tool_args:
        addresses = tool_args["addresses"]
        if isinstance(addresses, str):
            addr_s = addresses.strip()
            if addr_s.startswith("[") and addr_s.endswith("]"):
                try:
                    parsed = json.loads(addr_s)
                    if isinstance(parsed, list):
                        tool_args["addresses"] = parsed
                except json.JSONDecodeError:
                    pass
            if isinstance(tool_args.get("addresses"), str):
                # Simple fallback: split on commas.
                tool_args["addresses"] = [a.strip() for a in addr_s.split(",") if a.strip()]

    print("Parsed tool call:")
    print(json.dumps({"name": tool_name, "arguments": tool_args}, indent=2))

    tool_obj = tools_by_name.get(tool_name)
    if tool_obj is None:
        tool_result: Any = f"Tool '{tool_name}' not found."
    else:
        tool_result = tool_obj.invoke(tool_args)

    # 2) Feed tool result back, ask for final.
    messages.append(
        {
            "role": "model",
            "content": f"<tool_call>\n{json.dumps({'name': tool_name, 'arguments': tool_args})}\n</tool_call>",
        }
    )
    messages.append(
        {"role": "human", "content": build_tool_result_turn(tool_name, tool_result)}
    )

    final_prompt = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True, tokenize=False
    )
    final_text = mlx_generate_until_tags(
        model=model,
        tokenizer=tokenizer,
        prompt=final_prompt,
        max_tokens=256,
    )
    final_cleaned = strip_think_tags(str(final_text))
    final_answer2 = extract_tag(final_cleaned, "final")

    if final_answer2:
        print("\nFinal answer:")
        print(final_answer2.strip())
        return

    print("\nModel did not return <final>. Raw output:\n")
    print(final_text)


if __name__ == "__main__":
    query = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "Could you validate user 123? They previously lived at 123 Fake St in Boston MA and 234 Pretend Boulevard in Houston TX."
    )
    run_agent(query)

