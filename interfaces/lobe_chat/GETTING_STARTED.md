# 🎨 LobeChat Getting Started: Premium Chat Client

LobeChat is the most polished chat interface in the playground. It is designed for high-quality user interaction, managing diverse agent personas, and utilizing a rich plugin ecosystem.

---

## 🛠 1. The Critical "CORS" Fix (Required)

LobeChat runs in your browser and tries to talk to Ollama directly. For security reasons, Ollama blocks these requests by default. You **must** enable Cross-Origin Resource Sharing (CORS).

### On macOS:
1.  **Quit Ollama** from the macOS Menu Bar.
2.  Run the following in your terminal:
    ```bash
    launchctl setenv OLLAMA_ORIGINS "*"
    ```
3.  **Restart Ollama** from your Applications folder.

---

## 🏗 2. Launching & Unlocking

1.  **Start Container**:
    ```bash
    cd interfaces/lobe_chat
    docker compose up -d
    ```
2.  **Unlock the UI**:
    - Go to **[http://localhost:3210](http://localhost:3210)**.
    - Go to **Settings** $\rightarrow$ **General**.
    - Enter the Access Code: **`lobe66`**.

---

## ⚙️ 3. Ollama Configuration

1.  Go to **Settings** $\rightarrow$ **Language Model** $\rightarrow$ **Ollama**.
2.  Ensure **Ollama** is toggled to **Enabled**.
3.  Set the Proxy URL to: `http://localhost:11434` (or `http://host.docker.internal:11434`).
4.  Click the **Refresh** icon to see your local models (e.g., `mistral:v0.3`).

---

## 🤖 4. Using the Agent Market

LobeChat’s greatest strength is its built-in Agent Market.
1. Click the **Agents** icon in the left sidebar.
2. Click **Add** cross to search the market.
3. Select a persona (e.g., "Software Architect").
4. LobeChat will use your local Mistral model to play that character using its custom system prompts.

---

## 📌 Maintenance Notes
- **Lighter Footprint:** LobeChat is significantly lighter than Dify or Flowise. You can often leave it running in the background.
- **Plugins:** You can enable plugins (like Web Search or DALL-E) in the Settings, but some of these may require external API keys.
