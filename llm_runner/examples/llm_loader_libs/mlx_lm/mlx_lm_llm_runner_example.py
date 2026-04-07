import mlx_lm as mlx


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

prompt = "What is the capital of France?"
# model, tokenizer = mlx.load("Qwen/Qwen2.5-7B-Instruct", quantization="q4_0") # Supports various qtypes
model, tokenizer = mlx.load(model_dir_path) # Supports various qtypes

# response, _ = mlx.generate(
#     model, 
#     tokenizer, 
#     prompt,
#     max_tokens=100,
#     temp=0.7
# )
# print(response)

if tokenizer.chat_template is not None:
    messages = [{"role": "user", "content": prompt}]
    prompt = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True
    )

response = mlx.generate(model, tokenizer, prompt=prompt, verbose=True)
print(response)