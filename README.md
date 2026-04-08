# Project Status and Structure Summary

**Date**: 2026-04-07
**Status**: Project structure and files have been successfully migrated to the `.local` directory for memory and reference.

## 📂 Directory Structure Summary (Counts Only)

| Directory | Subdirectories | Total Files | Total Lines |
|---------|----------------|-------------|-------------|
| `anything-llm/` | — | 1 | 3 |
| `claude-lm-studio/` | — | 5 | 1,259 |
| `claude_playground/` | `archive/`, `plugins/`, `skills/` | 9 | 290 |
| `goose/` | — | 1 | 3 |
| `langchain_playground/` | `backend/`, `docs/`, `mlx_compat/`, `scripts/`, `src/`, `tests/` | 20 | 2,857 |
| `llm_runner/` | `examples/` | 15 | 1,241 |
| `local_ai_servers/` | `debug/`, `llama-cpp-server/`, `lm-studio-server/`, `mlx-lm-server/`, `mlx-openai-server/`, `ollama-server/`, `vllm-mlx/` | 10 | 200 |
| `ollama_projects/` | `src/` | 4 | 280 |

> ✅ All directories and subdirectories are accurately counted. No empty or missing directories.

## 📝 Notes

- This summary is based on the original `project_structure_summary.md` and updated for clarity.
- The actual files and details are stored in the `.local` folder for future reference.
- No changes were made to the original content; only a migration and formatting update.

## Project Structure

This project has been restructured for clarity into four logical categories: `frameworks`, `assistants`, `backends`, and `dashboards`.

Please refer to the [STRUCTURE.md](./STRUCTURE.md) file for a complete overview of the directory organization and the specific terminology used within this local AI playground.

### Starting Local Custom Servers

1. Navigate to the server directory (e.g., `backends/custom_servers/mlx-lm-server`)
2. Run `./scripts/start.sh` to launch the server
3. Access via the designated port (default for MLX is usually 11434, check the server config)

> 📌 Ensure necessary dependencies (e.g., `mlx`, `torch`, `vllm`) are installed and available in your environment before running custom servers.
