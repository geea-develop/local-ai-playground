import os
from smolagents import CodeAgent, OpenAIServerModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the model pointing to LM Studio
model_id = os.getenv("MODEL_DIR_PATH", "local-model")
api_base = os.getenv("LM_STUDIO_API_BASE", "http://localhost:1234/v1")

model = OpenAIServerModel(
    model_id=model_id,
    api_base=api_base,
    api_key="not-needed"
)

agent = CodeAgent(tools=[], model=model)

# Run an example
# Ensure LM Studio server is running before executing this script
try:
    agent.run("Tell me a short joke about robots.")
except Exception as e:
    print(f"Error: {e}")
    print("Make sure LM Studio is running and its local server is started at http://localhost:1234")
