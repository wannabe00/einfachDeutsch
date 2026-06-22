# German Learning Platform (einfachDeutsch)

A web app for learning German — SRS vocabulary flashcards, grammar reference, interactive exercises, drills, an AI tutor, and a "retell it in your own words" speaking exercise. Multi-user with CEFR leveling, a Mon/Wed/Fri lesson schedule, and practice streaks.

**Stack:** Django 5 + DRF (backend) · React 19 + TypeScript + Vite (frontend) · Google Gemini (AI) · SQLite (dev) / Postgres-Neon (prod).

---

## Project status

**Built & live (Phases 0–18 + landing page):**
- **Vocabulary + SRS** — SM-2 flashcards (type the German with its article), per-word performance tracking.
- **Word Bank** — chapters as a tile grid + word list (two-pane), add/import words (single, paste-list, CSV).
- **Grammar** — searchable topic-card gallery (Markdown rules).
- **Exercises** — 9 interactive types with server-side grading; **Drills** hub (6 games).
- **Dashboard** — stats, 7-day activity chart, streak banner.
- **AI Assistant** — chat, word/exercise generation, answer feedback (Google Gemini, account-only + rate-limited).
- **Recite (v2)** — read a text, retell it from memory; audio is transcribed (Gemini) and graded (coverage, grammar, pronunciation) then **discarded**.
- **Accounts & multi-user** — **Google/GitHub sign-in** (account creation is social-login only) + a username/password fallback set during onboarding; no email/phone verification. **Content shared / progress per-user**, freemium guest access with a daily cap + sign-up wall, server-side throttling.
- **CEFR leveling** — onboarding placement test (or quick-pick) with ±1 adjust; completion-gated progression engine.
- **Schedule + streaks** — Mon/Wed/Fri lesson unlock; streaks with auto-consumed freeze tokens.
- **Videos & shows** — curated German watch/listen suggestions tagged by level, unlocked at B1.
- **History track** — short German-history lessons (English+German through A2, German-only from B1) with a per-lesson quiz.
- **Landing page & account menu** — marketing landing page for guests; account dropdown with Settings (incl. level changer) and a public Privacy page.
- **Deployment** — Neon Postgres + Render (backend) + Vercel (frontend); WhiteNoise, gunicorn, env-driven prod config.

**Not yet built (see `PROJECT_PLAN.md`):**
- **UI polish pass (in progress)** — page-by-page visual upgrade using hand-copied 21st.dev components re-themed to our tokens (copied into the repo; no runtime dependency).
- **Phase 11** — more original per-lesson exercises, a "paste-your-own" exercise importer, voice conversation practice, extra drill/question variants.
- **Phase 19** — generic readers / `Passage` model with CEFR tagging.

---

## Quick start (local dev)

```bash
# Backend
cd backend
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # set GEMINI_API_KEY (optional); dev defaults work
python manage.py migrate
python manage.py seed_menschen  # loads the Menschen A1.1/A1.2 content
python manage.py createsuperuser
python manage.py runserver      # http://localhost:8000

# Frontend (new terminal)
cd frontend
npm install
npm run dev                     # http://localhost:5173
```

Open http://localhost:5173. Admin: http://localhost:8000/admin.

> **Sign-in:** accounts are created via **Google or GitHub** OAuth, then a username + password is set in onboarding (so username/password login also works). No email or phone verification. Configure OAuth client IDs/secrets via env (`GOOGLE_CLIENT_ID`/`GOOGLE_CLIENT_SECRET`, `GITHUB_CLIENT_ID`/`GITHUB_CLIENT_SECRET` on the backend; `VITE_GOOGLE_CLIENT_ID`/`VITE_GITHUB_CLIENT_ID` on the frontend). The existing superuser still logs in at `/admin`.

---

## Tech stack

| Layer | Tech |
|---|---|
| Backend | Django 5 + Django REST Framework |
| Frontend | React 19 + TypeScript + Vite + Tailwind v3 + shadcn/ui |
| Database | SQLite (dev) · Neon Postgres (prod, via `DATABASE_URL`) |
| SRS | SM-2 (custom, `apps/vocabulary/srs.py`) |
| AI / speech | Google Gemini (`gemini-2.5-flash`), behind swappable interfaces |
| Auth | django-allauth + dj-rest-auth, DRF token |
| Hosting | Vercel (frontend) · Render (backend) · Neon (DB) |

---

## Deployment

The repo is deploy-ready: `render.yaml` (backend blueprint), `frontend/vercel.json`, and env-driven settings (`ALLOWED_HOSTS`, `DATABASE_URL`, CORS/CSRF, SMTP, prod security). All variables are documented in `backend/.env.example`. Backend migrations run automatically on each Render deploy.

---

## Project docs

| File | What it covers |
|---|---|
| `PROJECT_PLAN.md` | Phase-by-phase build plan — what's done and what's left |
| `KNOWLEDGE_BASE.md` | Current state: features, API routes, directory map, changelog |
| `DESIGN.md` | UI design system, tokens, component rules |
| `AGENTS.md` / `CLAUDE.md` | Rules for AI coding sessions on this project |
| `WORKFLOW.md` | How work is driven ("do the next brick") |
| `CONTRIBUTING.md` | Git conventions |

---

## License

Personal project — not licensed for redistribution. Textbook content is author-original (not reproduced from copyrighted workbooks).
