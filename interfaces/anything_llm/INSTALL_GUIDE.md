# AnythingLLM POC Setup Guide

AnythingLLM is optimized for chatting with your documents via Retrieval-Augmented Generation (RAG) within customizable workspaces.

https://github.com/Mintplex-Labs/anything-llm

## Step-by-Step Installation

1. **Prepare the storage directory**
   AnythingLLM requires a local folder to store its vector database, documents, and environment variables. We will create this in the POC folder.

   ```bash
   cd interfaces/anything_llm
   export STORAGE_LOCATION=$(pwd)/storage
   mkdir -p $STORAGE_LOCATION
   touch "$STORAGE_LOCATION/.env"
   ```

2. **Start the Docker Container**
   Run the following command to start AnythingLLM, exposing it on port `3001`.

   ```bash
   docker run -d -p 3001:3001 \
     --cap-add SYS_ADMIN \
     -v ${STORAGE_LOCATION}:/app/server/storage \
     -v ${STORAGE_LOCATION}/.env:/app/server/.env \
     -e STORAGE_DIR="/app/server/storage" \
     --name anythingllm \
     mintplexlabs/anythingllm
   ```

## Next Steps (Testing)

1. Open your browser and navigate to: **http://localhost:3001**
2. You will be greeted by an onboarding flow.
3. During setup, you can either select a built-in default provider, or point it to your local models (using `http://host.docker.internal:8080/v1` for example, if MLX is running).
4. Let me know when you reach the UI, and we can test the workspace functionality!
