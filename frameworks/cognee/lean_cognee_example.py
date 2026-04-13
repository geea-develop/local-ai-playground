import asyncio
import os
import cognee
from dotenv import load_dotenv
import httpx

# Load initial environment variables
load_dotenv()

async def check_model_ready(model_name):
    print(f"Checking if model '{model_name}' is available in Ollama...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:11434/api/tags")
            if response.status_code == 200:
                models = [m["name"] for m in response.json().get("models", [])]
                if model_name in models or f"{model_name}:latest" in models:
                    print(f"✅ Model '{model_name}' found.")
                    return True
                else:
                    print(f"❌ Model '{model_name}' NOT found in Ollama.")
                    print(f"Available models: {', '.join(models)}")
                    return False
    except Exception as e:
        print(f"❌ Could not connect to Ollama: {e}")
        return False

async def run_lean_example():
    """
    A minimal Cognee example to verify the framework is working with lower overhead.
    """
    # Override model for this leaner test if needed, or use .env
    # We recommend mistral:v0.3 or llama3:8b for a balance of speed and reliability.
    model = os.getenv("LLM_MODEL", "mistral:v0.3")
    
    if not await check_model_ready(model):
        print("\nStopping: Please pull the required model or update .env")
        return

    print("\n--- Initializing Cognee (Minimal) ---")
    
    # 1. Add just two simple, clear facts
    print("Step 1: Adding minimal data...")
    try:
        await cognee.add("The Eiffel Tower is located in Paris, France.")
        await cognee.add("Paris is the capital of France.")
        print("Done.")
    except Exception as e:
        print(f"Error adding data: {e}")
        return

    # 2. Cognify (The heavy part)
    # This task is what usually gets 'stuck' if the model is too slow.
    print("\nStep 2: Cognifying (Building graph and vectors)...")
    print(f"Using model: {model}")
    print("This involves the LLM extracting entities and relationships.")
    
    try:
        # We wrap this in a timeout if possible, though cognee doesn't expose it easily here.
        # But we'll just wait and see.
        await cognee.cognify()
        print("✅ Cognification successful!")
    except Exception as e:
        print(f"\n❌ Cognification failed: {e}")
        print("Common issues: Model too slow, OOM on your Mac, or connection timeout.")
        return

    # 3. Search
    print("\nStep 3: Searching Memory...")
    queries = [
        "Where is the Eiffel Tower or Paris?",
        "What is the capital of France?"
    ]
    
    for query in queries:
        print(f"\nQuery: '{query}'")
        try:
            results = await cognee.search(query)
            print("Search Results:")
            if results:
                for i, result in enumerate(results):
                    # Clean up the output if it's a dict or object
                    print(f"[{i+1}] {result}")
            else:
                print("No results found in memory.")
        except Exception as e:
            print(f"Error during search for '{query}': {e}")

if __name__ == "__main__":
    asyncio.run(run_lean_example())
