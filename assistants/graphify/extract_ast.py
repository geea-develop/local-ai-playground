import json
from graphify.extract import collect_files, extract
from pathlib import Path
import argparse

def main():
    parser = argparse.ArgumentParser(description="Run Graphify AST extraction on detected code files.")
    parser.add_argument("--detect-file", default="graphify-out/.graphify_detect.json", help="Path to the detection JSON.")
    parser.add_argument("--output", default="graphify-out/.graphify_ast.json", help="Output path for the AST JSON.")
    args = parser.parse_args()

    detect_path = Path(args.detect_file)
    output_path = Path(args.output)

    if not detect_path.exists():
        print(f"Error: Detection file '{args.detect_file}' not found. Run detect_repo.py first.")
        return

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"🧬 Reading detection results from: {detect_path}")
    detect_data = json.loads(detect_path.read_text())
    
    code_files = []
    # Collect code files from the detection result
    raw_files = detect_data.get('files', {}).get('code', [])
    for f in raw_files:
        p = Path(f)
        if p.exists():
            code_files.extend(collect_files(p) if p.is_dir() else [p])

    if code_files:
        print(f"🔍 Extracting AST from {len(code_files)} files...")
        result = extract(code_files)
        
        output_path.write_text(json.dumps(result, indent=2))
        
        nodes = len(result.get("nodes", []))
        edges = len(result.get("edges", []))
        
        print(f"\n📊 Extraction Complete!")
        print(f"AST Graph: {nodes} nodes, {edges} edges")
        print(f"Tokens Used: Input={result.get('input_tokens', 0)}, Output={result.get('output_tokens', 0)}")
    else:
        print("⚠️ No code files found - creating empty AST.")
        empty_result = {'nodes': [], 'edges': [], 'input_tokens': 0, 'output_tokens': 0}
        output_path.write_text(json.dumps(empty_result, indent=2))

    print(f"\n✅ Results saved to: {output_path}")

if __name__ == "__main__":
    main()
