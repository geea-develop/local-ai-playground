import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Point to the LocalAI server
# Default is http://localhost:8080/v1
client = OpenAI(
    base_url=os.getenv("LOCALAI_API_BASE", "http://localhost:8080/v1"),
    api_key="not-needed" # LocalAI doesn't require a key by default
)

def chat_example():
    print("Connecting to LocalAI...")
    try:
        response = client.chat.completions.create(
            model=os.getenv("MODEL_DIR_PATH", "llama-3.2-1b-instruct:q4_k_m"),
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Explain what LocalAI is in one sentence."}
            ]
        )
        print("\nResponse from LocalAI:")
        print(response.choices[0].message.content)
    except Exception as e:
        print(f"\nError: {e}")
        print("Make sure LocalAI is running at http://localhost:8080 and the model is installed.")

if __name__ == "__main__":
    chat_example()
