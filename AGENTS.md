# Project: German Learning Platform

A German vocabulary + grammar study app built with **Django 5 + DRF** (backend) and **React 19 + TypeScript + Vite** (frontend). SRS flashcards, spaced repetition via SM-2, grammar reference, book exercises, and a Gemini AI assistant. **Multi-user** with **social login (Google + GitHub)** — content is shared/global, progress is per-user. Deployed: frontend on Vercel, backend on Render, DB on Neon Postgres.

**New here? Read in this order:** `WORKFLOW.md` (how work is driven) → `KNOWLEDGE_BASE.md` (current state) → `PROJECT_PLAN.md` (brick-by-brick plan). The default way work happens: the user says **"do the next brick"**.

---

## Rules — always follow these

### General
- Work proceeds one **brick** at a time (one logical step from `PROJECT_PLAN.md`). Never bundle unrelated bricks.
- After every brick: tick the box in `PROJECT_PLAN.md`, update `KNOWLEDGE_BASE.md`.
- **Never break the running state.** Both `python manage.py runserver` and `npm run dev` must still work after every commit.
- **Lint before done:** frontend `npx eslint src` + `npx tsc --noEmit`; backend `venv_mac/bin/ruff check .` + `ruff format .`. All must pass.

### Spec v2 architecture decisions (locked — see PROJECT_PLAN.md "Spec v2")
- **Hosting:** frontend → Vercel, backend → Render (persistent service), DB → **Neon Postgres** (never Render's bundled Postgres — 30-day auto-expiry).
- **AI:** ALL LLM + speech (chat, grading, transcription) uses **Gemini** behind a swappable interface so a paid provider can drop in later. No hardcoded paid Whisper/Claude.
- **Multi-user:** content (Book/Chapter/Word/GrammarRule/Exercise) is **shared/global**; progress (WordProgress/ReviewLog/ExerciseAttempt + new per-user models) is **per-user**. Don't add per-user FKs to content models.
- **Auth:** account creation is **social-login only** (Google + GitHub OAuth via allauth + dj-rest-auth). Onboarding then sets username + password + name (`UserProfile.profile_complete` gate); username/password is a login fallback. **No email/phone verification.** OAuth client IDs/secrets come from env. SMTP is wired only for a future password-reset flow.
- **Copyright:** never reproduce the Menschen workbooks (or other non-public-domain books) verbatim — author original lesson-matched content instead.

### Backend (Django)
- DB/secrets stay in the backend only — never touch them from the frontend directly.
- Always register new apps in `INSTALLED_APPS` and wire their URLs in `config/urls.py`.
- Signals go in `apps.py` (`ready()` method) — never at module level.
- The SM-2 algorithm lives in `apps/vocabulary/srs.py` as pure Python — no third-party SRS library.
- Management commands for seeds/utilities go in `apps/<app>/management/commands/`.
- Money (if ever needed) is stored as integer cents.
- Run `python manage.py migrate` after every model change; commit migration files.
- Never hand-edit an already-applied migration.

### Frontend (React + TypeScript)
- All API calls go through `src/api/client.ts` (the Axios instance) — never use raw `fetch`.
- Server state is managed by **React Query** (`@tanstack/react-query`) — no manual `useState` + `useEffect` for data fetching.
- All TypeScript interfaces live in `src/types/index.ts` — keep them in sync with Django serializers.
- Never hardcode the site name — import from `src/lib/site.ts`.
- Never call the LLM API from the frontend — all AI calls go through the Django `/api/ai/` endpoints.
- `npx tsc --noEmit` must pass before any brick is done.

### AI integration
- **Provider: Google Gemini** (switched from Claude — the project uses a free Gemini key). Model `gemini-2.5-flash`.
- The `GEMINI_API_KEY` lives in `backend/.env` only (never frontend).
- All LLM calls are in `apps/ai_assistant/llm.py` — views call those functions, they don't build prompts inline.
- If the key is missing, functions raise `AIConfigError` and endpoints return a graceful **503**; the frontend degrades without crashing. Keep this contract.

### Design
- Follow `DESIGN.md` for every UI brick — tokens, components, article badge colors, SRS button colors.
- German nouns always display capitalized (der Hund, not der hund) — enforce in serializers and UI.
- Article badge colors are non-negotiable: **der = blue, die = rose, das = amber**.

### Secrets
- Real values only in `backend/.env` and `frontend/.env.local` (both git-ignored).
- Every variable is documented (no values) in `backend/.env.example` and `frontend/.env.example`.
- Never paste keys into code, commits, or chat.
