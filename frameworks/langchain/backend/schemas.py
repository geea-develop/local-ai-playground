from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"] = Field(...)
    content: str = Field(...)


class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    stream: bool = False
    # extra kwargs are accepted but ignored
    extra: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        extra = "allow"


class ChatCompletionChoiceMessage(BaseModel):
    role: Literal["assistant"] = "assistant"
    content: str


class ChatCompletionChoice(BaseModel):
    index: int
    message: ChatCompletionChoiceMessage
    finish_reason: Literal["stop"] = "stop"


class ChatCompletionUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionResponse(BaseModel):
    id: str
    object: Literal["chat.completion"] = "chat.completion"
    created: int
    model: str
    choices: List[ChatCompletionChoice]
    usage: Optional[ChatCompletionUsage] = None


# --- Anthropic-style Messages API schemas (minimal subset) ---


class AnthropicTextBlock(BaseModel):
    type: Literal["text"] = "text"
    text: str


class AnthropicToolUseBlock(BaseModel):
    type: Literal["tool_use"] = "tool_use"
    id: str
    name: str
    input: Dict[str, Any] = Field(default_factory=dict)


AnthropicAssistantContentBlock = Union[AnthropicTextBlock, AnthropicToolUseBlock]


class AnthropicMessage(BaseModel):
    role: Literal["user", "assistant", "system"] = Field(...)
    # Anthropic supports rich content; we accept either:
    # - a simple string, or
    # - a list of text blocks. Both are tolerated via Any and normalized in the route.
    content: Any


class AnthropicMessagesRequest(BaseModel):
    model: str
    messages: List[AnthropicMessage]
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    stream: bool = False
    system: Optional[Any] = None
    tools: Optional[List[Any]] = None

    class Config:
        extra = "allow"


class AnthropicUsage(BaseModel):
    input_tokens: int
    output_tokens: int


class AnthropicMessageResponse(BaseModel):
    id: str
    type: Literal["message"] = "message"
    role: Literal["assistant"] = "assistant"
    model: str
    content: List[AnthropicAssistantContentBlock]
    stop_reason: Optional[str] = None
    stop_sequence: Optional[str] = None
    usage: Optional[AnthropicUsage] = None


# --- Ollama API compatibility (subset): /api/version, /api/tags, /api/generate, /api/chat, /api/show ---


class OllamaGenerateRequest(BaseModel):
    model: str
    prompt: str = ""
    suffix: Optional[str] = None
    system: Optional[str] = None
    template: Optional[str] = None
    stream: Optional[bool] = None
    raw: bool = False
    context: Optional[Any] = None
    options: Optional[Dict[str, Any]] = None

    class Config:
        extra = "allow"


class OllamaChatMessage(BaseModel):
    role: str
    content: Any = ""

    class Config:
        extra = "allow"


class OllamaChatRequest(BaseModel):
    model: str
    messages: List[OllamaChatMessage]
    stream: Optional[bool] = None
    options: Optional[Dict[str, Any]] = None
    tools: Optional[List[Any]] = None

    class Config:
        extra = "allow"


class OllamaShowRequest(BaseModel):
    model: str
    verbose: Optional[bool] = None

    class Config:
        extra = "allow"


