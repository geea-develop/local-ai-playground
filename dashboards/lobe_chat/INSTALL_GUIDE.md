# LobeChat POC Setup Guide

LobeChat is a stunning, heavily client-side Next.js based chat application. It thrives at managing dozens of different "agents" and connecting to global plugins.

## Step-by-Step Installation

1. **Start the Docker Container**
   LobeChat usually sits on port `3210`. The following command starts the minimal version required to test local models.
   
   To ensure LobeChat can freely communicate with your local MLX/Ollama/LocalAI models running on the Mac via Docker, we need to pass an environment variable mapping connections.

   ```bash
   docker run -d -p 3210:3210 \
     --add-host=host.docker.internal:host-gateway \
     -e OPENAI_API_KEY=sk-xxxx \
     -e OPENAI_PROXY_URL=http://host.docker.internal:8080/v1 \
     -e ACCESS_CODE=lobe66 \
     --name lobe-chat \
     lobehub/lobe-chat
   ```
   *Note: In the command above, `OPENAI_API_KEY` is a dummy key because local models don't need one, and `OPENAI_PROXY_URL` points to port `8080` (where your MLX/LocalAI server usually runs). If you're using Ollama, we can change the provider in the UI later.*

## Next Steps (Testing)

1. Open your browser and navigate to: **http://localhost:3210**
2. Important: Click the top left menu -> **Settings** -> **General** and enter the password: `lobe66` to unlock the app.
3. Once unlocked, you can jump straight to the "Agent Market" or test chatting. Let me know when you're in!
