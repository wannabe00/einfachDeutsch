# einfachDeutsch

A web app for learning German. Learners follow a guided path of short daily
lessons, review vocabulary with spaced-repetition flashcards, and practise with
drills, grammar notes, curated videos and short reads on German history.

**Stack:** Django 5 + Django REST Framework, React 19 + TypeScript + Vite,
Google Gemini for the AI features, SQLite locally and Neon Postgres in
production.

## Features

- **Learning path.** Levels are split into units (one per textbook Lektion) and
  each unit into 2-3 lessons (vocabulary, grammar, communication and review),
  with similar exercises grouped on one screen. A lesson can be left and
  resumed. Progress within a level is linear, and content above your level is
  never shown. A1 is complete.
- **Energy.** Free users have 3 energy, a new lesson costs 1, and it refills
  one every 4 hours. Redoing lessons, review and everything else is free.
- **Level exam.** Finishing a level's path unlocks an exam; passing it moves you
  up a level.
- **Spaced review.** SM-2 flashcards where you type the German, article
  included.
- **Word Bank and Grammar.** Grouped by level; topics and words unlock as you
  reach the lessons that teach them.
- **Drills.** Six short games (articles, spelling, word order and more).
- **Videos and History.** Curated watch suggestions and history reads with a
  quiz, filtered to your level.
- **Premium.** Unlimited energy, an AI tutor with saved conversations, and
  Recite: read a text, retell it aloud and get feedback. The audio is
  transcribed and then discarded. Payments aren't live yet, so premium is a
  flag set in the admin (plus a one-time 7-day trial).
- **Accounts.** Sign up with Google or GitHub, then set a username and
  password during onboarding. Guests can try parts of the app with a daily
  limit.

## Running locally

```bash
# Backend
cd backend
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env              # GEMINI_API_KEY is optional; the rest has dev defaults
python manage.py migrate
python manage.py seed_a1_path     # the A1 learning path
python manage.py create_dev_user  # a ready-to-use login, since OAuth rarely works on localhost
python manage.py runserver        # http://localhost:8000

# Frontend, in a second terminal
cd frontend
npm install
npm run dev                       # http://localhost:5173
```

`create_dev_user --superuser` also gives the account access to the Django admin
at http://localhost:8000/admin.

Google and GitHub sign-in need OAuth credentials in the environment:
`GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GITHUB_CLIENT_ID` and
`GITHUB_CLIENT_SECRET` for the backend, and `VITE_GOOGLE_CLIENT_ID` and
`VITE_GITHUB_CLIENT_ID` for the frontend.

## Checks

```bash
cd backend && ruff check . && ruff format --check . && python manage.py check
cd frontend && npx tsc --noEmit && npx eslint src && npm run build
```

## Deployment

The frontend is on Vercel (`frontend/vercel.json`), the backend on Render
(`render.yaml`) and the database on Neon. Settings come from environment
variables, all listed in `backend/.env.example` and `frontend/.env.example`.
Render runs migrations on every deploy.

## Project layout

| Path | Contents |
|---|---|
| `backend/apps/curriculum` | Units, lessons, energy, grading, the level exam |
| `backend/apps/vocabulary` | Words, SM-2 scheduling, review history |
| `backend/apps/accounts` | Profiles, placement test, streaks, premium |
| `backend/apps/ai_assistant` | Gemini calls and saved conversations |
| `frontend/src/pages` | One component per route |
| `frontend/src/components` | Shared UI, grouped by feature |

## License

Personal project, not licensed for redistribution. Lesson content is written
for this app; nothing is copied from the textbooks it follows.
