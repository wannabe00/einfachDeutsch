# German Learning Platform

A personal tool for learning German — built with Django (backend) and React + TypeScript (frontend). Spaced repetition flashcards, grammar reference, book exercises, and a Claude AI assistant.

Built as a learning project: learn German, learn Django, learn TypeScript — all at once.

---

## Quick start

```bash
# Clone
git clone <your-repo-url> german-platform
cd german-platform

# Backend
cd backend
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env           # fill in ANTHROPIC_API_KEY when you have it
python manage.py migrate
python manage.py seed_data     # loads sample book + chapter + words
python manage.py runserver     # http://localhost:8000

# Frontend (new terminal)
cd frontend
npm install
cp .env.example .env.local     # optional: set VITE_API_BASE_URL if not using default
npm run dev                    # http://localhost:5173
```

Open http://localhost:5173 in your browser. The Django admin is at http://localhost:8000/admin.

---

## Features

- **Review** — SRS flashcards: see the English word, type the German translation with the correct article (e.g. `der Hund`). Rated as Again / Hard / Good / Easy — schedules the next review automatically.
- **Word Bank** — Add vocabulary chapter by chapter as you work through your textbook. Bulk import via CSV.
- **Grammar** — Write grammar rules from your books (Markdown supported). Browse by chapter or category.
- **Exercises** — Add exercises from your books. Submit answers and see feedback.
- **AI Assistant** — Ask Claude to explain grammar, suggest vocabulary for a chapter, generate exercises, or just answer German questions.

---

## Tech stack

| Layer | Tech |
|---|---|
| Backend | Django 5 + Django REST Framework |
| Frontend | React 19 + TypeScript + Vite |
| Styling | Tailwind v3 + shadcn/ui |
| Database (dev) | SQLite |
| SRS algorithm | SM-2 (custom implementation) |
| AI | Claude (claude-sonnet-4) via Anthropic API |

---

## Project docs

| File | What it covers |
|---|---|
| `WORKFLOW.md` | How to drive the project day-to-day |
| `PROJECT_PLAN.md` | The full brick-by-brick build plan |
| `KNOWLEDGE_BASE.md` | Current state of what's built |
| `DESIGN.md` | UI design system, tokens, component rules |
| `CONTRIBUTING.md` | Git conventions, branching, how to add things |
| `AGENTS.md` | Rules for Claude sessions on this project |

---

## Environment variables

### `backend/.env`
```
SECRET_KEY=<django-secret-key>
DEBUG=True
ANTHROPIC_API_KEY=<your-key>       # needed for Phase 6+ (AI features)
```

### `frontend/.env.local`
```
VITE_API_BASE_URL=http://localhost:8000/api   # default if not set
```

---

## License

Personal project — not licensed for redistribution.
