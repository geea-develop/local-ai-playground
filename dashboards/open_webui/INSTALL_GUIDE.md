# Open WebUI POC Setup Guide

Open WebUI is a highly polished, ChatGPT-like interface designed specifically for local LLMs. It is lightweight since it runs in a single container.

## Step-by-Step Installation

1. **Start the Docker Container**
   Run the following single command in your terminal. We are mapping port `3000` to avoid conflicts, and using `--add-host=host.docker.internal:host-gateway` so the container can talk to your local Mac services (like MLX or Ollama).

   ```bash
   docker run -d -p 3000:8080 \
     --add-host=host.docker.internal:host-gateway \
     -v open-webui:/app/backend/data \
     --name open-webui \
     --restart always \
     ghcr.io/open-webui/open-webui:main
   ```

2. **Verify the Installation**
   It should be very fast. Run:
   ```bash
   docker ps | grep open-webui
   ```

## Next Steps (Testing)

1. Open your browser and navigate to: **http://localhost:3000**
2. Create your first admin account locally.
3. To connect to our local models (MLX/LM Studio/Ollama), we will need to go to **Admin Panel > Settings > Connections** and input the `host.docker.internal` URLs. Let me know when you are ready to do this!
