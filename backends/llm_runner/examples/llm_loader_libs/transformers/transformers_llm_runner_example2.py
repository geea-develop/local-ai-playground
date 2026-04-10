from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load model path from .env
models_dir = os.getenv("MODELS_DIR_PATH")
model_dir = os.getenv("MODEL_DIR_PATH")
repo_name = os.getenv("REPO_NAME")

if not models_dir or not model_dir:
    raise ValueError("Missing MODELS_DIR_PATH or MODEL_DIR_PATH in .env")


model_dir_path = os.path.join(models_dir, model_dir)
print(f"Targeting model from .env: {model_dir_path}\n")

local_path = model_dir_path # The directory containing the model files (e.g., config.json, pytorch_model.bin, tokenizer files)

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained(local_path)

# Load the model
model = AutoModelForCausalLM.from_pretrained(
    local_path,
    local_files_only=True,   # Forces the library to only look at local files
    # device_map="auto",       # Automatically handles GPU/CPU placement
    device_map={"": "mps"}, # Map directly to Apple Silicon GPU
    # torch_dtype=torch.float16, # Recommended to save RAM/VRAM
    dtype=torch.float16, # Recommended to save RAM/VRAM
    low_cpu_mem_usage=True,  # Reduces CPU memory usage during loading
)

# Test the model
prompt = "Explain quantum physics in one sentence."
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=50)

print(tokenizer.decode(outputs[0], skip_special_tokens=True))