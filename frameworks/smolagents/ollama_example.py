import os
from smolagents import CodeAgent, OpenAIServerModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- CONFIGURATION ---
OLLAMA_BASE_URL = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")
LLM_MODEL = os.getenv("OLLAMA_LLM_MODEL", "mistral:v0.3")

def main():
    print("\n" + "="*50)
    print("🚀 Running smolagents Local Chat (Ollama)")
    print("="*50 + "\n")

    # 1. Initialize the model pointing to Ollama
    model = OpenAIServerModel(
        model_id=LLM_MODEL,
        api_base=f"{OLLAMA_BASE_URL}/v1",
        api_key="ollama"
    )

    # 2. Setup Agent
    agent = CodeAgent(tools=[], model=model)

    # 3. Run Task
    task = "What is the capital of France?"
    print(f"👤 Question: {task}")
    print("-" * 30)

    try:
        result = agent.run(task)
        print("\n✅ Response:")
        print(result)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Tip: Ensure Ollama is running and the model is available.")

if __name__ == "__main__":
    main()

