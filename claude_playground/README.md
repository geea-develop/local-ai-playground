# Claude Plugins & Skills Guide

## Overview

This guide explains the differences between **Claude Skills** and **Claude Plugins**, and provides step-by-step instructions to help you choose and build the right extension for your needs.

---

## The Difference: Plugins vs. Skills

### Claude Skills

**What they are**: Slash-command actions (e.g., `/bug`, `/review`, `/help`) that Claude Code can execute to perform specific tasks.

- **Purpose**: Designed for developer workflows—automate coding tasks like debugging, code review, testing, or deployment.
- **How they work**: Defined in a `.claude/skills/` folder with a `SKILL.md` file. Claude Code CLI loads these and makes them available as slash commands.
- **Example**: A custom skill `/run-tests` could automate your project's testing steps.
- **Scope**: Code-focused and tied to Claude Code CLI.

### Claude Plugins (MCP Servers)

**What they are**: External integrations built using the **Model Context Protocol (MCP)**—tools that Claude can call during conversations to interact with external systems.

- **Purpose**: Broader than skills—enable Claude to connect with APIs, databases, file systems, third-party services.
- **How they work**: Implemented as MCP servers (standalone programs) that run separately.
- **Example**: A plugin could connect Claude to a weather API, database, or custom backend service.
- **Scope**: General-purpose and available in Claude Desktop and other MCP-compatible clients.

### Claude Tools (MCP Tool Methods)

**What they are**: The callable actions (operations/endpoints) exposed by a plugin, or the built-in helpers in Claude’s runtime, that can be invoked during a conversation.

- **Purpose**: Execute a discrete operation (search, translate, run command, fetch from DB) with structured input/output.
- **How they work**: Defined in plugin/MCP server metadata as tool definitions; Claude chooses a tool by name and passes arguments to it.
- **Example**: `get_weather`, `translate_text`, `run_code`, `fetch_config`.
- **Scope**: Used by any MCP-compatible client; in your repo, plugin methods can be thought of as tools available at runtime.

## Where Should You Start?

### Choose Skills If:
- You want to automate tasks **within your codebase** (testing, linting, deployment).
- You're primarily using **Claude Code** for development.
- You prefer a **simple, quick** setup with instructions.

### Choose Plugins If:
- You need to **integrate external APIs, databases, or services**.
- You want Claude to have **persistent access** to tools across different projects.
- You're comfortable with **coding an MCP server**.

---

## Project Structure

- `plugins/`: Implementation of modular extensions (Cache, Config, Logger).
- `skills/`: Implementation of utility functions (Math, Data, Text Processing).
- `.claude/skills/`: Custom skill definitions for Claude Code CLI.

---

## Resources

- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [Claude Code Documentation](https://docs.anthropic.com/claude/docs/claude-code)