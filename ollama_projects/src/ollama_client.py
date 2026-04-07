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

