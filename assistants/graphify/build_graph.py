import json
import argparse
from pathlib import Path
from graphify.build import build_from_json
from graphify.cluster import cluster, score_all
from graphify.analyze import god_nodes, surprising_connections, suggest_questions
from graphify.report import generate
from graphify.export import to_json

def main():
    parser = argparse.ArgumentParser(description="Build and analyze the Graphify knowledge graph.")
    parser.add_argument("--extract-file", default="graphify-out/.graphify_extract.json", help="Path to the merged extraction JSON.")
    parser.add_argument("--detect-file", default="graphify-out/.graphify_detect.json", help="Path to the detection JSON.")
    parser.add_argument("--output-json", default="graphify-out/graph.json", help="Output path for the final graph JSON.")
    parser.add_argument("--output-report", default="graphify-out/GRAPH_REPORT.md", help="Output path for the audit report.")
    parser.add_argument("--labels", help="Path to a JSON file containing community labels.")
    parser.add_argument("--directed", action="store_true", help="Build a directed graph.")
    args = parser.parse_args()

    extract_path = Path(args.extract_file)
    detect_path = Path(args.detect_file)
    
    if not extract_path.exists():
        print(f"Error: Extraction file '{args.extract_file}' not found. Run extraction steps first.")
        return

    print(f"🏗️ Building graph from: {extract_path}")
    extraction = json.loads(extract_path.read_text())
    detection = json.loads(detect_path.read_text()) if detect_path.exists() else {"total_files": 0, "total_words": 0}

    # Step 4: Build, Cluster, Analyze
    G = build_from_json(extraction, directed=args.directed)
    
    print("🧬 Clustering communities...")
    communities = cluster(G)
    cohesion = score_all(G, communities)
    
    gods = god_nodes(G)
    surprises = surprising_connections(G, communities)
    
    # Load or generate labels
    if args.labels and Path(args.labels).exists():
        labels = json.loads(Path(args.labels).read_text())
        labels = {int(k): v for k, v in labels.items()}
        print(f"🏷️ Loaded {len(labels)} community labels.")
    else:
        labels = {cid: f"Community {cid}" for cid in communities}
        print(f"🏷️ Generated {len(communities)} default community labels.")

    questions = suggest_questions(G, communities, labels)
    
    print("📝 Generating report...")
    tokens = {'input': extraction.get('input_tokens', 0), 'output': extraction.get('output_tokens', 0)}
    report = generate(G, communities, cohesion, labels, gods, surprises, detection, tokens, str(Path('.').absolute()), suggested_questions=questions)
    
    Path(args.output_report).write_text(report)
    to_json(G, communities, args.output_json)

    # Save analysis for potential labeling step
    analysis = {
        'communities': {str(k): v for k, v in communities.items()},
        'cohesion': {str(k): v for k, v in cohesion.items()},
        'gods': gods,
        'surprises': surprises,
        'questions': questions,
    }
    Path('graphify-out/.graphify_analysis.json').write_text(json.dumps(analysis, indent=2))

    print(f"\n📊 Graph Complete!")
    print(f"Nodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}")
    print(f"Communities: {len(communities)}")
    print(f"\n✅ Final Data: {args.output_json}")
    print(f"✅ Audit Report: {args.output_report}")

if __name__ == "__main__":
    main()
