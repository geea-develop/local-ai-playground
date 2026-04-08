# Project Structure & Terminology

This repository serves as a local AI playground and development environment. To keep things organized and easy to navigate, we have divided the projects, tools, and code into four main categories based on standard terminology.

## 📂 Directories

### 1. `frameworks/`
**Purpose**: Libraries, SDKs, and orchestration tools used to build agentic AI applications. These are the code abstractions that help developers chain calls, manage memory, and define tool use.
- **`langchain/`**: Experiments and tests with LangChain.
- **`smolagents/`**: Proof of concept builds with Hugging Face's smolagents.

### 2. `assistants/`
**Purpose**: Pre-built AI tools, CLI utilities, and autonomous agents designed to assist with coding and workflows.
- **`goose/`**: Configurations and usage examples for the Goose AI assistant.
- **`claude-cli/`**: Skills and plugins for the Anthropic Claude CLI tool.
- **`claude-lm-studio/`**: Custom integrations utilizing Claude and LM Studio.

### 3. `backends/`
**Purpose**: Open-source local execution engines, inference servers, and model runners. These components are responsible for hosting and serving the Large Language Models locally.
- **`ollama/`**: Projects directly relying on Ollama.
- **`localai/`**: Setups and API emulation using LocalAI.
- **`llm_runner/`**: Specialized orchestration for LLM inference.
- **`custom_servers/`**: Contains various custom backend configurations depending on the local hardware (e.g. `mlx-lm-server`, `mlx-openai-server`, `vllm-mlx`). 

### 4. `dashboards/`
**Purpose**: User interfaces and chat applications that consume APIs provided by the `backends/`, allowing for an easy way to chat with, compare, and fine-tune models through a graphical interface.
- Includes POCs and installation guides for UIs such as **Dify**, **Open WebUI**, **Lobe Chat**, and **Anything_LLM**.

## Guidelines for Adding New Tools

- **Building an app?** Use a tool from `frameworks/`.
- **Need a ready-made local UI?** Look in `dashboards/`.
- **Adding a new model serving inference?** Place it in `backends/`.
- **Testing a new autonomous coding CLI?** Place it in `assistants/`.
