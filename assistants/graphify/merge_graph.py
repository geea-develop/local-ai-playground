import json
from pathlib import Path
import argparse

def main():
    parser = argparse.ArgumentParser(description="Merge AST and Semantic extraction results for Graphify.")
    parser.add_argument("--ast-file", default="graphify-out/.graphify_ast.json", help="Path to the AST JSON.")
    parser.add_argument("--semantic-file", default="graphify-out/.graphify_semantic.json", help="Path to the semantic JSON.")
    parser.add_argument("--output", default="graphify-out/.graphify_extract.json", help="Output path for the merged extract JSON.")
    args = parser.parse_args()

    ast_path = Path(args.ast_file)
    sem_path = Path(args.semantic_file)
    output_path = Path(args.output)

    if not ast_path.exists() and not sem_path.exists():
        print("Error: Neither AST nor Semantic files found. Run extraction steps first.")
        return

    print("🔗 Merging results...")
    
    ast = json.loads(ast_path.read_text()) if ast_path.exists() else {'nodes': [], 'edges': []}
    sem = json.loads(sem_path.read_text()) if sem_path.exists() else {'nodes': [], 'edges': [], 'hyperedges': [], 'input_tokens': 0, 'output_tokens': 0}

    # Merge: AST nodes first, then deduplicate semantic nodes by ID
    seen_nodes = {n['id'] for n in ast.get('nodes', [])}
    merged_nodes = list(ast.get('nodes', []))
    
    for n in sem.get('nodes', []):
        if n['id'] not in seen_nodes:
            merged_nodes.append(n)
            seen_nodes.add(n['id'])
            
    merged_edges = ast.get('edges', []) + sem.get('edges', [])
    merged_hyperedges = sem.get('hyperedges', [])
    
    merged = {
        'nodes': merged_nodes,
        'edges': merged_edges,
        'hyperedges': merged_hyperedges,
        'input_tokens': sem.get('input_tokens', 0),
        'output_tokens': sem.get('output_tokens', 0),
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(merged, indent=2))

    print(f"\n📊 Merge Complete!")
    print(f"Total Nodes: {len(merged_nodes)} ({len(ast.get('nodes', []))} AST + {len(sem.get('nodes', []))} semantic)")
    print(f"Total Edges: {len(merged_edges)}")
    print(f"Total Hyperedges: {len(merged_hyperedges)}")
    print(f"\n✅ Results saved to: {output_path}")

if __name__ == "__main__":
    main()
