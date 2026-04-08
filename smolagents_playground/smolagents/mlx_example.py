import os
from smolagents import CodeAgent, Model
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MLXModel(Model):
    def __init__(self, model_id=None):
        super().__init__()
        
        # Load model ID or path from environment variables
        models_dir = os.getenv("MODELS_DIR_PATH")
        env_model_id = os.getenv("MODEL_DIR_PATH")
        
        if not model_id:
            if models_dir and env_model_id:
                local_path = os.path.join(models_dir, env_model_id)
                if os.path.isdir(local_path):
                    model_id = local_path
                    print(f"Loading MLX model from local path: {model_id}")
                else:
                    model_id = env_model_id
                    print(f"Loading MLX model from ID: {model_id}")
            else:
                model_id = env_model_id or "mlx-community/Llama-3.2-3B-Instruct-4bit"
                print(f"Loading MLX model: {model_id}")

        try:
            from mlx_lm import load, generate
            self.load = load
            self.generate = generate
            self.model, self.tokenizer = self.load(model_id)
        except ImportError:
            raise ImportError("Please install mlx-lm: pip install mlx-lm")

    def __call__(self, messages, stop_sequences=None, grammar=None):
        # Convert messages to prompt
        prompt = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        
        # Generate
        response = self.generate(self.model, self.tokenizer, prompt=prompt, verbose=False, max_tokens=500)
        
        # Clean up response if needed (remove prompt if it's included)
        return response

# Initialize the agent with the MLX model
model = MLXModel()
agent = CodeAgent(tools=[], model=model)

# Run an example
agent.run("What is the square root of 256 multiplied by 2?")
