"""
Minimal MLX tool-calling prompt example.

This example does NOT execute tools; it only prompts the model to emit a
`<tool_call>...</tool_call>` block.

See `mlx_lm_langchain_tool_call_example.py` for the full local tool execution loop.
"""

import mlx_lm as mlx

import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

import logging

logger = logging.getLogger(__name__)


def configure_logging() -> None:
    level_name = os.getenv("LOG_LEVEL", "INFO").upper().strip()
    level = getattr(logging, level_name, logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


configure_logging()

# Load model path from .env
models_dir = os.getenv("MODELS_DIR_PATH")
model_dir = os.getenv("MODEL_DIR_PATH")

if not models_dir or not model_dir:
    raise ValueError("Missing MODELS_DIR_PATH or MODEL_DIR_PATH in .env")

model_dir_path = os.path.join(models_dir, model_dir)
logger.info("Targeting model from .env: %s", model_dir_path)

model, tokenizer = mlx.load(model_dir_path)  # Supports various qtypes

prompt="""<bos><start_of_turn>human
You are a function calling AI model. You are provided with function signatures within <tools></tools> XML tags.You may call one or more functions to assist with the user query. Don't make assumptions about what values to plug into functions.Here are the available tools:<tools> [{'type': 'function', 'function': {'name': 'convert_currency', 'description': 'Convert from one currency to another', 'parameters': {'type': 'object', 'properties': {'amount': {'type': 'number', 'description': 'The amount to convert'}, 'from_currency': {'type': 'string', 'description': 'The currency to convert from'}, 'to_currency': {'type': 'string', 'description': 'The currency to convert to'}}, 'required': ['amount', 'from_currency', 'to_currency']}}}, {'type': 'function', 'function': {'name': 'calculate_distance', 'description': 'Calculate the distance between two locations', 'parameters': {'type': 'object', 'properties': {'start_location': {'type': 'string', 'description': 'The starting location'}, 'end_location': {'type': 'string', 'description': 'The ending location'}}, 'required': ['start_location', 'end_location']}}}] </tools>Use the following pydantic model json schema for each tool call you will make: {'title': 'FunctionCall', 'type': 'object', 'properties': {'arguments': {'title': 'Arguments', 'type': 'object'}, 'name': {'title': 'Name', 'type': 'string'}}, 'required': ['arguments', 'name']}For each function call return a json object with function name and arguments within <tool_call></tool_call> XML tags as follows:
<tool_call>
{tool_call}
</tool_call>Also, before making a call to a function take the time to plan the function to take. Make that thinking process between <think>{your thoughts}</think>

Hi, I need to convert 500 USD to Euros. Can you help me with that?<end_of_turn><eos>
<start_of_turn>model
<think>"""

tokenizer.chat_template = (
    "{{ bos_token }}"
    "{% if messages[0]['role'] == 'system' %}{{ raise_exception('System role not supported') }}{% endif %}"
    "{% for message in messages %}"
    "{{ '<start_of_turn>' + message['role'] + '\n' + message['content'] | trim + '<end_of_turn><eos>\n' }}"
    "{% endfor %}"
    "{% if add_generation_prompt %}{{'<start_of_turn>model\n'}}{% endif %}"
)

response = mlx.generate(model, tokenizer, prompt=prompt, verbose=True, max_tokens=1000)
print(response)
