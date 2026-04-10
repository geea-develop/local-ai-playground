# 🚀 Dify Getting Started: Local RAG Platform

This guide documents the validated "Golden Path" for setting up a fully private, local AI Platform using **Dify** and **Ollama**. Unlike Flowise, Dify provides an "Application-style" interface with built-in user management and advanced citation tracking.

---

## 🛠 1. Backend Requirements (Ollama)

Dify requires two separate models to handle RAG successfully. Ensure these are running in Ollama:

```bash
# Chat & Orchestration Model
ollama pull mistral:v0.3

# Embedding Model (Required for High-Quality Indexing)
ollama pull nomic-embed-text
```

---

## ⚙️ 2. Global Model Configuration

In Dify, models are configured at the **System Level**, not inside individual apps.

1.  Navigate to **Settings** (Account Menu) $\rightarrow$ **Model Provider**.
2.  Locate **Ollama** and configure the following:
    - **LLM Model**: 
        - Name: `mistral:v0.3`
        - Base URL: `http://host.docker.internal:11434`
    - **Text Embedding Model**: 
        - Name: `nomic-embed-text`
        - Base URL: `http://host.docker.internal:11434`

---

## 📚 3. Creating Knowledge (The Index)

1.  Click **Knowledge** in the top navigation bar.
2.  Click **Create Knowledge** and upload your document (PDF, Text, Markdown).
3.  **Important:** Under Index Mode, select **High Quality**. This will trigger the `nomic-embed-text` model to vectorize your data.
4.  Wait for the status to reach `Completed`.

---

## 🏗 4. Building your First App

1.  Go to **Studio** $\rightarrow$ **Create from Scratch**.
2.  Select **Chatbot**.
3.  **Setup Instructions**:
    - **Model (Top Right)**: Ensure `mistral:v0.3` is selected.
    - **Context**: Click **Add** and select your Knowledge Base.
    - **Instructions**: Define the persona (e.g., *"You are a local document expert"*).
4.  **Test**: Use the Preview window on the right to query your document.

---

## 📌 Maintenance & Tips

- **Resource Usage:** Dify is a heavy microservice stack. If you experience timeouts or "Killed" errors, ensure Docker Desktop has at least **8GB of RAM** allocated.
- **Citations:** Dify excels at showing exactly where its information came from. Click the "Source" icon in the chat response to verify the chunk retrieval.
- **Native vs Plugin:** Always use the **Native Ollama Provider** in Settings rather than the Ollama "Plugin" for the most stable connection to local models.
