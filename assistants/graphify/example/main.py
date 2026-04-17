"""
Main entry point for the Mini-RAG example.
Connects the Ingestor, Processor, and Storage components.
"""
from src.ingestor import Ingestor
from src.processor import Processor
from src.storage import Storage

def run_pipeline(data_source: str):
    print(f"Starting pipeline for: {data_source}")
    
    # 1. Ingest
    ingestor = Ingestor()
    raw_data = ingestor.fetch(data_source)
    
    # 2. Process
    processor = Processor()
    processed_data = processor.clean(raw_data)
    
    # 3. Store
    storage = Storage(db_type="local_vector_db")
    storage.save(processed_data)
    
    print("Pipeline complete.")

if __name__ == "__main__":
    run_pipeline("https://example.com/docs")
