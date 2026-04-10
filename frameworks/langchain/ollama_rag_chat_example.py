import os
import sys
from dotenv import load_dotenv

# LangChain components
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Load environment variables from .env
load_dotenv()

# --- CONFIGURATION ---
# Default to Ollama Local API (Success Path)
OLLAMA_BASE_URL = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")
LLM_MODEL = os.getenv("OLLAMA_LLM_MODEL", "mistral:v0.3")
EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")

# Support for direct local file loading (Alternative Path)
# This uses parameters from your .env like MODELS_DIR_PATH
MODELS_DIR = os.getenv("MODELS_DIR_PATH")
MODEL_PATH = os.path.join(MODELS_DIR, os.getenv("MODEL_DIR_PATH", ""), os.getenv("MODEL_FILE_PATH", "")) if MODELS_DIR else None

def get_llm():
    """Returns the LLM based on available configuration."""
    # Priority: Local GGUF file if OLLAMA_LLM_MODEL is not set but MODEL_PATH is valid
    use_local_file = os.getenv("USE_LOCAL_FILE", "false").lower() == "true"
    
    if use_local_file and MODEL_PATH and os.path.isfile(MODEL_PATH):
        from langchain_community.chat_models import ChatLlamaCpp
        print(f"📦 Loading local GGUF model: {MODEL_PATH}")
        return ChatLlamaCpp(model_path=MODEL_PATH, temperature=0, n_ctx=4096)
    
    # Default: Ollama Local API
    print(f"📡 Using Ollama Local API at {OLLAMA_BASE_URL} (Model: {LLM_MODEL})")
    return ChatOllama(model=LLM_MODEL, base_url=OLLAMA_BASE_URL, temperature=0)

def get_embeddings():
    """Returns the Embeddings model."""
    # Priority: Local embeddings if OLLAMA_EMBED_MODEL is not set or USE_LOCAL_EMBED is true
    use_local_embed = os.getenv("USE_LOCAL_EMBED", "false").lower() == "true"
    
    if use_local_embed:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        print("🧬 Using local HuggingFace Embeddings")
        return HuggingFaceEmbeddings()
    
    # Default: Ollama Local API
    print(f"🧬 Using Ollama Embeddings: {EMBED_MODEL}")
    return OllamaEmbeddings(model=EMBED_MODEL, base_url=OLLAMA_BASE_URL)

def run_rag_example():
    print(f"🚀 Initializing Local RAG Example")
    print(f"--------------------------------")
    
    try:
        # 1. Initialize Components
        llm = get_llm()
        embeddings = get_embeddings()

        # 2. Prepare Knowledge (Loading from the provided PDF)
        pdf_path = os.path.join(os.path.dirname(__file__), ".local", "menu-template.pdf")
        print(f"\n📦 Loading PDF: {pdf_path}")
        
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"Could not find PDF at {pdf_path}")

        from langchain_community.document_loaders import PyPDFLoader
        from langchain_text_splitters import RecursiveCharacterTextSplitter

        loader = PyPDFLoader(pdf_path)
        docs = loader.load()
        
        # Split text into chunks for better retrieval
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)
        
        print(f"📄 Indexed {len(splits)} chunks from PDF.")
        
        vectorstore = FAISS.from_documents(splits, embeddings)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

        # 3. Create RAG Chain
        template = """Answer the question based only on the following context derived from the PDF:
        {context}

        Question: {question}
        """
        prompt = ChatPromptTemplate.from_template(template)

        chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

        # 4. Execute Query
        query = sys.argv[1] if len(sys.argv) > 1 else "based on the provided file what is the content of the menu?"
        print(f"\n👤 Question: {query}")
        print("🤖 Thinking...")
        
        response = chain.invoke(query)
        
        print(f"\n✅ Response:\n{response}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting Tips:")
        print(f"1. Ensure Ollama is running and models are pulled.")
        print(f"2. Check your .env for OLLAMA_LLM_MODEL and OLLAMA_EMBED_MODEL.")
        if MODELS_DIR:
            print(f"3. Local models directory detected at: {MODELS_DIR}")

if __name__ == "__main__":
    run_rag_example()
