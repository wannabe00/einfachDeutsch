# Contributing

How you (and your AI assistant) work on this project without breaking things. This project has two sub-projects in one repo: `backend/` (Django) and `frontend/` (React + TypeScript).

## Before you start
1. Read `WORKFLOW.md` → `KNOWLEDGE_BASE.md` → `PROJECT_PLAN.md`.
2. `cd backend && source venv_mac/bin/activate && pip install -r requirements.txt`
3. `cd frontend && npm install`
4. Copy `backend/.env.example` → `backend/.env` and fill in any keys you have.
5. `python manage.py runserver` and `npm run dev` — both must boot before you change anything.

## The unit of work is a "brick"
One small step from `PROJECT_PLAN.md` per commit. Drive it with `do the next brick`. Don't bundle unrelated changes — a backend model change and a new frontend page are two different bricks even if they're related.

## Branching strategy
Trunk-based with short-lived branches. One brick per branch, merged back fast.

**The model**
- `main` is always green and runnable (both servers boot; no migration conflicts; TypeScript passes).
- Never commit directly to `main`.
- All work happens on short-lived feature branches — one brick per branch.
- Branches are temporary: open → implement → verify → merge → delete. Don't let a branch sit for days.

**Naming**
- `phase-<n>/<short-slug>` — e.g. `phase-3/srs-review-endpoint`, `phase-1/word-models`
- Quick fixes: `fix/<short-slug>` — e.g. `fix/article-badge-parse`
- Reference the brick number in the PR, not the branch name.

**Lifecycle of a brick**
1. `git switch main && git pull`
2. `git switch -c phase-<n>/<slug>`
3. Implement the brick
4. Pass the gate (see "Before pushing" below)
5. Push and open a PR into `main`
6. Verify it works (browser + curl)
7. Squash merge; delete the branch

**Staying in sync**
- Before starting a new brick: `git switch main && git pull`
- If `main` moves while you're working: `git fetch && git rebase origin/main`
- Collision-prone files: `backend/config/settings.py`, `backend/config/urls.py`, `frontend/src/types/index.ts`, `frontend/src/App.tsx` — be aware when two bricks touch these simultaneously.

**Merging**
- PR into `main` only. Prefer **squash merge** — one tidy commit per brick on main.
- Commit message style: `feat(vocabulary): brick 3.2 SM-2 algorithm + review endpoint`
- Don't merge a broken PR.

**Solo shortcut**
Working alone: you can commit directly to a working branch and merge to `main` yourself. Still use branches for risky changes (schema migrations, dependency bumps, new integrations) so you can test before merging.

## Commits
- Conventional style: `type(scope): summary` — e.g. `feat(grammar): brick 4.2 grammar page + card`
- Types: `feat`, `fix`, `chore`, `refactor`, `docs`, `style`, `test`
- Reference the brick number in the summary.
- Small, focused commits. Don't commit secrets or generated files (see `.gitignore`).

## Readability (keep code human-scannable)
- **Soft size caps:** page components ≤ ~150 lines (layout only), other components/functions ≤ ~120. Past that, extract logic into a **hook** (`src/hooks/useX.ts`) and/or split JSX into sub-components (co-locate related ones in a folder, e.g. `components/exercises/inputs/`).
- Backend view modules ≤ ~150 lines; group unrelated endpoints into a `views/` package by concern (see `apps/accounts/views/`), not one giant file.
- No dense one-liners doing three things; name intermediate values. A reviewer should scan a function top-to-bottom without decoding it.
- Delete dead code the moment a change orphans it (run `npx knip` / `vulture` before a cleanup PR).

## Before pushing / opening a PR
A brick is **done** only when:

1. `npm run build` + `npx eslint src` pass (frontend — `build` runs the real type-check; root `tsc --noEmit` checks nothing)
2. `ruff check .` + `python manage.py check` pass (backend)
3. Both `python manage.py runserver` and `npm run dev` boot without errors
4. The brick's "Done when" criteria is verified in the browser or with curl
5. The brick's box is ticked in `PROJECT_PLAN.md`
6. `KNOWLEDGE_BASE.md` changelog is updated (one line, newest at top)

## Database changes
- Edit `backend/apps/<app>/models.py`, then run `python manage.py makemigrations` and `python manage.py migrate`.
- **Always commit the migration files** alongside the model change.
- Never hand-edit an already-applied migration.
- If a migration causes issues on `main`, write a new corrective migration — don't edit the old one.
- Schema changes are the most collision-prone thing in this project. If two bricks both change models, do them sequentially, not in parallel.

## Adding a new Django app
If a new app is needed (unlikely after Phase 1 — all apps are planned):
1. `python manage.py startapp <name>` inside `backend/apps/`
2. Add to `INSTALLED_APPS` in `settings.py` as `'apps.<name>'`
3. Create `apps/<name>/urls.py` and include it in `config/urls.py`
4. Update `KNOWLEDGE_BASE.md` directory map

## Adding a new shadcn/ui component
```bash
cd frontend
npx shadcn@latest add <component-name>
```
Components are added to `frontend/src/components/ui/`. Don't modify them directly — wrap or extend them in `components/` instead.

## Secrets
- Django backend: `backend/.env` (git-ignored via `.gitignore`)
- React frontend: `frontend/.env.local` (git-ignored by Vite default)
- Every variable documented (no real values) in `backend/.env.example` and `frontend/.env.example`
- Never paste keys into code, commit messages, or chat

## Keeping docs honest
`KNOWLEDGE_BASE.md` = current reality. `PROJECT_PLAN.md` = future plan. Update them as part of the change — not later. They are how the assistant gets up to speed at the start of every session.
