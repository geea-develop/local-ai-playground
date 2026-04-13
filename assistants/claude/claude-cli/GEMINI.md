# GEMINI.md

This project is a **Claude Playground** designed for exploring and developing extensions for Claude, specifically focusing on **Skills** (slash commands for Claude Code CLI) and **Plugins** (MCP Servers for Claude Desktop).

## Project Overview

- **Purpose**: A sandbox for building modular Python extensions to enhance AI interactions.
- **Main Technologies**: Python 3, Model Context Protocol (MCP), Claude Code CLI.
- **Architecture**:
    - **Plugins (`/plugins`)**: Class-based, stateful modules (e.g., `CachePlugin`, `ConfigPlugin`, `LoggerPlugin`) intended for integration as MCP servers.
    - **Skills (`.claude/skills/`)**: Modular instruction packages (e.g., `run-tests`, `check-style`, `deploy`) that can be mapped to slash commands in the Claude Code CLI. Each skill is stored in its own folder with a `SKILL.md` file.

## Building and Running

### Development Commands
The following commands are defined in `CLAUDE.md`, though they may require the creation of a `Makefile` or a `src/` directory to fully function:

- **Build**: `make build` (TODO: Implement Makefile)
- **Linting**: `flake8 src/` (TODO: Create src/ directory)
- **Testing**: `pytest tests/ -v` (TODO: Create tests/ directory)

### Running Plugins/Skills Manually
Each plugin and skill includes a `if __name__ == "__main__":` block for standalone testing.
```bash
python plugins/cache_plugin.py
python skills/math_skill.py
```

## Development Conventions

1.  **Plugins vs. Skills**:
    - Use **Plugins** (classes) for stateful logic or external integrations (MCP style).
    - Use **Skills** (functions) for simple, reusable data transformations or utility tasks.
2.  **Modular Design**: Every plugin or skill should be self-contained in its own file with a clear interface.
3.  **Documentation**: Each module must include a docstring explaining its purpose and usage.
4.  **CLI Integration**: Custom skills are modular packages in `.claude/skills/`.

## Key Files

- `README.md`: Comprehensive guide on the difference between Skills and Plugins and how to set up an MCP server.
- `CLAUDE.md`: Configuration file for Claude Code CLI.
- `plugins/`: Implementation of modular extensions (Cache, Config, Logger).
- `skills/`: Implementation of utility functions (Math, Data, Text Processing).
