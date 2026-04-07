import mlx_lm as mlx
from langchain_community.chat_models.mlx import ChatMLX
from langchain.messages import HumanMessage
from langchain_community.llms.mlx_pipeline import MLXPipeline
from langchain_core.prompts import PromptTemplate

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

model, tokenizer = mlx.load(model_dir_path)

pipe = MLXPipeline(model=model, tokenizer=tokenizer)

template = """Question: {question}

Answer: Let's think step by step."""
prompt = PromptTemplate.from_template(template)

chain = prompt | pipe

question = "What is electroencephalography?"

print(chain.invoke({"question": question}))