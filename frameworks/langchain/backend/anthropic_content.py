"""
Normalize Anthropic Messages API content to/from our local MLX text bridge.

Never drops tool_use, tool_result, server_tool_use, or other structured blocks
when building the prompt. Optionally parses model text into tool_use blocks
for the assistant response when the model follows common patterns.
"""

from __future__ import annotations

import json
import re
import uuid
from typing import Any, List, Optional, Union

from .schemas import AnthropicTextBlock, AnthropicToolUseBlock

AssistantBlock = Union[AnthropicTextBlock, AnthropicToolUseBlock]


def serialize_anthropic_block(block: Any) -> str:
    """Turn one content block into a string line for the local model."""
    if isinstance(block, AnthropicTextBlock):
        return block.text
    if isinstance(block, dict):
        if block.get("type") == "text" and isinstance(block.get("text"), str):
            return block["text"]
        return json.dumps(block, ensure_ascii=False)
    return json.dumps(block, default=str, ensure_ascii=False)


def message_content_to_prompt_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        lines = [serialize_anthropic_block(b) for b in content]
        return "\n".join(lines)
    return str(content)


def system_to_prompt_prefix(system: Any) -> List[str]:
    if isinstance(system, str):
        return [f"system: {system}"]
    if isinstance(system, list):
        lines = [serialize_anthropic_block(b) for b in system]
        return ["system: " + "\n".join(lines)] if lines else []
    return []


def extract_tag(text: str, tag: str) -> Optional[str]:
    start = f"<{tag}>"
    end = f"</{tag}>"
    i = text.find(start)
    if i < 0:
        return None
    j = text.find(end, i + len(start))
    if j < 0:
        return None
    return text[i + len(start) : j].strip()


def _coerce_tool_input(raw_in: Any) -> dict[str, Any]:
    if raw_in is None:
        return {}
    if isinstance(raw_in, dict):
        return raw_in
    return {"args": str(raw_in)}


def json_obj_to_tool_use_block(obj: dict[str, Any]) -> Optional[AnthropicToolUseBlock]:
    """
    Map JSON from the model into an Anthropic tool_use block.

    Supports:
    - Native Anthropic shape: type tool_use + name + input
    - Common alternate: name + arguments | input | args
    - Claude Code skill line: skill + args (args often a string)
    """
    if obj.get("type") == "tool_use":
        return _dict_to_tool_use_block(obj)

    name: Optional[str] = obj.get("name") if isinstance(obj.get("name"), str) else None
    if isinstance(obj.get("skill"), str):
        name = obj["skill"]
    if not name:
        return None

    has_payload = any(k in obj for k in ("arguments", "input", "args"))
    if name == obj.get("name") and not has_payload:
        # Plain {"name": "x"} with no args — not a tool call.
        return None

    tid = obj.get("id")
    if not isinstance(tid, str) or not tid:
        tid = f"toolu_{uuid.uuid4().hex[:24]}"
    raw_in = obj.get("arguments")
    if raw_in is None:
        raw_in = obj.get("input")
    if raw_in is None:
        raw_in = obj.get("args")
    input_ = _coerce_tool_input(raw_in)
    return AnthropicToolUseBlock(id=tid, name=name, input=input_)


def _tool_payload_to_block(payload: str) -> Optional[AnthropicToolUseBlock]:
    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        return None
    if not isinstance(data, dict):
        return None
    return json_obj_to_tool_use_block(data)


def _dict_to_tool_use_block(obj: dict[str, Any]) -> Optional[AnthropicToolUseBlock]:
    name = obj.get("name")
    if not isinstance(name, str):
        return None
    tid = obj.get("id")
    if not isinstance(tid, str) or not tid:
        tid = f"toolu_{uuid.uuid4().hex[:24]}"
    inp = obj.get("input")
    if not isinstance(inp, dict):
        inp = {}
    return AnthropicToolUseBlock(id=tid, name=name, input=inp)


def _split_blocks_around_tool(
    text: str, start: int, end: int, block: AnthropicToolUseBlock
) -> List[AssistantBlock]:
    before = text[:start].strip()
    after = text[end:].strip()
    out: List[AssistantBlock] = []
    if before:
        out.append(AnthropicTextBlock(text=before))
    out.append(block)
    if after:
        out.append(AnthropicTextBlock(text=after))
    return out


def _tool_blocks_from_embedded_json_objects(text: str) -> Optional[List[AssistantBlock]]:
    """Handle prose followed by a JSON tool/skill object (no ``` fence)."""
    pos = 0
    decoder = json.JSONDecoder()
    while True:
        start = text.find("{", pos)
        if start < 0:
            return None
        try:
            obj, end = decoder.raw_decode(text, start)
        except json.JSONDecodeError:
            pos = start + 1
            continue
        if isinstance(obj, dict):
            b = json_obj_to_tool_use_block(obj)
            if b is not None:
                return _split_blocks_around_tool(text, start, end, b)
        pos = start + 1


def parse_assistant_completion_to_content_blocks(text: str) -> List[AssistantBlock]:
    """
    Map raw model output to Anthropic-shaped assistant content blocks.

    If nothing matches, returns a single text block (full string).
    """
    for m in _JSON_FENCE.finditer(text):
        inner = m.group(1).strip()
        try:
            obj = json.loads(inner)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            b = json_obj_to_tool_use_block(obj)
            if b is not None:
                before = text[: m.start()].strip()
                after = text[m.end() :].strip()
                out_fence: List[AssistantBlock] = []
                if before:
                    out_fence.append(AnthropicTextBlock(text=before))
                out_fence.append(b)
                if after:
                    out_fence.append(AnthropicTextBlock(text=after))
                return out_fence
        if isinstance(obj, list):
            out3: List[AssistantBlock] = []
            for item in obj:
                if not isinstance(item, dict):
                    continue
                b2 = json_obj_to_tool_use_block(item)
                if b2 is not None:
                    out3.append(b2)
                elif item.get("type") == "text" and isinstance(item.get("text"), str):
                    out3.append(AnthropicTextBlock(text=item["text"]))
            if out3:
                return out3

    tc = extract_tag(text, "tool_call")
    if tc:
        block = _tool_payload_to_block(tc)
        if block is not None:
            out: List[AssistantBlock] = []
            before = text[: text.find("<tool_call>")].strip()
            if before:
                out.append(AnthropicTextBlock(text=before))
            out.append(block)
            end_i = text.find("</tool_call>")
            if end_i >= 0:
                remainder = text[end_i + len("</tool_call>") :].strip()
                if remainder:
                    out.append(AnthropicTextBlock(text=remainder))
            return out

    trimmed = text.strip()
    if trimmed.startswith("{"):
        try:
            obj = json.loads(trimmed)
            if isinstance(obj, dict):
                b = json_obj_to_tool_use_block(obj)
                if b is not None:
                    return [b]
        except json.JSONDecodeError:
            pass

    if trimmed.startswith("["):
        try:
            arr = json.loads(trimmed)
            if isinstance(arr, list) and arr:
                out2: List[AssistantBlock] = []
                for item in arr:
                    if not isinstance(item, dict):
                        continue
                    b2 = json_obj_to_tool_use_block(item)
                    if b2 is not None:
                        out2.append(b2)
                    elif item.get("type") == "text" and isinstance(item.get("text"), str):
                        out2.append(AnthropicTextBlock(text=item["text"]))
                if out2:
                    return out2
        except json.JSONDecodeError:
            pass

    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        if "tool_use" not in line and "skill" not in line and '"name"' not in line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            b = json_obj_to_tool_use_block(obj)
            if b is not None:
                return [b]

    embedded = _tool_blocks_from_embedded_json_objects(text)
    if embedded is not None:
        return embedded

    return [AnthropicTextBlock(text=text)]


# Find ```json ... ``` with a tool_use object
_JSON_FENCE = re.compile(r"```(?:json)?\s*([\s\S]*?)```", re.MULTILINE)
