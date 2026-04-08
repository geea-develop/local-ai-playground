import os
from smolagents import CodeAgent, Model
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LlamaCppModel(Model):
    def __init__(self):
        super().__init__()
        try:
            from llama_cpp import Llama
            self.Llama = Llama
        except ImportError:
            raise ImportError("Please install llama-cpp-python: pip install llama-cpp-python")
        
        # Load model path from .env
        models_dir = os.getenv("MODELS_DIR_PATH")
        model_dir = os.getenv("MODEL_DIR_PATH")
        model_file_path = os.getenv("MODEL_FILE_PATH")
        
        if not all([models_dir, model_dir, model_file_path]):
             raise ValueError("Missing MODELS_DIR_PATH, MODEL_DIR_PATH, or MODEL_FILE_PATH in .env")
             
        self.model_path = os.path.join(models_dir, model_dir, model_file_path)
        print(f"Loading llama.cpp model from: {self.model_path}")
        
        self.llm = self.Llama(
            model_path=self.model_path,
            n_gpu_layers=-1, # Use all GPU layers on Mac
            n_ctx=2048,
            verbose=False
        )

    def __call__(self, messages, stop_sequences=None, grammar=None):
        # Format messages for llama_cpp (OpenAI-like format)
        response = self.llm.create_chat_completion(
            messages=messages,
            stop=stop_sequences,
            max_tokens=500
        )
        return response['choices'][0]['message']['content']

# Initialize and run
try:
    model = LlamaCppModel()
    agent = CodeAgent(tools=[], model=model)
    agent.run("What is 15 + 27?")
except Exception as e:
    print(f"Error: {e}")
