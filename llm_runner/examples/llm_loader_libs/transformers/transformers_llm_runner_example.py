from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

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

# model_name = "Qwen/Qwen2.5-7B-Instruct"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForCausalLM.from_pretrained(
#     model_name,
#     device_map="auto",  # Automatically puts on GPU if available
#     torch_dtype=torch.float16, # Or bfloat16 for Ampere/AI GPUs
#     low_cpu_mem_usage=True,
# )

tokenizer = AutoTokenizer.from_pretrained(
    repo_name,
    pretrained_model_name_or_path="".join([models_dir, "/", model_file_path]),
    local_files_only=True
)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    device_map="auto",  # Automatically puts on GPU if available
    torch_dtype=torch.float16, # Or bfloat16 for Ampere/AI GPUs
    low_cpu_mem_usage=True,
)
model.eval()

input_text = "What is the capital of France?"
inputs = tokenizer(input_text, return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=50, temperature=0.7)

print(tokenizer.decode(outputs[0], skip_special_tokens=True))
