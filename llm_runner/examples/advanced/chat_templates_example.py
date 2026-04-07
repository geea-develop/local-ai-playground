import os
from pathlib import Path
from dotenv import load_dotenv
from transformers import AutoTokenizer

# Load environment variables
load_dotenv()

# Load model path from .env
models_dir = os.getenv("MODELS_DIR_PATH")
model_file_path = os.getenv("MODEL_FILE_PATH")
repo_name = os.getenv("REPO_NAME")

if not models_dir or not model_file_path:
    raise ValueError("Missing MODELS_DIR_PATH or MODEL_FILE_PATH in .env")

print(f"Targeting model from .env: {model_file_path}\n")

# tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-7B-Instruct")
tokenizer = AutoTokenizer.from_pretrained(
    pretrained_model_name_or_path="".join([models_dir, "/", model_file_path]),
    local_files_only=True
)
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello! How are you?"}
]

# 1. Format the prompt correctly for the model
# Using tokenize=False returns a raw string prompt.
# This fixes the PyTorch ImportError because we skip `return_tensors="pt"` entirely.
text = tokenizer.apply_chat_template(
    messages, 
    tokenize=False, 
    add_generation_prompt=True
)

print("--- Generated Prompt Template ---")
print(text)
print("---------------------------------\n")

# 2. Get response from the model (mocked here since we don't have the actual model loading code)
# In a real implementation, you would load the model and generate a response like this:
# from transformers import AutoModelForCausalLM
# model = AutoModelForCausalLM.from_pretrained(model_file_path, local_files_only=True)
# inputs = tokenizer(text, return_tensors="pt").to(model.device)
# outputs = model.generate(**inputs, max_new_tokens=50, temperature=0.7)
# response = tokenizer.decode(outputs[0], skip_special_tokens=True)
