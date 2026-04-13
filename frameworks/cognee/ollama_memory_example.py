import asyncio
import os
import cognee
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

async def run_memory_example():
    """
    Demonstrates the Cognee memory lifecycle: Add, Cognify, and Search.
    This example is configured to use local Ollama models.
    """
    
    # 1. Add some data to the system
    # In a real app, this could be messages, documents, or raw text.
    print("--- 1. Adding data to Cognee ---")
    data_points = [
        "Steve Jobs founded Apple Inc. in 1976.",
        "Apple Inc. released the Macintosh in 1984.",
        "The headquarters of Apple is located in Cupertino, California.",
        "Tim Cook became the CEO of Apple in 2011."
    ]
    
    for point in data_points:
        print(f"Adding: {point}")
        await cognee.add(point)

    # 2. Build the memory (Cognify)
    # This step extracts entities and relationships to build the Knowledge Graph
    # and generates vector embeddings for semantic search.
    print("\n--- 2. Cognifying (Building Graph and Vector Store) ---")
    print("This may take a moment as the LLM processes the data...")
    try:
        await cognee.cognify()
        print("Cognification successful!")
    except Exception as e:
        print(f"An error occurred during cognification: {e}")
        print("Tip: Ensure your Ollama server is running and the models are pulled.")
        return

    # 3. Perform a Semantic Search
    # Cognee can find information based on the entities and relationships it learned.
    print("\n--- 3. Searching Memory ---")
    query = "Who founded Apple and when?"
    print(f"Query: '{query}'")
    
    search_results = await cognee.search(query)
    
    print("\nResults:")
    if search_results:
        for i, result in enumerate(search_results):
            # The structure of search_results depends on the search type and configuration
            print(f"[{i+1}] {result}")
    else:
        print("No results found in memory.")

    # 4. Another query to show relationship understanding
    print("\n--- 4. Relationship Search ---")
    query = "Where is the company founded by Steve Jobs located?"
    print(f"Query: '{query}'")
    
    search_results = await cognee.search(query)
    
    print("\nResults:")
    if search_results:
        for i, result in enumerate(search_results):
            print(f"[{i+1}] {result}")
    else:
        print("No results found in memory.")

if __name__ == "__main__":
    # Ensure Cognee uses its default local storage for this example
    # Note: Cognee creates .cognee_system and cognee_data directories by default.
    asyncio.run(run_memory_example())
