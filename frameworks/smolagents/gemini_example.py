import os
from smolagents import ToolCallingAgent, LiteLLMModel, Tool
from dotenv import load_dotenv
from tavily import TavilyClient

# Load environment variables
load_dotenv()

class WebSearchTool(Tool):
    name = "web_search"
    description = "A high-quality web search engine. Use this for all your search needs. Returns a list of relevant snippets."
    inputs = {
        "query": {
            "type": "string",
            "description": "The search query to look up",
        }
    }
    output_type = "string"

    def forward(self, query: str) -> str:
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key or "your_tavily" in api_key:
             return "Error: TAVILY_API_KEY is missing or invalid. Please provide a valid key in .env."
             
        client = TavilyClient(api_key=api_key)
        # depth="basic" is faster and usually enough for simple facts
        response = client.search(query, search_depth="basic", max_results=5)
        
        results = []
        for r in response.get("results", []):
            # Truncate content to keep context window clean
            content = r.get('content', '')
            if len(content) > 500:
                content = content[:500] + "..."
            results.append(f"Source: {r.get('url')}\nContent: {content}")
        
        return "\n---\n".join(results) if results else "No results found."

def main():
    print("\n" + "="*50)
    print("🚀 Running smolagents with Google Gemini & Tavily")
    print("="*50 + "\n")

    # 1. Initialize the model using LiteLLM
    model_id = os.getenv("GEMINI_MODEL", "gemini/gemini-3-flash-preview")
    
    print(f"🤖 Using model: {model_id}")
    
    model = LiteLLMModel(
        model_id=model_id,
        api_key=os.getenv("GOOGLE_API_KEY")
    )

    # 2. Setup Agent with our WebSearchTool
    # ToolCallingAgent is often more reliable with Gemini as it uses native function calling (JSON)
    # instead of trying to parse python code blocks with regex.
    agent = ToolCallingAgent(
        tools=[WebSearchTool()], 
        model=model,
        max_steps=10
    )

    # 3. Run Task
    task = "Who won the latest Formula 1 race (April 2026) and what was the gap to the second place?"
    print(f"👤 Question: {task}")
    print("-" * 30)

    try:
        result = agent.run(task)
        print("\n✅ Final Result:")
        print(result)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if "TAVILY_API_KEY" in str(e):
            print("\nTip: Please set your TAVILY_API_KEY in the .env file.")

if __name__ == "__main__":
    main()
