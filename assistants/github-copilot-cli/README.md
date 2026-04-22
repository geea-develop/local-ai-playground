# 🐙 GitHub Copilot CLI

> [!NOTE]
> **Status: 🚧 In Progress** — This directory is a placeholder for the GitHub Copilot CLI integration. Setup and usage notes will be added here.

[GitHub Copilot in the CLI](https://docs.github.com/en/copilot/github-copilot-in-the-cli) extends GitHub Copilot to the terminal. It provides AI-powered suggestions for shell commands, explains unfamiliar commands, and helps debug scripts — all directly in your terminal session.

---

## Planned Setup

1. **Install the GitHub CLI extension**:
   ```bash
   gh extension install github/gh-copilot
   ```

2. **Authenticate**:
   ```bash
   gh auth login
   ```

3. **Use Copilot in the CLI**:
   ```bash
   # Explain a command
   gh copilot explain "git rebase -i HEAD~3"

   # Suggest a command
   gh copilot suggest "undo the last git commit without losing changes"
   ```

---

## Key Subcommands

| Command | Description |
|---|---|
| `gh copilot explain <cmd>` | Explains what a shell command does |
| `gh copilot suggest <task>` | Suggests a shell command for a task |

---

## Planned Integration

- Document common shell command patterns used with this playground (e.g., Ollama management, Docker operations)
- Add shell aliases for frequent Copilot CLI patterns

---

## Resources

- [Official Documentation](https://docs.github.com/en/copilot/github-copilot-in-the-cli)
- [GitHub CLI Extensions](https://cli.github.com/manual/gh_extension)
