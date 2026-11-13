<!--
Guidance for AI coding agents working in the `anygen` repo.
Keep this file short (20-50 lines). Be concrete and reference real files/commands.
-->

# Copilot / AI agent instructions — anygen

Quick start
- Identify user request scope; follow `CLAUDE.md` quick-start steps (specs, plans, reviews) before coding.
- Choose protocol in `codev/protocols/` (SPIDER, SPIDER-SOLO, TICK) and obey its `protocol.md`.
- Sync with artefacts in `codev/specs/`, `codev/plans/`, `codev/reviews/`; document major shifts back into `CLAUDE.md`.

Workspace map
- Consult `README.md` and `VPN/README.md` for architecture and deployment; scripts and services live across `db/`, `GitLab/`, `telegram/`, `scripts/`.
- Prompts/env settings derive from `.env.example`; keep secrets out of Git and verify assumptions with repo search (`rg 'openai'`, `rg 'telegram'`).

Workflow essentials
- Use Python 3.11+ venv (`python -m venv .venv && source .venv/bin/activate`), then `pip install -r requirements.txt`.
- Run `pytest -q` before committing; validate infra configs (`caddy validate`, `docker-compose config`, `kubectl apply --dry-run=client`) when edited.
- Reuse helpers under `tests/` and follow SPIDER consultation checkpoints (Gemini 2.5 Pro + GPT-5) unless the user opts out.

Quality & security
- Apply `RECIPES.md` checklist: expressive names, <50-line functions, docstrings/type hints, input validation, robust error handling.
- Enforce DRY/KISS/SOLID: centralize config in `.env` or shared modules, prefer simple flows, split responsibilities cleanly.
- Secrets stay in `.env`; use ED25519 SSH, least-privilege access, and update `.env.example` + docs when adding env vars.

Collaboration
- Commits follow Russian Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`) and reference affected specs/plans.
- Keep edits minimal, add nearby tests, and align documentation/recipes when introducing new processes.
