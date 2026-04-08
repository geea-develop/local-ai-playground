import os
import json
import subprocess
import sys
import asyncio
from typing import Any, Dict, Optional
from contextlib import asynccontextmanager

from anthropic import Anthropic
from dotenv import load_dotenv

# Import MCP libraries at top level
try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    print("[DEBUG] mcp package successfully imported at module level")
except ImportError as e:
    print(f"[ERROR] Failed to import mcp package: {e}")
    print(f"[ERROR] Please install with: pip install mcp")
    sys.exit(1)

# Load environment variables
load_dotenv()

# Configuration
MAX_TOKENS = 1024

MAX_RESULTS = 1

# Lazy-load the Anthropic client to avoid initialization errors
client = None

def get_client():
    """Lazy-load the Anthropic client."""
    global client
    if client is None:
        client = Anthropic(
            base_url=os.getenv("ANTHROPIC_BASE_URL"),
            api_key=os.getenv("ANTHROPIC_API_KEY"),
        )
    return client


class MCPDuckDuckGoSearchPlugin:
    """Plugin for web search using DuckDuckGo MCP server.
    
    Uses the mcp Python SDK with proper async context management.
    Install with: pip install mcp
    """

    def __init__(self, timeout_seconds: int = 30):
        self.timeout_seconds = timeout_seconds
        self.stdio_context = None
        self.client_obj = None
        self.mcp_server_available = False
        self._mcp_initialized = False
        self._check_docker_availability()

    def _check_docker_availability(self):
        """Check if Docker is running."""
        # Check if Docker is available
        try:
            result = subprocess.run(
                ["docker", "ps"],
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                self.docker_available = True
                print("[DEBUG] Docker is available and running")
            else:
                self.docker_available = False
                print("[DEBUG] Docker is not running")
        except FileNotFoundError:
            self.docker_available = False
            print("[DEBUG] Docker is not installed")

    async def _ensure_connected_async(self):
        """Ensure MCP connection is established and initialized."""
        if self._mcp_initialized and self.client_obj:
            return
        
        try:
            print("[DEBUG] Initializing MCP DuckDuckGo client...")
            
            # Create server parameters for docker-based server
            server_params = StdioServerParameters(
                command="docker",
                args=["run", "-i", "--rm", "mcp/duckduckgo"]
            )
            
            print("[DEBUG] Starting DuckDuckGo MCP server via Docker...")
            # stdio_client is an async context manager that yields (read_stream, write_stream)
            self.stdio_context = stdio_client(server_params)
            read_stream, write_stream = await self.stdio_context.__aenter__()
            
            print("[DEBUG] Creating MCP client session...")
            # Create client session with both read and write streams
            self.client_obj = ClientSession(read_stream, write_stream)
            await self.client_obj.__aenter__()
            
            # CRITICAL: Initialize MCP protocol handshake before using tools
            print("[DEBUG] Performing MCP protocol initialization handshake...")
            await self.client_obj.initialize()
            print("[DEBUG] MCP protocol initialization complete")
            
            self._mcp_initialized = True
            self.mcp_server_available = True
            print("[DEBUG] MCP connection initialized successfully")
            
        except FileNotFoundError:
            raise RuntimeError(
                "Docker is not installed or not in PATH. "
                "Please install Docker to use the DuckDuckGo MCP server."
            )
        except Exception as e:
            print(f"[DEBUG] Error during MCP initialization: {e}")
            import traceback
            traceback.print_exc()
            raise RuntimeError(f"Failed to initialize MCP server: {e}")

    def _run_async(self, coro):
        """Helper to run async code from sync context."""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(coro)

    async def _call_tool_async(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """Call a tool asynchronously via MCP.
        
        Args:
            tool_name: Name of the tool to call
            **kwargs: Tool arguments
        
        Returns:
            Dictionary with 'ok' and 'result' or 'error' keys
        """
        try:
            await self._ensure_connected_async()
            
            print(f"[DEBUG] Calling tool: {tool_name}")
            print(f"[DEBUG] Arguments: {json.dumps(kwargs, indent=2)}")
            
            # Call the tool via MCP client
            result = await self.client_obj.call_tool(tool_name, kwargs)
            
            print(f"[DEBUG] Tool result: {result}")
            
            # Process the result
            if result.isError:
                return {
                    "ok": False,
                    "error": result.content[0].text if result.content else "Tool call failed"
                }
            else:
                # Extract content from result
                content = ""
                if result.content:
                    for block in result.content:
                        if hasattr(block, 'text'):
                            content += block.text
                        elif isinstance(block, dict) and 'text' in block:
                            content += block['text']
                
                # Try to parse as JSON if it's a structured result
                try:
                    parsed = json.loads(content)
                    return {
                        "ok": True,
                        "result": parsed
                    }
                except (json.JSONDecodeError, ValueError):
                    # Return as-is if not JSON
                    return {
                        "ok": True,
                        "result": content
                    }
        except Exception as e:
            print(f"[DEBUG] Tool call error: {e}")
            import traceback
            traceback.print_exc()
            return {
                "ok": False,
                "error": f"Tool call failed: {str(e)}"
            }

    def search(self, query: str, max_results: Optional[int] = None) -> Dict[str, Any]:
        """Search the web using DuckDuckGo.
        
        Args:
            query: The search query string
            max_results: Maximum number of results (1-20, default 10)
        
        Returns:
            Dictionary with 'ok' and 'result' or 'error' keys
        """
        # Ensure max_results is within valid range
        if max_results is None:
            max_results = 10
        elif max_results < 1:
            max_results = 1
        elif max_results > 20:
            max_results = 20
        
        print(f"[DEBUG] Executing search: query='{query}', max_results={max_results}")
        
        # Call async function from sync context
        result = self._run_async(self._call_tool_async("search", query=query, max_results=max_results))
        return result

    def fetch_content(self, url: str, max_length: Optional[int] = None, start_index: Optional[int] = None) -> Dict[str, Any]:
        """Fetch and extract the main text content from a webpage.
        
        Args:
            url: The full URL of the webpage (must start with http:// or https://)
            max_length: Maximum number of characters to return (default: 8000)
            start_index: Character offset to start reading from (default: 0)
        
        Returns:
            Dictionary with 'ok' and 'result' or 'error' keys
        """
        kwargs = {"url": url}
        if max_length is not None:
            kwargs["max_length"] = max_length
        if start_index is not None:
            kwargs["start_index"] = start_index
        
        print(f"[DEBUG] Fetching content from: {url}")
        
        # Call async function from sync context
        result = self._run_async(self._call_tool_async("fetch_content", **kwargs))
        return result

    def shutdown(self):
        """Shutdown the MCP server."""
        if self._mcp_initialized:
            try:
                print("[DEBUG] Shutting down MCP client...")
                # Close the client session and stdio context in reverse order
                if self.client_obj:
                    self._run_async(self.client_obj.__aexit__(None, None, None))
                if self.stdio_context:
                    self._run_async(self.stdio_context.__aexit__(None, None, None))
                print("[DEBUG] MCP shutdown complete")
            except Exception as e:
                print(f"[DEBUG] Error during MCP shutdown: {e}")
        
        self._mcp_initialized = False
        self.mcp_server_available = False


# Initialize search plugin (lazy-load to avoid startup errors)
search_plugin = None

# Define tools
tools = [
    {
        "name": "web_search",
        "description": "Search the web using DuckDuckGo. Returns results with titles, URLs, and snippets. Use specific search queries for best results.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query string. Be specific for better results (e.g., 'Python asyncio tutorial' rather than 'Python')"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results to return, between 1 and 20 (default: 10)",
                    "default": 1,
                    "minimum": 1,
                    "maximum": MAX_RESULTS
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "fetch_content",
        "description": "Fetch and extract the main text content from a webpage. Strips out navigation, headers, footers, scripts, and styles. Use this after searching to read full content of a specific result.",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The full URL of the webpage to fetch (must start with http:// or https://)"
                },
                "max_length": {
                    "type": "integer",
                    "description": "Maximum number of characters to return (default: 8000), increase for more content",
                    "default": 8000
                },
                "start_index": {
                    "type": "integer",
                    "description": "Character offset to start reading from (default: 0). Use this to paginate through long content",
                    "default": 0
                }
            },
            "required": ["url"]
        }
    }
]


def get_search_plugin():
    """Lazy initialize the search plugin on first use."""
    global search_plugin
    if search_plugin is None:
        search_plugin = MCPDuckDuckGoSearchPlugin()
    return search_plugin


def execute_web_search(query: str, max_results: Optional[int] = None) -> str:
    """Execute a web search using the MCP plugin"""
    try:
        plugin = get_search_plugin()
        result = plugin.search(query, max_results)
        
        if result["ok"]:
            results = result.get("result", "")
            if not results:
                return "No search results found."
            
            # DuckDuckGo MCP server returns already-formatted text results
            if isinstance(results, str):
                # Results are already formatted, return as-is
                return results
            
            # If results are a list of dictionaries (unexpected but handle it)
            if isinstance(results, list):
                formatted_results = []
                for i, item in enumerate(results, 1):
                    if isinstance(item, dict):
                        item_text = f"{i}. **{item.get('title', 'No title')}**"
                        if item.get('body'):
                            item_text += f"\n   {item['body']}"
                        if item.get('href'):
                            item_text += f"\n   Source: {item['href']}"
                    else:
                        item_text = f"{i}. {str(item)}"
                    formatted_results.append(item_text)
                
                return "\n\n".join(formatted_results)
            
            # Fallback for other types
            return str(results)
        else:
            return f"Search error: {result['error']}"
    except Exception as e:
        return f"Search failed: {str(e)}"


def execute_fetch_content(url: str, max_length: Optional[int] = None, start_index: Optional[int] = None) -> str:
    """Execute content fetching from a URL"""
    try:
        plugin = get_search_plugin()
        result = plugin.fetch_content(url, max_length, start_index)
        
        if result["ok"]:
            content = result.get("result", "")
            # DuckDuckGo MCP server returns text content directly
            return content if content else "No content found on the page."
        else:
            return f"Fetch error: {result['error']}"
    except Exception as e:
        return f"Content fetch failed: {str(e)}"


def process_tool_call(tool_name: str, tool_input: Dict[str, Any]) -> str:
    """Process tool calls and return results"""
    print(f"[DEBUG] Executing tool: {tool_name}")
    print(f"[DEBUG] Tool input: {tool_input}")

    if tool_name == "web_search":
        result = execute_web_search(
            tool_input["query"],
            tool_input.get("max_results")
        )
        print(f"[DEBUG] Tool result length: {len(result)} chars")
        return result
    elif tool_name == "fetch_content":
        result = execute_fetch_content(
            tool_input["url"],
            tool_input.get("max_length"),
            tool_input.get("start_index")
        )
        print(f"[DEBUG] Tool result length: {len(result)} chars")
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


def call_lm_studio_with_web_search_tools(user_prompt):
    """Call LM Studio with web search tools via MCP and handle tool use"""
    print(f"\n{'='*60}")
    print(f"User Prompt: {user_prompt}")
    print(f"{'='*60}\n")

    # Debug: Print tool configuration
    print(f"[DEBUG] Available tools: {len(tools)}")
    for i, tool in enumerate(tools):
        print(f"  {i+1}. {tool['name']}: {tool['description']}")
    print()

    # System prompt that encourages tool use
    system_prompt = """You are a helpful assistant with access to web search tools powered by DuckDuckGo MCP server.

You have access to two tools:
1. web_search - Search the web for information
2. fetch_content - Get the full text content from a specific webpage

For any question that requires current information, recent events, or detailed content from websites, use these tools.
Always search for accurate, up-to-date information rather than relying on your training data.

When searching:
- Use specific, descriptive queries for best results
- Start with web_search to find relevant pages
- Use fetch_content to read full details from important pages

IMPORTANT: To call a tool, you MUST respond with ONLY a JSON code block in this format:
```json
{"name": "tool_name", "arguments": {"param1": "value1", "param2": "value2"}}
```

Examples:
- For a general search:
```json
{"name": "web_search", "arguments": {"query": "latest news about AI", "max_results": 1}}
```

- To fetch full content from a URL found in search results:
```json
{"name": "fetch_content", "arguments": {"url": "https://example.com/article"}}
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
    print("[DEBUG] Sending request to model with web search tools...")
    response = get_client().messages.create(
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
        response = get_client().messages.create(
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
    try:
        # Example 1: Simple web search
        try:
            result = call_lm_studio_with_web_search_tools("What is the latest news about artificial intelligence?")
            print(f"Result: {result}\n")
        except Exception as e:
            print(f"\nError in Example 1: {e}\n")
            import traceback
            traceback.print_exc()

        # Example 2: Technical information search
        # try:
        #     result = call_lm_studio_with_web_search_tools("Tell me about recent developments in Python programming")
        #     print(f"Result: {result}\n")
        # except Exception as e:
        #     print(f"\nError in Example 2: {e}\n")
        #     import traceback
        #     traceback.print_exc()

        # Example 3: News search
        # try:
        #     result = call_lm_studio_with_web_search_tools("What are the top tech news stories this week?")
        #     print(f"Result: {result}\n")
        # except Exception as e:
        #     print(f"\nError in Example 3: {e}\n")
        #     import traceback
        #     traceback.print_exc()

    finally:
        # Cleanup: Shutdown the MCP server
        print("\n[DEBUG] Cleaning up...")
        if search_plugin is not None:
            search_plugin.shutdown()
        print("[DEBUG] Cleanup complete")
