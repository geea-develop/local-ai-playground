import os

from dotenv import load_dotenv
from llama_cpp import Llama
from langchain_community.chat_models import ChatLlamaCpp
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import time

# Load environment variables
load_dotenv()

# Load model path from .env
models_dir = os.getenv("MODELS_DIR_PATH")
model_dir = os.getenv("MODEL_DIR_PATH")
model_file_path = os.getenv("MODEL_FILE_PATH")
repo_name = os.getenv("REPO_NAME")

if not models_dir or not model_dir:
    raise ValueError("Missing MODELS_DIR_PATH or MODEL_DIR_PATH in .env")

if not model_file_path:
    raise ValueError("Missing MODEL_FILE_PATH in .env")

model_path = os.path.join(models_dir, model_dir, model_file_path)
print(f"Targeting model from .env: {model_path}\n")


def main():
    # 1. Load the Local Model
    # We use 'gguf' format (e.g., .bin files) which are small and fast on Apple Silicon.
    # You can download a model from HuggingFace.co like Qwen2.5-1.5B-Instruct or Llama-3-8B.
    
    print("🚀 Loading local model...")
    start_time = time.time()
    
    # Parameters optimized for Apple Silicon (llama-metal)
    # llm = Llama.from_pretrained(
    #     # repo_id="Qwen/Qwen2.5-1.5B-Instruct", 
    #     # Alternatively, if you have a local file path:
    #     # model_path="/path/to/your/model.gguf"
    #     model_path=model_path,
    #     n_ctx=4096,          # Context window size
    #     n_threads=min(8, 4), # CPU threads (Metal handles the inference)
    #     n_gpu_layers=-1,     # -1 means let llama-cpp decide optimal split
    #     verbose=False
    # )
    llm = ChatLlamaCpp(
        model_path=model_path)
    
    load_time = time.time() - start_time
    print(f"✅ Model loaded in {load_time:.2f} seconds.\n")

    # 2. Define the Prompt Template
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI assistant running locally on macOS."),
        ("user", "{input}")
    ])

    # 3. Build the LangChain Chain
    def format_docs(docs):
        return "\n\n".join([doc.page_content for doc in docs])
    
    chain = (
        {"input": lambda x: x["input"]}
        | prompt_template
        | llm.invoke  # The LLM callable acts as the language model
        | StrOutputParser()
    )

    # 4. Interact with the Model
    print("--- Starting Conversation ---")
    
    # Test 1: Simple query
    response = chain.invoke({"input": "What is the capital of France?"})
    print(f"\nUser: What is the capital of France?")
    print(f"Assistant: {response}\n")

    # Test 2: Longer context (using a multi-line prompt)
    long_input = """
    I am writing an essay about local AI models on Mac. 
    Explain the benefits of running LLMs locally compared to cloud APIs, 
    focusing on privacy and latency. Keep it under 100 words.
    """
    response = chain.invoke({"input": long_input})
    print(f"User: {long_input[:50]}...") # Truncated for display
    print(f"Assistant: {response}\n")

    print("--- End of Conversation ---")

if __name__ == "__main__":
    main()
