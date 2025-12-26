# Repository Guidelines

## Project Structure & Module Organization
- `src/` holds the core Python agents and shared utilities (`src/agents/`, `src/base/`, `src/a2a_integration/`, `src/mcp_config_module/`).
- `docs/` and `examples/` contain reference material and sample workflows.
- `docker/`, `docker-compose-full.yml`, and `1-run-docker.sh` manage the containerized stack.
- `a2a-inspector/` (UI/backend) and `mem0/` (OpenMemory MCP/UI) are standalone subprojects with their own tooling.

## Build, Test, and Development Commands
Use `uv` for dependency management (Python 3.12):
```bash
./setup.sh
uv sync --dev
export PYTHONPATH="${PWD}/src"
uv run python -m src.agents.supervisor
./1-run-docker.sh start
uv run ruff check src/
uv run ruff format src/
uv run pytest
```
`./1-run-docker.sh` handles full Docker orchestration; `docker compose -f docker-compose-full.yml up -d --build` is the direct alternative.

## Coding Style & Naming Conventions
- Python: 4-space indentation, 80-character lines, Google-style docstrings.
- Formatting and linting via Ruff (`.ruff.toml`); run `ruff format` before committing.
- Use type hints consistently and prefer async/await for I/O.
- Naming: modules and functions in `snake_case`, classes in `PascalCase`, agent modules under `src/agents/<agent_name>/`.
- No emojis in documentation, comments, or commit messages.

## Testing Guidelines
- `pytest` is configured in `pyproject.toml`; no global coverage threshold is defined.
- New tests should live under `tests/` with `test_*.py` or `*_test.py` names.
- Optional coverage run: `uv run pytest --cov=src tests/`.

## Commit & Pull Request Guidelines
- Recent commits mix `chore:`-style prefixes and plain summaries; follow the existing pattern for similar changes.
- Keep commits scoped and update `uv.lock` when dependencies change.
- PRs should include a short description, how to run or verify, and any required env vars or Docker services. Include UI screenshots for `a2a-inspector/frontend` changes.

## Security & Configuration
- Copy `.env.example` to `.env` and set API keys (OpenAI, Tavily, Serper, Notion). Do not commit secrets.

## Agent-Specific Instructions
- Follow `AGENT.md` and `CLAUDE.md`: reuse existing base classes and utilities, consult `docs/` before new patterns, and keep prompts centralized in `src/agents/prompts.py`.
