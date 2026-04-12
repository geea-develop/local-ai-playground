# 🚀 Getting Started with Onyx

Welcome to the Onyx POC! This playground is designed to help you evaluate Onyx as your local Enterprise RAG solution.

## 🎯 Key Objectives

1. **Connect Data Sources**: Index a few local files or a GitHub repo to test the RAG performance.
2. **Local Inference**: Route all queries through your local Ollama or LM Studio backend.
3. **Hybrid Search**: Evaluate how Onyx combines keyword (BM25) and vector search.

## 📁 Project Structure

- `INSTALL_GUIDE.md`: Detailed setup instructions.
- `src/`: The cloned Onyx repository (after installation).

## 💡 Quick Tips

- **Model Selection**: For embedding, Onyx uses a default local model (sentence-transformers). You can change this in the admin settings.
- **Connectors**: Onyx has 50+ built-in connectors. Start with the "File" connector for a quick test.
- **Port Conflicts**: Onyx uses port `3000` by default. If it's already used by Open WebUI, you may need to change `APP_PORT` in your `.env`.

---

## 📅 Roadmap for this POC

- [ ] Successful Docker deployment.
- [ ] Connect to local Ollama (Llama 3).
- [ ] Index first 10 documents.
- [ ] First successful answer with citations.
