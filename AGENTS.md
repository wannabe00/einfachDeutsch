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

### Spec v3 — Learning Path (locked 2026-07-15 — see PROJECT_PLAN.md "Phase 23")
The app is being rebuilt into a **Duolingo-style guided path**. These decisions are locked; build to them.
- **Structure:** Level (A1…C1) → **Unit** (theme) → **Lesson** ("day", ~6 mixed items: exercises + a drill + a few review cards). Progression is **strictly linear within the current level**; ahead is **locked + blurred**.
- **Level-gating (everywhere, consistent):** a user only sees content **≤ their level**. Below = optional review (fully unlocked), current = linear, future = fully locked. Applies to path, Word Bank, Grammar, Videos, History. **Never show forward-level content.**
- **Level-up:** completing (at/near 100%) a level's path unlocks a **Goethe-style checkpoint exam**; **pass → promote**, **fail → back to review**. Placement test sets the *starting* level only; no free skipping.
- **Energy:** free users start **3**, each **new** lesson costs 1, refill **+1 every ~4h (cap 3)**, spent **on completion** (quitting is free). Redoing lessons / Review / Word Bank / Grammar / Drills never cost energy. **Premium = unlimited energy.** Keep energy logic swappable/tunable via settings.
- **Tiers:** **Free** = full path (energy-limited) + Review + Word Bank + Grammar + Videos + History + Books. **Premium** = **unlimited energy + AI Assistant + AI explanations + Recite (speech)**. Price **$2.99/mo or ~$24/yr, 7-day trial**. Free users see AI/Recite **locked with upsell**. Until Stripe ships (last brick), premium is a **manual admin flag**; gate features on `is_premium`, never on a hardcoded user list.
- **Grading:** exercise grading is **deterministic/local** (not AI) so free users are graded. AI is only for chat/explanations/speech (all premium).
- **Content:** **pre-generated once, admin-approved**, shared/global (no per-user content). **Books = structure only** (owner provides A1 books); all stored items **authored original**. Grammar topics map to the **specific lessons that teach them** (grammar lives only on some chapters). MVP = **A1 only** first.
- **Coverage rule (locked 2026-07-15 — non-negotiable):** a level on the site must **contain everything the source books cover at that level**. For **A1** that means the full content of **Menschen A1.1 + A1.2, Kursbuch *and* Arbeitsbuch** — every Lektion's Wortschatz, Grammatik, and exercise types. Nothing from the books' level is left out. (Still authored original — the books supply structure/topics/wordlists/exercise *types*, never their text.)
- **Book→path mapping (locked):** **one Lektion = one `Unit`**; each Lektion is sliced into as many **~6-item day-sized `Lesson`s** as its Kursbuch+Arbeitsbuch content needs (a 4-page Lektion is far more than one day). **A1 = 24 Units** (A1.1 = Lektionen 1–12, A1.2 = Lektionen 13–24; each book = 4 Module × 3 Lektionen). Module grouping is *not* modelled — units carry the Lektion theme.
- **Data:** **additive** — new path/energy/premium/conversation models sit alongside existing SRS/streak/level models; **retire the thin Menschen seed** as real curriculum lands. Money stored as integer cents.
- **AI history:** ChatGPT-style per-user `Conversation` + `Message` models (resume/new/rename/delete, auto-titled). Premium-gated.
- **Visual:** friendlier **"dark + depth"** (gradients/glow/imagery, rounder cards, per-unit section colors) — see `DESIGN.md` → "Design v3". **Keep der/die/das color+shape + German-flag-red accent.** Gamification = **XP + per-lesson crowns + streak** (leagues later).

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
