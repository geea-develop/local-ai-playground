# Graphify

> [!TIP]
> **New to Graphify?** Check out the **[Getting Started Guide](./GETTING_STARTED.md)** for a step-by-step setup!

[Graphify](https://github.com/safishamsi/graphify) is a specialized AI coding assistant skill designed to transform folders of code, documents, papers, images, and videos into a queryable knowledge graph. It allows AI assistants to understand complex codebases and architectural designs through relationships rather than just raw text.

## 🚀 Key Features

- **Knowledge Graph Extraction**: Turns code structures (classes, functions, imports) into a persistent graph using AST parsing (tree-sitter).
- **Multi-Modal Support**: Processes images, videos (transcribed with Whisper), and documents.
- **Semantic Understanding**: Uses LLM subagents to extract design rationale and entity relationships.
- **High Efficiency**: Designed to use significantly fewer tokens by querying a graph instead of reading full files.

## 🛠 Installation

Graphify is available on PyPI as `graphifyy`.

```bash
pip install graphifyy
```

## 📖 Usage

### Example Project
Explore the **[Example Mini-RAG Project](./example)** to see how Graphify maps a multi-module Python application with local backends.

### Detection Utility
We've included a helper script to quickly analyze any directory before full indexing:
```bash
python detect_repo.py ./example
```

### Extraction Utility
Once detected, you can extract the codebase structure (AST) into a graph:
```bash
python extract_ast.py
```

### Full Pipeline Simulation
If you want to test the graph construction and report generation locally without an AI agent, follow the **[Simulation Guide](./SIMULATION_GUIDE.md)** which covers the step-by-step utility workflow:
1. **Detect** -> 2. **Extract** -> 3. **Merge** -> 4. **Build** -> 5. **Export**

### Slash Command Integration
Graphify is primarily designed to work as a skill within AI coding environments. Use the following command in supported CLI assistants (like Claude Code, Cursor, or Gemini CLI):

```bash
/graphify
```

### Manual Indexing
You can also run it directly to index a directory:

```bash
graphify index /path/to/your/repo
```

## 🧩 Integration with this Repository

Graphify is a powerful addition to the `assistants/` suite, complementing tools like Goose and the Claude CLI. It provides the "context engine" that helps these assistants navigate the `local_ai_playground` infrastructure more effectively.

- **For Claude CLI**: Enhances codebase navigation.
- **For Goose**: Provides a structural map for autonomous agents.
- **For Cognee**: While Cognee provides a general semantic memory framework, Graphify is highly specialized for code-first knowledge graph construction.

## 🔗 Resources
- [GitHub Repository](https://github.com/safishamsi/graphify)
- [PyPI Package](https://pypi.org/project/graphifyy/)
- [Website](https://graphify.net/)