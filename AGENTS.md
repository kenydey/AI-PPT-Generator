# AGENTS.md

## Cursor Cloud specific instructions

### Project overview
AI PPT Generator — 企业级 AI PPT 全自动生成系统。Two-service monorepo: Python FastAPI backend + React/Vite frontend. No database; presentation state is in-memory.

### Services

| Service | Port | Start command |
|---------|------|---------------|
| Backend (FastAPI) | 8000 | `uv run uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000` (from repo root) |
| Frontend (Vite)   | 6000 | `npm run dev` (from `frontend/`) |

The Vite dev server proxies `/api`, `/docs`, `/health`, `/openapi.json` to backend port 8000.

### Running commands

- **Backend deps**: `uv sync` (from repo root)
- **Frontend deps**: `npm install` (from `frontend/`)
- **TypeScript check**: `npx tsc -b` (from `frontend/`). Pre-existing TS6133 warnings exist in `Home.tsx` (unused variables).
- **Tests**: `uv run pytest` (from repo root). Currently no test files exist; pytest dev dependency is configured in `pyproject.toml`.
- **Build frontend**: `npm run build` (from `frontend/`)

### System dependencies

- `graphviz` system package is required — the Python `graphviz` library calls the `dot` binary for flowchart rendering.

### Environment variables

- `OPENAI_API_KEY` — **required** for AI outline generation (LiteLLM, supports OpenAI/Gemini/DeepSeek/Ollama)
- `TAVILY_API_KEY` — optional, web search augmentation
- `PEXELS_API_KEY` / `UNSPLASH_ACCESS_KEY` / `ICONFINDER_API_KEY` — optional, image/icon search
- `SEARXNG_HOST` — optional, self-hosted search fallback

### Gotchas

- The export API (`POST /api/export`) works without any API keys — useful for testing PPTX generation pipeline independently.
- Backend has no database — all presentation state is stored in a Python dict and lost on restart.
- `uv` must be on PATH (`$HOME/.local/bin`); it is installed via `curl -LsSf https://astral.sh/uv/install.sh | sh`.
