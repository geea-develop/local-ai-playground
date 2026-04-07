#!/usr/bin/env python
"""Direct test of MCP plugin initialization"""
import sys
import asyncio

sys.path.insert(0, 'tests')

from call_with_mcp_search_tools import MCPDuckDuckGoSearchPlugin

async def test_mcp_initialization():
    """Test MCP plugin initialization"""
    print("[TEST] Starting MCP initialization test...")
    
    try:
        # Create plugin
        print("[TEST] Creating MCPDuckDuckGoSearchPlugin...")
        plugin = MCPDuckDuckGoSearchPlugin()
        print("[SUCCESS] Plugin instance created")
        
        # Test the async initialization directly
        print("[TEST] Testing _ensure_connected_async()...")
        await plugin._ensure_connected_async()
        print("[SUCCESS] _ensure_connected_async() completed without errors!")
        
        # Check if MCP is initialized
        if plugin._mcp_initialized:
            print("[SUCCESS] MCP is marked as initialized")
        else:
            print("[ERROR] MCP not marked as initialized")
        
        if plugin.client_obj:
            print("[SUCCESS] MCP client object exists")
        else:
            print("[ERROR] MCP client object is None")
            
        # Try to call a tool
        print("\n[TEST] Attempting to call a tool...")
        print("[TEST] Calling search tool with test query...")
        result = await plugin._call_tool_async("search", query="Python", max_results=2)
        
        if result["ok"]:
            print(f"[SUCCESS] Tool call succeeded!")
            print(f"[RESULT] {result['result']}")
        else:
            print(f"[ERROR] Tool call failed: {result['error']}")
            
        # Shutdown
        print("\n[TEST] Shutting down...")
        plugin.shutdown()
        print("[SUCCESS] Plugin shutdown complete")
        
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_mcp_initialization())
