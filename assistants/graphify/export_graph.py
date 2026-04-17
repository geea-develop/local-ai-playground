import json
import argparse
from pathlib import Path
from graphify.build import build_from_json
from graphify.export import to_html, to_svg, to_graphml, to_cypher, to_obsidian, to_canvas

def main():
    parser = argparse.ArgumentParser(description="Export Graphify graph to various formats.")
    parser.add_argument("--extract-file", default="graphify-out/.graphify_extract.json", help="Path to the merged extraction JSON.")
    parser.add_argument("--analysis-file", default="graphify-out/.graphify_analysis.json", help="Path to the analysis JSON.")
    parser.add_argument("--labels-file", default="graphify-out/.graphify_labels.json", help="Path to the labels JSON.")
    parser.add_argument("--format", choices=['html', 'svg', 'graphml', 'cypher', 'obsidian'], default='html', help="Export format.")
    parser.add_argument("--output-dir", default="graphify-out", help="Output directory.")
    args = parser.parse_args()

    extract_path = Path(args.extract_file)
    analysis_path = Path(args.analysis_file)
    labels_path = Path(args.labels_file)
    output_dir = Path(args.output_dir)

    if not extract_path.exists() or not analysis_path.exists():
        print("Error: Required JSON files not found. Run build_graph.py first.")
        return

    print(f"📦 Loading graph and analysis...")
    extraction = json.loads(extract_path.read_text())
    analysis = json.loads(analysis_path.read_text())
    labels_raw = json.loads(labels_path.read_text()) if labels_path.exists() else {}

    G = build_from_json(extraction)
    communities = {int(k): v for k, v in analysis['communities'].items()}
    cohesion = {int(k): v for k, v in analysis['cohesion'].items()}
    labels = {int(k): v for k, v in labels_raw.items()}

    output_dir.mkdir(parents=True, exist_ok=True)

    if args.format == 'html':
        output_file = output_dir / "graph.html"
        to_html(G, communities, str(output_file), community_labels=labels or None)
        print(f"✅ HTML Visualization: {output_file}")

    elif args.format == 'svg':
        output_file = output_dir / "graph.svg"
        to_svg(G, communities, str(output_file), community_labels=labels or None)
        print(f"✅ SVG Export: {output_file}")

    elif args.format == 'graphml':
        output_file = output_dir / "graph.graphml"
        to_graphml(G, communities, str(output_file))
        print(f"✅ GraphML Export: {output_file}")

    elif args.format == 'cypher':
        output_file = output_dir / "cypher.txt"
        to_cypher(G, str(output_file))
        print(f"✅ Cypher Export (Neo4j): {output_file}")

    elif args.format == 'obsidian':
        vault_dir = output_dir / "obsidian"
        n = to_obsidian(G, communities, str(vault_dir), community_labels=labels or None, cohesion=cohesion)
        to_canvas(G, communities, str(vault_dir / "graph.canvas"), community_labels=labels or None)
        print(f"✅ Obsidian Vault: {n} notes in {vault_dir}/")
        print(f"✅ Obsidian Canvas: {vault_dir}/graph.canvas")

if __name__ == "__main__":
    main()
