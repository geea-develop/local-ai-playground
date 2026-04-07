from anthropic import Anthropic
import json

# Configuration
MAX_TOKENS = 1024

client = Anthropic(
    base_url="http://localhost:1234",
    # base_url="http://localhost:8000",
    api_key="lmstudio",
)

# Define tools
tools = [
    {
        "name": "calculator",
        "description": "A simple calculator that can perform arithmetic operations",
        "input_schema": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["add", "subtract", "multiply", "divide"],
                    "description": "The arithmetic operation to perform"
                },
                "a": {
                    "type": "number",
                    "description": "First number"
                },
                "b": {
                    "type": "number",
                    "description": "Second number"
                }
            },
            "required": ["operation", "a", "b"]
        }
    },
    {
        "name": "get_weather",
        "description": "Get the current weather for a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city name or location"
                }
            },
            "required": ["location"]
        }
    }
]


def execute_calculator(operation, a, b):
    """Execute calculator operations"""
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        if b == 0:
            return "Error: Division by zero"
        return a / b
    return "Unknown operation"


def execute_get_weather(location):
    """Simulate getting weather data"""
    weather_data = {
        "San Francisco": "72°F, Cloudy",
        "New York": "65°F, Rainy",
        "Los Angeles": "78°F, Sunny",
        "Seattle": "62°F, Rainy"
    }
    return weather_data.get(location, f"Weather data not available for {location}")


def process_tool_call(tool_name, tool_input):
    """Process tool calls and return results"""
    if tool_name == "calculator":
        result = execute_calculator(
            tool_input["operation"],
            tool_input["a"],
            tool_input["b"]
        )
        return f"Result: {result}"
    elif tool_name == "get_weather":
        result = execute_get_weather(tool_input["location"])
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

def call_lm_studio_with_tools(user_prompt):
    """Call LM Studio with tools and handle tool use"""
    print(f"\n{'='*60}")
    print(f"User Prompt: {user_prompt}")
    print(f"{'='*60}\n")
    
    # Start with user message
    messages = [
        {
            "role": "user",
            "content": user_prompt
        }
    ]
    
    # First call to the model with tools
    response = client.messages.create(
        model="qwen/qwen3.5-9b",
        max_tokens=MAX_TOKENS,
        tools=tools,
        messages=messages
    )
    
    print(f"Initial Response Stop Reason: {response.stop_reason}")
    
    # Process the response
    while response.stop_reason == "tool_use":
        print(f"\n{'-'*60}")
        print("--- Processing Tool Use ---")
        print(f"{'-'*60}\n")
        
        # Step 1: Extract all tool_use blocks from current response
        tool_uses = parse_tool_use_blocks(response.content)
        
        if not tool_uses:
            print("No tool uses found in response")
            break
        
        print(f"Found {len(tool_uses)} tool(s) to execute")
        
        # Step 2: IMPORTANT - Add the assistant message with tool_use FIRST
        assistant_message = {
            "role": "assistant",
            "content": response.content
        }
        messages.append(assistant_message)
        
        # Step 3: Build and add user message with tool_result blocks SECOND
        tool_result_message = build_tool_result_message(tool_uses)
        messages.append(tool_result_message)
        
        print(f"\nTool Result Message sent to model:")
        print(json.dumps(messages[-1], indent=2))
        
        # Step 4: Call the model again with tool results
        response = client.messages.create(
            model="qwen/qwen3.5-9b",
            max_tokens=MAX_TOKENS,
            tools=tools,
            messages=messages
        )
        
        print(f"\nResponse Stop Reason: {response.stop_reason}")
    
    # Extract final text response
    final_response = ""
    for block in response.content:
        if isinstance(block, dict) and block.get("type") == "text":
            final_response += block.get("text", "")
        elif hasattr(block, 'text'):
            final_response += block.text
    
    print(f"\n{'='*60}")
    print(f"Final Response:\n{final_response}")
    print(f"{'='*60}\n")
    
    return final_response


# Test the function
if __name__ == "__main__":
    # Example 1: Calculator
    try:
        result = call_lm_studio_with_tools("What is 25 multiplied by 4?")
        print(f"Result: {result}")
    except Exception as e:
        print(f"\nError occurred: {e}\n")
    
    # Example 2: Weather
    try:
        result = call_lm_studio_with_tools("What's the weather like in San Francisco and New York?")
        print(f"Result: {result}")
    except Exception as e:
        print(f"\nError occurred: {e}\n")
    
    # Example 3: Multiple operations
    try:
        result = call_lm_studio_with_tools("Calculate 100 divided by 5, then add 10 to the result")
        print(f"Result: {result}")
    except Exception as e:
        print(f"\nError occurred: {e}\n")
