# 🎨 LobeChat POC Setup Guide

LobeChat is a highly polished, heavily client-side chat application. It excels at managing diverse "Agent Markets" and has a beautiful UI that feels like a native macOS app.

---

## 🛠 Prerequisites

- **Docker Desktop**
- **Ollama** running locally on your Mac.

---

## 📦 Installation Steps

### 1. Launch LobeChat
Navigate to the directory and start the container.
```bash
cd interfaces/lobe_chat
docker compose up -d
```

### 2. Access the UI
Open your browser and navigate to: **[http://localhost:3210](http://localhost:3210)**

### 3. Unlock and Configure
1.  **Unlock**: Click the top left menu $\rightarrow$ **Settings** $\rightarrow$ **General**. Enter the password: `lobe66`.
2.  **Enable Ollama**: 
    - Go to **Settings** $\rightarrow$ **Language Model**.
    - Find the **Ollama** tab.
    - Toggle it to **Enabled**.
    - The Proxy URL should already be working (`http://host.docker.internal:11434/v1`).
3.  **Select Model**: You should now see your `mistral:v0.3` in the model selection list!

---

## 🧪 Testing the "Agent Market"

LobeChat's best feature is its pre-built agents.
1. Click the **Agents** icon (the robot head).
2. Browse the market and select one (e.g., "English Teacher" or "Code Expert").
3. LobeChat will apply the system prompt automatically and use your local Mistral model to run the persona.

> [!TIP]
> LobeChat is primarily a "Chat Client." It is much faster than Dify but lacks the heavy visual workflow builders. Use this for your daily interaction with local models.
