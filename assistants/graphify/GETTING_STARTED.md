# Getting Started with Graphify

This guide will walk you through setting up and using **Graphify** to index your local repository into a queryable knowledge graph.

## 📋 Prerequisites

- **Python 3.10+**
- An AI coding assistant (Claude Code, Cursor, Gemini CLI, etc.) with a configured API key.
- (Optional) **Node.js/npm** if using specific CLI wrappers.

## 🚀 Step 1: Installation

Install the Graphify package from PyPI and run the initialization:

```bash
# Install the core package
pip install graphifyy

# Initialize Graphify (sets up tree-sitter parsers and local dependencies)
graphify install
```

## 🔍 Step 2: Indexing your Repository

To build a knowledge graph of this repository or any specific folder, use the `/graphify` command:

```bash
# Index the current directory
/graphify .

# Or index a specific subdirectory (e.g., frameworks)
/graphify ./frameworks
```

## 📊 Step 3: Exploring the Results

Once indexing is complete, Graphify generates a `graphify-out/` directory with the following assets:

- **`graph.html`**: An interactive, 3D visualization of your codebase that you can open in any browser.
- **`GRAPH_REPORT.md`**: A summary of "God Nodes" (central components), "Surprises" (unexpected relationships), and suggested questions to ask your AI.
- **`graph.json`**: The persistent, queryable graph structure used by AI assistants.
- **`cache/`**: Incremental cache to speed up subsequent indexing.

## 🤖 Step 4: Interacting via AI Assistants

With the graph built, you can use specialized commands within your AI coding assistant:

- **Query**: Ask specific structural questions.
  ```bash
  /graphify query "How does authentication flow through the system?"
  ```
- **Path**: Find the relationship between two files or components.
  ```bash
  /graphify path "auth_logic.py" "user_model.py"
  ```
- **Explain**: Get a high-level architectural overview of a community/module.
  ```bash
  /graphify explain "interface-orchestration"
  ```

## 🛡️ Privacy & Security

- **Local Processing**: Code parsing and graph construction happen entirely on your machine.
- **Semantic Extraction**: Only semantic descriptions and relationship metadata are sent to the AI model—**never your raw source code.**
- **No Vector Stores**: Graphify uses graph topology and clustering (Leiden algorithm) rather than vector embeddings, meaning no heavy local database setups are required.

## 💡 Tips for Best Results

1. **Large Repositories**: Use `/graphify` on specific subdirectories if you only need to understand one part of a large system.
2. **Commit the Graph?**: You can add `graphify-out/` to your `.gitignore` to keep it local, or commit it if you want team members to have an immediate architectural map.
3. **Multi-Modal**: Graphify automatically reads diagrams and transcribes videos if it finds them—perfect for repositories with visual documentation.
