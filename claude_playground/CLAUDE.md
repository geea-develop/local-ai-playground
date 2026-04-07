# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

- Build: `make build`
- Lint: `flake8 src/`
- Run Tests: `pytest tests/ -v`
- Run Single Test: `pytest tests/test_example.py -v`

## Project Structure
- Main application logic in `src/main.py`
- Core utilities in `src/utils/`
- API endpoints in `src/api/`
- Tests in `tests/`
- Custom skills are located in `.claude/skills/`