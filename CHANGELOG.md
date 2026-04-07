# Changelog

All notable changes to this project will be documented in this file.

## [v1.0.0] - 2024-10-05

- Initial release with Docker setup using Colima
- Added .gitignore and .gooseignore
- Added LICENSE (Apache 2.0)
- Added CHANGELOG.md
- Setup instructions for SSH remote and push

## [Docs] Add review signature to all READMEs

- Added audit trail line \"Reviewed by Goose 2026-04-07 16:05\" to the end of all `README.md` files across the project.
- Ensures consistent documentation review and traceability for future audits.
- Affected files:
  - `anything-llm/README.md`
  - `claude-lm-studio/README.md`
  - `claude_playground/README.md`
  - `goose/README.md`
  - `langchain_playground/README.md`
  - `llm_runner/README.md`
  - `local_ai_servers/README.md`
  - All nested `README.md` files under `local_ai_servers/` (e.g., `debug/`, `llama-cpp-server/`, etc.)

## 2026-04-07

### [Feature] Project Structure Migration

- Migrated project structure files to a centralized `.local` directory for memory and reference.
- Updated the project's README and changelog with a concise summary of the directory structure.
- Summary includes only file and folder counts by directory, excluding actual file names.

## Directory Structure Summary (Counts Only)

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
