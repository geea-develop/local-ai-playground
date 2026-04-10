# FlowiseAI POC Setup Guide

FlowiseAI is a low-code, drag-and-drop tool to build customized LLM biological circuits using LangChain. It is perfect for rapid prototyping of complex multi-step workflows.

## Prerequisites
- Docker and Docker Compose installed.

## Step-by-Step Installation

1. **Prepare the Directory**
   Ensure you are in the `interfaces/flowise/` directory.

2. **Configuration**
   Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
   *Note: By default, it uses port `3001` to avoid conflicts with Open WebUI (3000) or Dify (80).*

3. **Start FlowiseAI**
   Run the following command to start the container in the background:
   ```bash
   docker compose up -d
   ```

4. **Verify the Installation**
   Check if the container is running:
   ```bash
   docker ps | grep flowise
   ```

## Connecting to Local Models
To connect Flowise to your local backends (MLX, Ollama, LM Studio), use the following base URLs within the nodes:

- **Ollama:** `http://host.docker.internal:11434`
- **LM Studio / MLX (OpenAI API):** `http://host.docker.internal:1234/v1` (verify your actual port)

## Next Steps
1. Open your browser and navigate to: **http://localhost:3001**
2. In the "Marketplace", you can find templates for multi-step agents or RAG flows.
3. Drag a "ChatOllama" or "ChatOpenAI" node to get started!
