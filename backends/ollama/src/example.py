from .ollama_client import OllamaClient

MODEL="qwen3-coder" # 'llama3'


# Usage
client = OllamaClient(MODEL)

# Regular chat
result = client.chat("Explain quantum computing in simple terms")
print(result)

# Streaming chat
print("Streaming response:")
client.stream_chat("Write a 50-word explanation of machine learning")