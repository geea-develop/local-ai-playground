# Docling Framework

[Docling](https://github.com/DS4SD/docling) is a powerful tool for document conversion, enabling you to transform complex documents (PDFs, DOCX, HTML, PPTX, and more) into structured formats like Markdown and JSON. It is particularly useful for preparing data for RAG (Retrieval-Augmented Generation) pipelines.

## Features

- **High-Quality Conversion**: Converts layouts, tables, and text with high precision.
- **Multimodal Support**: Handles multiple file formats beyond just PDF.
- **Table Extraction**: Detects and extracts tables into structural formats like Pandas DataFrames.
- **RAG Ready**: Provides chunking strategies for context-aware document segmentation.

## Getting Started

### 1. Set up Environment
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment
Copy `.env.example` to `.env` if you need custom configurations.
```bash
cp .env.example .env
```

## Examples

- `convert_document_example.py`: Simple conversion of a PDF (local or remote) to Markdown.

## Usage Example

```python
from docling.document_converter import DocumentConverter

source = "https://arxiv.org/pdf/2408.09869"
converter = DocumentConverter()
result = converter.convert(source)

print(result.document.export_to_markdown())
```

## Resources
- [Official Repository](https://github.com/DS4SD/docling)
- [Documentation](https://docling.ai/)
