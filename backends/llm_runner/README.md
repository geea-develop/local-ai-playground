# LLM Runner: A Guide to Python Libraries for Running Local LLMs

<!-- Description -->

When it comes to running local large language models (LLMs) in Python, there are several libraries to choose from, each with its own strengths and weaknesses. Here's a quick overview of the most popular options:

<!-- Tested -->

1. The Best Balance: llama-cpp-python (via Ollama or direct install)
Recommended for: Most users, especially those with NVIDIA GPUs or who want a drop-in replacement for LM Studio's capabilities in code.

This is the official Python binding for the llama.cpp C++ library (which LM Studio also uses).

Pros: Fast, supports GPU offloading (CUDA/Metal), easy to use, actively maintained.
Cons: Requires installing the library (can be tricky on some systems without pre-built wheels).

Note: To get pre-compiled wheels that support CUDA easily, many developers wrap this with Ollama. You can run ollama run qwen2.5:7b and then import the model in Python using the Ollama bindings if available, or pull the GGUF and use llama-cpp-python directly as shown above.

2. The Enterprise/Research Standard: transformers (Hugging Face)
Recommended for: Researchers, complex pipelines, multi-modal models, or when you need specific Hugging Face features (like automatic prompt templates).

Pros: Industry standard, huge ecosystem, works on CPU/GPU/NPU.
Cons: Can be slower on inference than llama-cpp-python due to overhead; GPU memory management can be less efficient unless tuned perfectly.

Critical Tip for Speed: If using transformers, always use llama-cpp-python's underlying logic if possible, but if sticking with transformers, ensure you are using Flash Attention 2 (available via flash-attn library) to achieve speeds comparable to llama.cpp.

3. The Apple Silicon Supercharger: mlx-lm
Recommended for: Mac users (M1/M2/M3/M4 chips).

Pros: Blazing fast on Apple hardware, extremely low memory footprint, uses unified memory efficiently.
Cons: Only works on macOS/Apple Silicon. Not available for Windows/Linux.

No Server, no code. Just a simple Python library that runs the model directly on your Mac's Apple Silicon chip with incredible speed and efficiency.
```bash
mlx_lm.generate --model "/path/to/your/models/lmstudio-community/Qwen3-4B-Instruct-2507-MLX-4bit" --prompt "hello"
```

<!-- Next -->

4. The Lightweight Option: pyllamacpp
Recommended for: Users who want a simple, minimal wrapper around llama.cpp without the full Hugging Face ecosystem.

Pros: Lightweight, easy to install, minimal dependencies.
Cons: Less feature-rich than transformers, may not be as actively maintained or optimized as llama-cpp-python.

This is not supported by Apple M1/M2/M3/M4 chips, so if you're on a Mac, it's best to stick with mlx-lm or llama-cpp-python.

5. The Cutting Edge: Direct llama.cpp C++ bindings
Recommended for: Developers who want maximum performance and are comfortable working with C++ or creating their own Python bindings.

Pros: Maximum performance, full control over the library.
Cons: Requires C++ development skills, more complex to set up and maintain.

<!-- Advanced -->

1. Using Chat Templates
If you want to use system prompts or chat history (like "User: ... Assistant: ..."), LM Studio handles this visually. In Python, you can manually construct the prompt using the tokenizer:

2. Streaming Output
To see text appear character-by-character (like a chatbot), use the streaming argument:

3. Example: Running a Local Model with LangChain (via llama-cpp)
This example connects your local CPU/GPU setup to the LangChain framework so you can build an "Agent" that can browse the web or read files, not just chat.

How this works under the hood:
When ChatLlamaCpp is initialized, LangChain internally uses the llama-cpp-python library to load the .gguf file. If you have an NVIDIA GPU and set n_gpu_layers=-1, LangChain will automatically move the model weights to your VRAM for inference speed.

4. vLLM (Best for Production/Chat Interfaces)
If you want to build a chatbot interface (like what LM Studio shows but via API) or serve the model to multiple users, vLLM is currently the state-of-the-art.

Why use it: It uses PagedAttention, a technique that manages memory incredibly efficiently. It is much faster than standard transformers for continuous batching (handling many requests at once).
How to run: You usually run it as a server, then connect LangChain via the Hugging Face Inference Client.

Reviewed by Goose 2026-04-07 16:05