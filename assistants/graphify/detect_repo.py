import json
from graphify.detect import detect
from pathlib import Path
import argparse

def main():
    parser = argparse.ArgumentParser(description="Run Graphify detection on a directory.")
    parser.add_argument("path", help="Path to the directory to index.")
    parser.add_argument("--output", default="graphify-out/.graphify_detect.json", help="Output path for the detection JSON.")
    args = parser.parse_args()

    input_path = Path(args.path)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"Error: Path '{args.path}' does not exist.")
        return

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"🔍 Running detection on: {input_path}")
    
    result = detect(input_path)
    
    output_path.write_text(json.dumps(result, indent=2))
    
    total = result.get('total_files', 0)
    words = result.get('total_words', 0)
    
    print(f"\n📊 Detection Complete!")
    print(f"Total Corpus: {total} files, ~{words} words")
    
    files = result.get('files', {})
    for ftype in ['code', 'document', 'image', 'video', 'paper']:
        file_list = files.get(ftype, [])
        if file_list:
            print(f"  - {ftype.capitalize()}: {len(file_list)} files")

    print(f"\n✅ Results saved to: {output_path}")

if __name__ == "__main__":
    main()
