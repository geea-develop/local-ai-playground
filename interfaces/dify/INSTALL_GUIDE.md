# Dify POC Setup Guide

This guide covers the steps required to spin up the Dify platform locally for evaluation.

> [!CAUTION]
> Dify consists of numerous microservices (Postgres, Redis, Weaviate, Sandbox, etc.). The initial `docker compose up -d` command will pull several large images. Make sure you have a fast connection and some disk space.

## Step-by-Step Installation

1. **Navigate to the setup directory**
   Before running anything, ensure you are in the correct directory. We have already cloned the repository for you into the `src` folder.
   ```bash
   cd interfaces/dify/src/docker
   ```

2. **Start the Docker Containers**
   The `.env` file has already been generated. Run the following command to pull the images and start the orchestrated containers in the background.
   ```bash
   docker compose up -d
   ```
   *Note: This will output a large block of pulling progress. It might take ~3-10 minutes depending on your internet connection.*

3. **Verify the Installation**
   Once the command finishes, check that all containers are running gracefully:
   ```bash
   docker compose ps
   ```

## Next Steps (Testing)

Once the containers are successfully running:
1. Open your browser and navigate to exactly: **http://localhost/install**
2. Follow the initial admin setup (create an account locally).
3. Let me know when you've reached the main console, and we will proceed to connect Dify to your local MLX/Ollama backends and test a simple Agent workflow.
