import os
import sys
from smolagents import OpenAIServerModel
from dotenv import load_dotenv

# RAG components
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings

# Load environment variables
load_dotenv()

# --- CONFIGURATION ---
OLLAMA_BASE_URL = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")
# mistral:v0.3 is generally more stable for simple RAG than llama3 on local hardware
LLM_MODEL = os.getenv("OLLAMA_LLM_MODEL", "mistral:v0.3")
EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")

class SimpleRetriever:
    """A wrapper for PDF retrieval logic using LangChain."""
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.vectorstore = self._initialize_vectorstore()
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})

    def _initialize_vectorstore(self):
        print(f"📦 Indexing PDF: {self.pdf_path}")
        if not os.path.exists(self.pdf_path):
            raise FileNotFoundError(f"PDF file not found: {self.pdf_path}")
            
        loader = PyPDFLoader(self.pdf_path)
        docs = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
        splits = text_splitter.split_documents(docs)
        
        embeddings = OllamaEmbeddings(model=EMBED_MODEL, base_url=OLLAMA_BASE_URL)
        return FAISS.from_documents(splits, embeddings)

    def get_context(self, query: str) -> str:
        docs = self.retriever.invoke(query)
        return "\n---\n".join([d.page_content for d in docs])

def main():
    print("\n" + "="*50)
    print("🚀 Running smolagents Local RAG (Simple)")
    print("="*50 + "\n")

    # 1. Setup Model
    model = OpenAIServerModel(
        model_id=LLM_MODEL,
        api_base=f"{OLLAMA_BASE_URL}/v1",
        api_key="ollama"
    )

    # 2. Path to local PDF
    pdf_path = os.path.join(os.path.dirname(__file__), ".local", "menu-template.pdf")

    try:
        # 3. Initialize Retriever
        retriever = SimpleRetriever(pdf_path)

        # 4. Input Query
        default_query = "What are the main items in the menu, and what are their prices?"
        user_query = sys.argv[1] if len(sys.argv) > 1 else default_query
        
        print(f"\n👤 Question: {user_query}")
        
        # 5. Retrieve Context
        print("🔍 Searching documents...")
        context = retriever.get_context(user_query)
        
        # 6. Call Model directly with a retrieval prompt
        # This is more stable for local models than multi-step agents
        prompt = f"""Use the following pieces of context to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context:
{context}

Question: {user_query}

Answer:"""

        print("🤖 Thinking...")
        response = model(messages=[{"role": "user", "content": prompt}])
        
        print("\n" + "✅ Response:")
        print("-" * 30)
        print(response.content)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Tip: Ensure Ollama is running (ollama serve) and models are pulled.")

if __name__ == "__main__":
    main()
