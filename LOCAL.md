
<!-- LM Studio -->

lms server start --port 1234

lms load qwen/qwen3-4b-2507 -c 32000 --gpu 0.5

<!-- Goose -->

goose session --with-extension "docker run -i --rm mcp/duckduckgo"

goose session --with-builtin developer

● new session · custom_lm_studio qwen/qwen3-4b-2507

<!-- Ollama -->

brew services start ollama

OR 

OLLAMA_FLASH_ATTENTION="1" OLLAMA_KV_CACHE_TYPE="q8_0" /opt/homebrew/opt/ollama/bin/ollama serve
