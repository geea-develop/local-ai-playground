# 🤖 AI Assistants & Coding Utilities

This directory holds configuration, research, and usage guides for pre-built AI assistants and specialized coding tools used in this playground.

## Purpose

The projects here are designed to be **autonomous or semi-autonomous helpers** that assist with development workflows, coding tasks, and system management. All assistants can be connected to the local backends defined in [`/backends`](../backends).

---

## 📦 Contents

| Assistant | Type | Status | Key Capability |
|---|---|---|---|
| **[goose/](./goose)** | AI Agent | ✅ Active | Open-source autonomous dev agent |
| **[claude/](./claude)** | CLI + Local LLM | ✅ Active | Anthropic Claude with local inference routing |
| **[graphify/](./graphify)** | Code Graph Tool | ✅ Active | AST-based codebase knowledge graph indexing |
| **[gemini-cli/](./gemini-cli)** | CLI Assistant | 🚧 In Progress | Google Gemini CLI integration |
| **[opencode/](./opencode)** | AI Coding Tool | 🚧 In Progress | Opencode AI coding assistant |
| **[github-copilot-cli/](./github-copilot-cli)** | CLI Assistant | 🚧 In Progress | GitHub Copilot CLI integration |

---

## 🛠 Assistant Details

### 🪿 Goose
Block's open-source autonomous AI coding agent. Designed for multi-step development tasks including writing code, running commands, and debugging — all driven by natural language instructions.
- **Setup:** [`goose/README.md`](./goose/README.md)
- **Docs:** [`docs/GOOSE.md`](../docs/GOOSE.md)

### ⬛ Claude (CLI + LM Studio)
Anthropic's Claude integrated in two ways:
- **`claude-cli/`**: Custom skills and slash commands for Claude Code CLI.
- **`claude-lm-studio/`**: Connects Claude's CLI to a locally running LM Studio inference server via a custom API proxy.
- **Setup:** [`claude/README.md`](./claude/) (see subdirectories)

### 📈 Graphify
A specialized tool for transforming code repositories into queryable **knowledge graphs** using AST parsing (`tree-sitter`). Provides AI assistants with structural, relationship-aware context instead of raw file contents, significantly reducing token usage.
- **Setup:** [`graphify/README.md`](./graphify/README.md)
- **Getting Started:** [`graphify/GETTING_STARTED.md`](./graphify/GETTING_STARTED.md)

### ♊ Gemini CLI *(In Progress)*
Integration setup for Google's Gemini CLI coding assistant.
- **Setup:** [`gemini-cli/README.md`](./gemini-cli/README.md)

### 🔷 Opencode *(In Progress)*
Setup and configuration for the Opencode AI coding assistant.
- **Setup:** [`opencode/README.md`](./opencode/README.md)

### 🐙 GitHub Copilot CLI *(In Progress)*
Configuration and usage tips for GitHub Copilot in the terminal.
- **Setup:** [`github-copilot-cli/README.md`](./github-copilot-cli/README.md)

---

## 💡 When to Use These

| Goal | Recommended Tool |
|---|---|
| Autonomous multi-step coding tasks | **Goose** |
| Quick code edits with deep codebase context | **Claude CLI** or **Gemini CLI** |
| Understanding a new, complex codebase | **Graphify** (build knowledge graph first) |
| Persistent memory across sessions | **Graphify** + **Cognee** (see `/frameworks/cognee`) |
| Inline code completions in terminal | **GitHub Copilot CLI** |
