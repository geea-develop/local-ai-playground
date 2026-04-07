import os

from anthropic import Anthropic
import json

from dotenv import load_dotenv
from urllib import error, parse, request
from typing import Any, Dict, Optional

# Load environment variables
load_dotenv()

# Configuration
MAX_TOKENS = 1024

client = Anthropic(
    base_url=os.getenv("ANTHROPIC_BASE_URL"),
    api_key=os.getenv("ANTHROPIC_API_KEY"),
)


class CurrencyConversionPlugin:
    """Plugin for converting currency amounts using a remote API."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout_seconds: int = 8,
    ):
        self.base_url = (
            base_url
            or os.getenv("CURRENCY_API_BASE_URL")
            or "https://api.exchangerate.host"
        )
        self.api_key = api_key or os.getenv("CURRENCY_API_KEY")
        self.timeout_seconds = timeout_seconds

    def convert(
        self,
        amount: float,
        from_currency: str,
        to_currency: str,
    ) -> Dict[str, Any]:
        """Convert amount from one ISO currency to another."""
        query_params = {
            "from": from_currency.upper(),
            "to": to_currency.upper(),
            "amount": amount,
        }
        if self.api_key:
            query_params["access_key"] = self.api_key

        query = parse.urlencode(query_params)
        url = f"{self.base_url.rstrip('/')}/convert?{query}"
        req = request.Request(
            url=url,
            headers={"Accept": "application/json"},
            method="GET",
        )
        try:
            with request.urlopen(req, timeout=self.timeout_seconds) as response:
                payload = response.read().decode("utf-8")
                data = json.loads(payload) if payload else {}
                print(f"[DEBUG] API Response for {from_currency}->{to_currency}: {json.dumps(data)}")
                result = data.get("result")
                rate = data.get("info", {}).get("rate")
                print(f"[DEBUG] Extracted - result={result}, rate={rate}")
                return {
                    "ok": True,
                    "amount": amount,
                    "from": from_currency.upper(),
                    "to": to_currency.upper(),
                    "rate": rate,
                    "result": result,
                    "raw": data,
                }
        except error.HTTPError as exc:
            return {
                "ok": False,
                "error": f"Currency API returned HTTP {exc.code}.",
            }
        except error.URLError as exc:
            return {
                "ok": False,
                "error": f"Currency API is unreachable: {exc.reason}",
            }
        except json.JSONDecodeError:
            return {
                "ok": False,
                "error": "Currency API returned invalid JSON.",
            }

    def execute(
        self,
        amount: float,
        from_currency: str,
        to_currency: str,
    ) -> Dict[str, Any]:
        """Common plugin entrypoint."""
        return self.convert(amount, from_currency, to_currency)


# Initialize currency plugin
currency_plugin = CurrencyConversionPlugin()

# Define tools
tools = [
    {
        "name": "convert_currency",
        "description": "Convert an amount from one currency to another using real-time exchange rates",
        "input_schema": {
            "type": "object",
            "properties": {
                "amount": {
                    "type": "number",
                    "description": "The amount to convert"
                },
                "from_currency": {
                    "type": "string",
                    "description": "The source currency code (e.g., USD, EUR, GBP, JPY)"
                },
                "to_currency": {
                    "type": "string",
                    "description": "The target currency code (e.g., USD, EUR, GBP, JPY)"
                }
            },
            "required": ["amount", "from_currency", "to_currency"]
        }
    },
    {
        "name": "get_exchange_rate",
        "description": "Get the current exchange rate between two currencies",
        "input_schema": {
            "type": "object",
            "properties": {
                "from_currency": {
                    "type": "string",
                    "description": "The source currency code (e.g., USD, EUR, GBP, JPY)"
                },
                "to_currency": {
                    "type": "string",
                    "description": "The target currency code (e.g., USD, EUR, GBP, JPY)"
                }
            },
            "required": ["from_currency", "to_currency"]
        }
    }
]


def execute_convert_currency(amount, from_currency, to_currency):
    """Execute currency conversion using the plugin"""
    result = currency_plugin.convert(amount, from_currency, to_currency)
    if result["ok"]:
        if result['result'] is None or result['rate'] is None:
            return f"Error: API returned incomplete data (result={result['result']}, rate={result['rate']}). Raw response: {result['raw']}"
        return f"{result['amount']} {result['from']} = {result['result']:.2f} {result['to']} (Rate: {result['rate']:.4f})"
    else:
        return f"Error: {result['error']}"


def execute_get_exchange_rate(from_currency, to_currency):
    """Get the exchange rate between two currencies"""
    result = currency_plugin.convert(1, from_currency, to_currency)
    if result["ok"]:
        if result['result'] is None:
            return f"Error: API returned incomplete data (result={result['result']}). Raw response: {result['raw']}"
        return f"1 {result['from']} = {result['result']:.4f} {result['to']}"
    else:
        return f"Error: {result['error']}"


def process_tool_call(tool_name, tool_input):
    """Process tool calls and return results"""
    print(f"[DEBUG] Executing tool: {tool_name}")
    print(f"[DEBUG] Tool input: {tool_input}")
    
    if tool_name == "convert_currency":
        result = execute_convert_currency(
            tool_input["amount"],
            tool_input["from_currency"],
            tool_input["to_currency"]
        )
        print(f"[DEBUG] Tool result: {result}")
        return result
    elif tool_name == "get_exchange_rate":
        result = execute_get_exchange_rate(
            tool_input["from_currency"],
            tool_input["to_currency"]
        )
        print(f"[DEBUG] Tool result: {result}")
        return result
    else:
        return f"Unknown tool: {tool_name}"


def parse_tool_use_blocks(response_content):
    """Extract all tool_use blocks from response content"""
    tool_uses = []
    for block in response_content:
        if isinstance(block, dict) and block.get("type") == "tool_use":
            tool_uses.append(block)
        elif hasattr(block, 'type') and block.type == "tool_use":
            tool_uses.append(dict(block))
    return tool_uses


def build_tool_result_message(tool_use_blocks):
    """Build a user message with tool_result blocks for all tool uses"""
    results = []
    for tool_use_block in tool_use_blocks:
        tool_name = tool_use_block["name"]
        tool_input = tool_use_block["input"]
        
        # Execute the tool
        tool_result_text = process_tool_call(tool_name, tool_input)
        
        # Add to results list (tool_results must come first in content array)
        results.append({
            "type": "tool_result",
            "tool_use_id": tool_use_block["id"],
            "content": tool_result_text
        })
    
    return {
        "role": "user",
        "content": results
    }


def call_lm_studio_with_currency_tools(user_prompt):
    """Call LM Studio with currency tools and handle tool use"""
    print(f"\n{'='*60}")
    print(f"User Prompt: {user_prompt}")
    print(f"{'='*60}\n")
    
    # Debug: Print tool configuration
    print(f"[DEBUG] Available tools: {len(tools)}")
    for i, tool in enumerate(tools):
        print(f"  {i+1}. {tool['name']}: {tool['description']}")
    print()
    
    # System prompt that encourages tool use
    system_prompt = """You are a helpful assistant with access to currency conversion tools. 
For ANY currency-related question or conversion request, you MUST use the available tools to get accurate, real-time exchange rates. 
Do not estimate or assume exchange rates - always use the tools provided.
This ensures the most accurate and current information is provided to the user.

IMPORTANT: To call a tool, you MUST respond with ONLY a JSON code block in this format:
```json
{"name": "tool_name", "arguments": {"param1": "value1", "param2": "value2"}}
```

For example, to convert 100 USD to EUR, respond with:
```json
{"name": "convert_currency", "arguments": {"amount": 100, "from_currency": "USD", "to_currency": "EUR"}}
```

Or to get an exchange rate:
```json
{"name": "get_exchange_rate", "arguments": {"from_currency": "USD", "to_currency": "EUR"}}
```

CRITICAL: Always respond with JSON tool calls in a code block. Do NOT provide explanations or prose - only the tool invocation JSON."""
    
    # Start with user message
    messages = [
        {
            "role": "user",
            "content": user_prompt
        }
    ]
    
    # First call to the model with tools
    print("[DEBUG] Sending request to model with tools...")
    response = client.messages.create(
        model=os.getenv("ANTHROPIC_MODEL_NAME"),
        max_tokens=MAX_TOKENS,
        system=system_prompt,
        tools=tools,
        messages=messages
    )
    
    print(f"[DEBUG] Initial Response Stop Reason: {response.stop_reason}")
    print(f"[DEBUG] Response has {len(response.content)} content blocks")
    for i, block in enumerate(response.content):
        block_type = block.get("type") if isinstance(block, dict) else getattr(block, "type", "unknown")
    print()
    
    # Process the response
    while response.stop_reason == "tool_use":
        print(f"\n{'-'*60}")
        print("--- Processing Tool Use ---")
        print(f"{'-'*60}\n")
        
        # Step 1: Extract all tool_use blocks from current response
        tool_uses = parse_tool_use_blocks(response.content)
        
        if not tool_uses:
            print("[DEBUG] No tool uses found in response despite stop_reason=tool_use")
            break
        
        print(f"[DEBUG] Found {len(tool_uses)} tool(s) to execute:")
        for i, tool_use in enumerate(tool_uses):
            print(f"  {i+1}. Tool: {tool_use['name']}")
            print(f"     ID: {tool_use['id']}")
            print(f"     Input: {json.dumps(tool_use['input'], indent=6)}")
        
        # Step 2: IMPORTANT - Add the assistant message with tool_use FIRST
        assistant_message = {
            "role": "assistant",
            "content": response.content
        }
        messages.append(assistant_message)
        
        # Step 3: Build and add user message with tool_result blocks SECOND
        tool_result_message = build_tool_result_message(tool_uses)
        messages.append(tool_result_message)
        
        print(f"\n[DEBUG] Tool Result Message sent to model:")
        print(json.dumps(messages[-1], indent=2))
        
        # Step 4: Call the model again with tool results
        print(f"\n[DEBUG] Sending tool results back to model...")
        response = client.messages.create(
            model=os.getenv("ANTHROPIC_MODEL_NAME"),
            max_tokens=MAX_TOKENS,
            system=system_prompt,
            tools=tools,
            messages=messages
        )
        
        print(f"[DEBUG] Response Stop Reason: {response.stop_reason}")
        print(f"[DEBUG] Response has {len(response.content)} content blocks")
        for i, block in enumerate(response.content):
            block_type = block.get("type") if isinstance(block, dict) else getattr(block, "type", "unknown")
            print(f"  Block {i+1}: type={block_type}")
    
    # Extract final text response
    final_response = ""
    for block in response.content:
        if isinstance(block, dict) and block.get("type") == "text":
            final_response += block.get("text", "")
        elif hasattr(block, 'text'):
            final_response += block.text
    
    print(f"\n[DEBUG] Final response extracted:")
    print(f"[DEBUG] Response length: {len(final_response)} characters")
    print(f"[DEBUG] Stop reason at end: {response.stop_reason}")
    
    print(f"\n{'='*60}")
    print(f"Final Response:\n{final_response}")
    print(f"{'='*60}\n")
    
    return final_response


# Test the function
if __name__ == "__main__":
    # Example 1: Simple currency conversion
    try:
        result = call_lm_studio_with_currency_tools("Convert 100 USD to EUR")
        print(f"Result: {result}\n")
    except Exception as e:
        print(f"\nError occurred: {e}\n")
    
    # Example 2: Multiple conversions
    try:
        result = call_lm_studio_with_currency_tools("What is 500 GBP in JPY and also in USD?")
        print(f"Result: {result}\n")
    except Exception as e:
        print(f"\nError occurred: {e}\n")
    
    # Example 3: Exchange rate inquiry
    try:
        result = call_lm_studio_with_currency_tools("What is the current exchange rate between EUR and INR?")
        print(f"Result: {result}\n")
    except Exception as e:
        print(f"\nError occurred: {e}\n")
