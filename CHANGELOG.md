# Changelog

All notable changes to this project will be documented in this file.

## [2026-04-08] - local AI playground updates

- Initialized `smolagents` playground with a dedicated virtual environment and examples for MLX, llama.cpp, LM Studio, and Ollama.
- Setup `localai` directory with documentation and a Python example using the OpenAI SDK.
- Integrated `dotenv` across all new examples for consistent configuration.

## [2026-04-07] - Docs and Structure Migration

### Documentation
- Added audit trail line "Reviewed by Goose 2026-04-07 16:05" to the end of all `README.md` files across the project for consistent traceability.
- Affected directories include `anything-llm/`, `claude-lm-studio/`, `claude_playground/`, `goose/`, `langchain_playground/`, `llm_runner/`, `local_ai_servers/`, and `ollama_projects/`.

### Project Structure
- Migrated project structure files to a centralized `.local` directory.
- Updated the root README and changelog with a directory structure summary.

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

## [1.0.0] - 2024-10-05

- Initial release with Docker setup using Colima.
- Added infrastructure files: `.gitignore`, `.gooseignore`, `LICENSE` (Apache 2.0).
- Setup instructions for SSH remote and push.
