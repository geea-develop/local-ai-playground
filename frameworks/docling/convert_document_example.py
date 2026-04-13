import os
import sys
from docling.document_converter import DocumentConverter
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """
    Main entry point for the Docling document conversion example.
    """
    # The source can be a local file path or a URL
    source = "https://arxiv.org/pdf/2408.09869"
    
    print(f"--- Initializing DocumentConverter ---")
    converter = DocumentConverter()
    
    print(f"--- Converting source: {source} ---")
    try:
        # Perform the conversion
        result = converter.convert(source)
        
        # Export the document to Markdown
        markdown_output = result.document.export_to_markdown()
        
        print("\n--- Conversion Successful! ---")
        print("\nFirst 1000 characters of Markdown output:")
        print("-" * 40)
        print(markdown_output[:1000])
        print("-" * 40)
        
        # Optionally save to a file in .local directory
        output_dir = ".local/output"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "converted_doc.md")
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_output)
            
        print(f"\nFull converted document saved to: {output_path}")

        # Demonstrate table extraction if any
        if result.document.tables:
            print(f"\n--- Detected {len(result.document.tables)} tables ---")
            for i, table in enumerate(result.document.tables):
                df = table.export_to_dataframe()
                print(f"\nTable {i+1} preview:")
                print(df.head())
        
    except Exception as e:
        print(f"Error during conversion: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
