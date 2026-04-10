src/
  __init__.py  [0]
  example.py  [15]
  ollama_client.py  [54]

## Ollama Projects

This project demonstrates how to use the Ollama Python client to interact with local LLMs.

### Installation

First, install the Ollama Python client:

```bash
pip install ollama
```

### Basic Usage

#### 1. Simple Chat Completion

```python
import ollama

# Basic chat
response = ollama.chat(
    model='llama3',
    messages=[
        {'role': 'user', 'content': 'Hello!'},
    ]
)

print(response['message']['content'])
```

#### 2. Streaming Responses

```python
import ollama

# Stream responses
response = ollama.chat(
    model='llama3',
    messages=[
        {'role': 'user', 'content': 'Write a short poem about Python programming'},
    ],
    stream=True
)

for chunk in response:
    print(chunk['message']['content'], end='', flush=True)
```

#### 3. With Context and History

```python
import ollama

# Chat with conversation history
messages = [
    {'role': 'user', 'content': 'What is Python?'},
    {'role': 'assistant', 'content': 'Python is a high-level programming language...'},
    {'role': 'user', 'content': 'What are its main features?'}
]

response = ollama.chat(
    model='llama3',
    messages=messages
)

print(response['message']['content'])
```

#### 4. Using Different Models

```python
import ollama

# Different models
models = ['llama3', 'mistral', 'phi3', 'gemma']

for model in models:
    try:
        response = ollama.chat(
            model=model,
            messages=[{'role': 'user', 'content': 'Hello!'}]
        )
        print(f"{model}: {response['message']['content'][:100]}...")
    except Exception as e:
        print(f"Error with {model}: {e}")
```

#### 5. Image and Multimodal Models

```python
import ollama

# For multimodal models (if available)
response = ollama.chat(
    model='llava',
    messages=[
        {
            'role': 'user',
            'content': 'What do you see in this image?',
            'images': ['path/to/image.jpg']
        }
    ]
)
```

### Complete Example with Error Handling

```python
import ollama
import json

class OllamaClient:
    def __init__(self, model='llama3'):
        self.model = model
    
    def chat(self, message, system_prompt=None):
        try:
            messages = []
            
            if system_prompt:
                messages.append({'role': 'system', 'content': system_prompt})
            
            messages.append({'role': 'user', 'content': message})
            
            response = ollama.chat(
                model=self.model,
                messages=messages
            )
            
            return response['message']['content']
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def stream_chat(self, message, system_prompt=None):
        try:
            messages = []
            
            if system_prompt:
                messages.append({'role': 'system', 'content': system_prompt})
            
            messages.append({'role': 'user', 'content': message})
            
            response = ollama.chat(
                model=self.model,
                messages=messages,
                stream=True
            )
            
            full_response = ""
            for chunk in response:
                content = chunk['message']['content']
                full_response += content
                print(content, end='', flush=True)
            
            print()  # New line at the end
            return full_response
            
        except Exception as e:
            print(f"Error: {str(e)}")
            return ""

# Usage
client = OllamaClient('llama3')

# Regular chat
result = client.chat("Explain quantum computing in simple terms")
print(result)

# Streaming chat
print("Streaming response:")
client.stream_chat("Write a 50-word explanation of machine learning")
```

### Prerequisites

1. **Install Ollama**: Download and install Ollama from [ollama.com](https://ollama.com/download)
2. **Pull Models**: Download models you want to use:

   ```bash
   ollama pull llama3
   ollama pull mistral
   ollama pull phi3
   ollama pull gemma
   ```

### Key Parameters

- `model`: The model name (e.g., 'llama3', 'mistral')
- `messages`: List of message objects with 'role' and 'content'
- `stream`: Boolean to enable streaming responses
- `temperature`: Controls randomness (0.0 to 1.0)
- `max_tokens`: Maximum tokens to generate

### Common Models

- `llama3` - Llama 3 (recommended)
- `mistral` - Mistral
- `phi3` - Phi-3
- `gemma` - Gemma
- `llava` - For image understanding

This approach gives you full control over running local LLMs in Python with the convenience of the Ollama API.

Reviewed by Goose 2026-04-07 16:05