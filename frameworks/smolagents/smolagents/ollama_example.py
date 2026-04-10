import os
from smolagents import CodeAgent, OpenAIServerModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the model pointing to Ollama
model_id = os.getenv("MODEL_DIR_PATH", "llama3")
api_base = os.getenv("OLLAMA_API_BASE", "http://localhost:11434/v1")

model = OpenAIServerModel(
    model_id=model_id,
    api_base=api_base,
    api_key="ollama"
)

agent = CodeAgent(tools=[], model=model)

# Run an example
# Ensure Ollama is running before executing this script
try:
    agent.run("What is the capital of France?")
except Exception as e:
    print(f"Error: {e}")
    print("Make sure Ollama is running and the model is available.")
