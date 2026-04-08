import mlx_lm as mlx

import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load model path from .env
models_dir = os.getenv("MODELS_DIR_PATH")
model_dir = os.getenv("MODEL_DIR_PATH")

if not models_dir or not model_dir:
    raise ValueError("Missing MODELS_DIR_PATH or MODEL_DIR_PATH in .env")

model_dir_path = os.path.join(models_dir, model_dir)
print(f"Targeting model from .env: {model_dir_path}\n")

prompt = "Im using the mlx_lm library. Give me a python code example for using chat templates with mlx_lm. I want to see how to apply a chat template to a list of messages and generate a response from the model using the applied template. Show me how to do this in code."
model, tokenizer = mlx.load(model_dir_path)

if tokenizer.chat_template is not None:
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    # Using tokenize=False returns a raw string prompt.
    prompt = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True, tokenize=False, 
    )

print("--- Generated Prompt Template ---")
print(prompt)
print("---------------------------------\n")


response = mlx.generate(model, tokenizer, prompt=prompt, verbose=True)

print("--- Model Response ---")
print(response)
print("----------------------")