import os

from dotenv import load_dotenv

from llama_cpp import Llama


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

# Load model from GGUF file (works with any quantization)
# llm = Llama.from_pretrained(
#     repo_id="Qwen/Qwen2.5-7B-Instruct-GGUF", # Example model
#     filename="qwen2.5-7b-instruct-q4_0.gguf",
#     n_ctx=2048,           # Context window size
#     n_threads=8,          # CPU threads (use all cores)
#     n_gpu_layers=-1,      # Load ALL layers to GPU (set to 0 for CPU only)
#     f16_kv=True,          # Use FP16 KV cache for faster inference
#     use_mlock=False,      # Don't lock RAM (save memory)
# )

# # Generate text
# response = llm(
#     "What is the capital of France?",
#     max_tokens=50,
#     temperature=0.7
# )


llm = Llama(model_path=model_path, ntcx=3000)
output = llm("Q: Name the planets in the solar system? A: ", max_tokens=32, temperature=0.1)
print(output)

# print(response["choices"][0]["text"])
