# Workflow

How you and Claude work on this project together. Read this first, every session.

---

## The unit of work is a "brick"

Everything in `PROJECT_PLAN.md` is broken into small, independently verifiable bricks (e.g. `3.2`, `4.1`). One brick = one PR + one working thing you can test in the browser or with curl.

**The main command:** say `do the next brick` and Claude will:
1. Find the next unticked brick in `PROJECT_PLAN.md`
2. Read the relevant files to understand current state
3. Implement it end-to-end (backend + frontend if needed)
4. Verify it passes the "Done when" criteria
5. Tick the box in `PROJECT_PLAN.md` and update `KNOWLEDGE_BASE.md`

You can also say `do brick 3.4` to jump to a specific one, or `what's the next brick?` to check without doing anything.

---

## Reading order (new session or new context)

1. `AGENTS.md` — rules Claude must follow on this project
2. `KNOWLEDGE_BASE.md` — what's actually built right now
3. `PROJECT_PLAN.md` — what comes next (find the first unticked box)
4. `DESIGN.md` — before touching any UI

---

## Session rhythm

**Start of session:**
- Say `what's the current state?` → Claude reads `KNOWLEDGE_BASE.md` and summarizes where you are
- Or just say `do the next brick` and it will orient itself

**End of brick:**
- Claude ticks the brick in `PROJECT_PLAN.md`
- Claude updates the changelog in `KNOWLEDGE_BASE.md`
- You verify manually ("Done when" criteria)
- Commit and push

**If something is broken:**
- Say `the build is broken, here's the error: [paste]`
- Claude fixes it before moving to the next brick

---

## Providing content from your books

When you finish a chapter in your German textbook, open this project and say:

> "I finished Chapter [N] — here are the words: [paste list] / here are the grammar rules: [paste]"

Claude will add them to the correct API endpoint, or give you a quick command to run if it's bulk data.

You don't need to provide books upfront. Add content as you learn it.

---

## The two servers

Always run both during development:

```bash
# Terminal 1 — backend
cd backend
source venv/bin/activate
python manage.py runserver          # http://localhost:8000

# Terminal 2 — frontend
cd frontend
npm run dev                         # http://localhost:5173
```

The frontend proxies API calls to the backend. If the backend isn't running, the frontend will show loading/error states — that's expected.

---

## "Done" definition for a brick

A brick is done when all of the following are true:

1. The "Done when" criterion in `PROJECT_PLAN.md` is verified in the browser or with curl
2. `npx tsc --noEmit` passes (frontend)
3. `python manage.py check` passes (backend)
4. Both servers still start without errors
5. The brick's box is ticked in `PROJECT_PLAN.md`
6. `KNOWLEDGE_BASE.md` changelog is updated
