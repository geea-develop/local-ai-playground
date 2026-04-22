# Getting Started with Goose

## What is Goose?
[Goose](https://block.github.io/goose/) is Block's open-source autonomous AI coding agent. It is designed to help developers build, manage, and iterate on software projects — executing terminal commands, writing code, browsing documentation, and debugging — all driven by natural language instructions.

---

## Installation

```bash
# Install via pip
pip install goose-ai

# Or follow the official install guide:
# https://block.github.io/goose/docs/getting-started/installation
```

---

## How to Get Started

1. **Install Goose**: Use `pip install goose-ai` or follow the [installation guide](https://block.github.io/goose/docs/getting-started/installation).
2. **Initialize a Project**: Run `goose session start` to begin a session in your project directory.
3. **Enable Developer Mode**: Use the developer toolkit for advanced coding and debugging capabilities.

---

## Session Management

```bash
# Start a new session
goose session start

# Resume a previous session
goose session resume

# List all sessions
goose session list
```

---

## Quick Start Examples

```bash
# Analyze code structure
goose "Explain the structure of this project"

# Run a shell command via Goose
goose "List all Python files in the src/ directory"

# Write and run code
goose "Create a Python script that pings the Ollama API and prints the available models"
```

---

## Integration with This Playground

Goose is used as the primary **autonomous coding agent** in this playground. It works best when given access to the full repository context.

> [!TIP]
> Combine Goose with **Graphify** (`assistants/graphify/`) to give it a structural knowledge graph of the codebase, dramatically reducing errors on large refactoring tasks.

### Recommended Workflow

1. Start an Ollama backend: `ollama serve`
2. Open the playground in your terminal
3. Start a Goose session: `goose session start`
4. Give Goose a task: _"Set up the Cognee framework and run the example"_

---

## Configuration

Goose reads configuration from `~/.config/goose/config.yaml`. Key settings:

```yaml
provider: ollama          # Use local Ollama as the LLM provider
model: mistral:v0.3       # Default model
```

---

## Resources

- [Official Documentation](https://block.github.io/goose/)
- [GitHub Repository](https://github.com/block/goose)
- [Extensions Registry](https://block.github.io/goose/docs/extensions/)