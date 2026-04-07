from llama_cpp import Llama

# ... load llm as above ...

prompt = "Tell me a story about AI"
for token in llm(prompt, stream=True):
    # Access the generated text as it comes in
    print(token['choices'][0]['text'], end='', flush=True)
