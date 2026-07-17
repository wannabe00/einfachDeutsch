# German Learning Platform — Project Plan

Work proceeds one brick at a time. Say **"do the next brick"** to drive progress. Tick boxes as bricks complete. Full context: `KNOWLEDGE_BASE.md` (current state) and `DESIGN.md` (UI rules).

> **Status (2026-07-06):** Phases **0–18 done and live** in production (Vercel + Render + Neon). Auth is **social-login only** (Google + GitHub) + username/password fallback; the placement test is a 7-step AI-graded wizard. **Planned next (owner reviews docs, then implements brick-by-brick):** **Phase 20 — Hardening** (all findings in `AUDIT.md`: bugs, security, dead code, readability), **Phase 21 — Design v2 "Cinematic"** (image-led, spaceship.com-inspired; **landing page first**, spec in `DESIGN.md` v2 section), **Phase 22 — Content population** (curriculum A1.1 first — owner provides per-Lektion structure, original items authored to it; grammar library; videos/history; honest stats). Still open further out: Phase 11 leftovers, Phase 19 (readers), password-reset flow.
>
> **Big pivot (2026-07-15):** after the Phase 21 design work, the app is being rebuilt into a **Duolingo-style Learning Path** with energy limits, a free/premium tier, and strict level-gating — see **Phase 23** below (the major current effort) and the locked decisions in `AGENTS.md` → "Spec v3". Phase 23 supersedes most of Phase 22. Payments (Stripe) come last; MVP is **A1 only** first.

---

## Phase 0 — Scaffold & Config
Goal: Two servers running. Frontend can fetch from backend. Design tokens wired.

- [x] **0.1 Django project init**
  What: Create `backend/` directory, virtual environment, install dependencies, `startproject config`, create five apps: `books`, `vocabulary`, `grammar`, `exercises`, `ai_assistant`.
  Commands:
  ```bash
  mkdir backend && cd backend
  python -m venv venv && source venv/bin/activate
  pip install django djangorestframework django-cors-headers python-dotenv anthropic
  django-admin startproject config .
  python manage.py startapp books
  # ... repeat for all five apps
  ```
  Done when: `python manage.py runserver` starts at http://localhost:8000 with no errors; all five app directories exist under `backend/apps/`.
  Key files: `backend/manage.py`, `backend/config/settings.py`, `backend/apps/*/`

- [x] **0.2 DRF + CORS config**
  What: Add `rest_framework` and `corsheaders` to `INSTALLED_APPS`; configure `CORS_ALLOWED_ORIGINS` for `localhost:5173`; add `CorsMiddleware` as the first middleware; set `DEFAULT_PERMISSION_CLASSES` to `AllowAny` (no auth in v1); wire a `/api/` root URL.
  Done when: Visiting `http://localhost:8000/api/` in the browser shows the DRF browsable API root. A preflight request from `localhost:5173` is not blocked.
  Key files: `backend/config/settings.py`, `backend/config/urls.py`

- [x] **0.3 Vite + React + TypeScript init**
  What: Create the `frontend/` project. Install core dependencies.
  Commands:
  ```bash
  npm create vite@latest frontend -- --template react-ts
  cd frontend
  npm install axios @tanstack/react-query react-router-dom react-markdown
  ```
  Done when: `npm run dev` serves the app at http://localhost:5173; `npx tsc --noEmit` passes on the scaffold.
  Key files: `frontend/package.json`, `frontend/src/main.tsx`, `frontend/tsconfig.json`, `frontend/vite.config.ts`

- [x] **0.4 Tailwind CSS + shadcn/ui**
  What: Install Tailwind v3, configure `tailwind.config.ts` and `src/index.css`. Init shadcn/ui (choose `zinc` base, CSS variables on). Install first few components: `button`, `input`, `badge`, `card`, `separator`.
  Commands:
  ```bash
  npm install -D tailwindcss postcss autoprefixer
  npx tailwindcss init -p
  npx shadcn@latest init
  npx shadcn@latest add button input badge card separator
  ```
  Done when: A shadcn `Button` renders on the home page with correct Tailwind styling; dark mode class toggle works (add `dark` class to `<html>` and verify colors flip).
  Key files: `frontend/tailwind.config.ts`, `frontend/src/index.css`, `frontend/components.json`

- [x] **0.5 Design tokens + TypeScript types**
  What: Add all DESIGN.md color tokens as CSS custom properties in `src/index.css`. Add article badge colors (`--article-der`, `--article-die`, `--article-das`). Create `src/types/index.ts` with all TypeScript interfaces (Book, Chapter, Word, WordProgress, GrammarRule, Exercise, ExerciseAttempt, ReviewResult, AIResponse). Create `src/lib/site.ts` with `SITE_NAME`.
  Done when: `npx tsc --noEmit` passes; every interface is exported; swatching to dark mode in browser shows tokens applied correctly.
  Key files: `frontend/src/index.css`, `frontend/src/types/index.ts`, `frontend/src/lib/site.ts`

- [x] **0.6 Axios client + React Query + Router**
  What: Create `src/api/client.ts` (Axios instance pointing to `http://localhost:8000/api`, with `Content-Type: application/json`). Wrap `<App>` in `<QueryClientProvider>`. Set up `react-router-dom` with `<BrowserRouter>` and routes for all 7 pages: `/` (Dashboard), `/review` (Review), `/words` (Word Bank), `/grammar` (Grammar), `/exercises` (Exercises), `/books` (Books), `/ai` (AI Assistant). Each route renders a placeholder page component that just shows its name. Create `src/components/layout/Sidebar.tsx` with nav links to all pages.
  Done when: Navigating to each route in the browser renders the correct placeholder; the sidebar nav highlights the active route.
  Key files: `frontend/src/App.tsx`, `frontend/src/api/client.ts`, `frontend/src/main.tsx`, `frontend/src/components/layout/Sidebar.tsx`, `frontend/src/pages/*.tsx`

---

## Phase 1 — Data Layer
Goal: All Django models exist, are migrated, seeded with sample data, and browsable in admin.

- [x] **1.1 Book + Chapter models**
  What: Define `Book` (title, description, created_at) and `Chapter` (book FK, number, title, description) in `apps/books/models.py`. Generate and apply migration.
  Done when: `python manage.py migrate` runs with no errors; `python manage.py shell` → `from apps.books.models import Book` imports cleanly.
  Key files: `backend/apps/books/models.py`, `backend/apps/books/migrations/0001_initial.py`

- [x] **1.2 Word + WordProgress models**
  What: Define `Word` (chapter FK, english, german, notes, created_at) and `WordProgress` (OneToOne to Word, repetitions, ease_factor, interval, next_review, last_reviewed). Add a `post_save` signal in `apps/vocabulary/apps.py` (`ready()`) that auto-creates a `WordProgress` with defaults whenever a `Word` is saved for the first time.
  Done when: Creating a Word in Django shell auto-creates a linked WordProgress; `WordProgress.objects.get(word=my_word)` works without manual creation.
  Key files: `backend/apps/vocabulary/models.py`, `backend/apps/vocabulary/apps.py`

- [x] **1.3 Grammar + Exercise models**
  What: Define `GrammarRule` (chapter FK, title, category with choices, content, example_sentences). Define `Exercise` (chapter FK, exercise_type with choices, prompt, correct_answer, hint, explanation). Define `ExerciseAttempt` (exercise FK, user_answer, is_correct, ai_feedback, attempted_at). Apply migrations.
  Done when: `python manage.py migrate` runs; all three tables exist; `from apps.grammar.models import GrammarRule` and `from apps.exercises.models import Exercise` import cleanly.
  Key files: `backend/apps/grammar/models.py`, `backend/apps/exercises/models.py`

- [x] **1.4 DRF serializers**
  What: Create `ModelSerializer` for every model in `apps/*/serializers.py`. `WordSerializer` must nest `WordProgressSerializer` (read-only). `ExerciseSerializer` must exclude `correct_answer` from the default read representation (it is only returned by the attempt endpoint). All serializers must be importable with no errors.
  Done when: `python manage.py shell` → serialize a `Word` instance → JSON includes nested `progress` object with SM-2 fields.
  Key files: `backend/apps/*/serializers.py`

- [x] **1.5 Django admin**
  What: Register all models. Customize: `WordAdmin` shows list columns `english`, `german`, `chapter`; inline `WordProgressInline` (StackedInline) shows SM-2 state on the Word change page. `GrammarRuleAdmin` filter by chapter and category. `ExerciseAdmin` filter by chapter and exercise_type.
  Done when: http://localhost:8000/admin shows all models; can create a Book → Chapter → Word through the admin UI; Word change page shows the linked WordProgress inline.
  Key files: `backend/apps/*/admin.py`

- [x] **1.6 Seed data**
  What: Write a management command `python manage.py seed_data` that creates: 1 book ("Beginner German"), 2 chapters (Ch.1 "Greetings", Ch.2 "Numbers"), 5 words across both chapters, 2 grammar rules, 2 exercises. Idempotent — if a Book with that title already exists, skip creation (no duplicates on re-run).
  Done when: Running `python manage.py seed_data` twice produces no errors and no duplicate records; all seeded data is visible in admin.
  Key files: `backend/apps/books/management/commands/seed_data.py`

---

## Phase 2 — Books & Chapters
Goal: Books and chapters can be created and viewed via API and a frontend page.

- [x] **2.1 Books/Chapters DRF viewsets + URLs**
  What: `ModelViewSet` for `Book` (CRUD). Nested route for chapters: `GET/POST /api/books/{id}/chapters/`. Wire both to `/api/books/` in `config/urls.py`.
  Done when: `GET http://localhost:8000/api/books/` returns the seeded book as JSON with a `chapters` count or nested chapters. `POST /api/books/` creates a new book. `POST /api/books/1/chapters/` creates a chapter belonging to book 1.
  Key files: `backend/apps/books/views.py`, `backend/apps/books/urls.py`, `backend/config/urls.py`

- [x] **2.2 Books/Chapters frontend page**
  What: Page at `/books`. Fetches books with React Query. Shows each book as a card with its chapters listed inside. "Add Chapter" button per book opens an inline form (title, number). Form submits to `POST /api/books/{id}/chapters/`, invalidates the query on success. Follow `DESIGN.md` for card and button styling.
  Done when: Books and chapters from the API render on the page; adding a chapter via the form persists it and the list refreshes; no TypeScript errors.
  Key files: `frontend/src/pages/BooksPage.tsx`, `frontend/src/api/books.ts`

---

## Phase 3 — Vocabulary + SRS
Goal: Full spaced-repetition review loop works end-to-end.

- [x] **3.1 Vocabulary DRF viewsets + due-words endpoint**
  What: `ModelViewSet` for `Word` (CRUD). Filterable by `?chapter=<id>`. Custom action `GET /api/vocabulary/due/` returns words where `progress__next_review__lte=date.today()` ordered by `next_review ASC`.
  Done when: `GET /api/vocabulary/words/` returns all words; `GET /api/vocabulary/due/` returns only words due today (after seed, all 5 should appear); `?chapter=1` filter works.
  Key files: `backend/apps/vocabulary/views.py`, `backend/apps/vocabulary/urls.py`

- [x] **3.2 SM-2 algorithm + review endpoint**
  What: Implement SM-2 in `apps/vocabulary/srs.py` as a pure Python function `calculate_next_review(repetitions, ease_factor, interval, quality) -> (new_reps, new_ef, new_interval, next_review_date)`. Quality scale: 0=Again, 2=Hard, 4=Good, 5=Easy. Wire `POST /api/vocabulary/words/{id}/review/` to call it, save the updated `WordProgress`, and return the updated progress.
  Algorithm rules:
  - quality < 3 → reset: reps=0, interval=1
  - quality ≥ 3, reps=0 → interval=1; reps=1 → interval=6; reps>1 → interval=round(prev_interval × ef)
  - new_ef = ef + 0.1 − (5 − quality) × (0.08 + (5 − quality) × 0.02); clamp to ≥ 1.3
  Done when: POST `{"quality": 4}` twice to the same word shows interval growing from 1 → 6 → larger. POST `{"quality": 0}` resets it to interval=1 and reps=0.
  Key files: `backend/apps/vocabulary/srs.py`, updated `backend/apps/vocabulary/views.py`

- [x] **3.3 Word Bank page**
  What: Page at `/words`. Table of all words (english | german | chapter | next_review | interval). Chapter filter dropdown at the top. "Add Word" form (english, german, chapter select, optional notes). On submit, POST to `/api/vocabulary/words/`, invalidate query. Follow DESIGN.md: use ArticleBadge component to display the article part of `german` separately from the noun.
  Done when: All words display; chapter filter narrows list; adding a word persists it; ArticleBadge shows correct color (blue/rose/amber) based on article.
  Key files: `frontend/src/pages/WordBankPage.tsx`, `frontend/src/api/vocabulary.ts`, `frontend/src/components/vocabulary/ArticleBadge.tsx`

- [x] **3.4 FlashCard component + answer checking**
  What: `FlashCard.tsx` displays the English word, an input field, and a Submit button. On submit, check the answer client-side:
  - Correct: `normalize(input) === normalize(correct_answer)` (trim + lowercase)
  - Close: article matches exactly AND Levenshtein distance on the noun part is 1–2
  - Wrong: anything else
  Show feedback: green border + "Correct!" / yellow border + "Almost — check your spelling" / red border + "Wrong — the answer was [correct_answer]". Levenshtein helper in `src/lib/levenshtein.ts`.
  Done when: "der Hund" for prompt "dog" → correct. "die Hund" → wrong (article). "der Hundd" → close. Visual feedback matches description.
  Key files: `frontend/src/components/vocabulary/FlashCard.tsx`, `frontend/src/lib/levenshtein.ts`

- [x] **3.5 Review Session page**
  What: Page at `/review`. Fetch due words. Loop: show FlashCard → user submits → feedback shown → four quality buttons appear (Again / Hard / Good / Easy) → POST review → next card. After all cards: show session summary (X answered, Y correct, Z due again tomorrow). "Back to Dashboard" button. If no words due, show an empty state: "Nothing due — come back tomorrow or add more words."
  Done when: Full loop completes without errors. After rating a word "Good" and refreshing `/review`, that word no longer appears in the session. Summary shows correct counts.
  Key files: `frontend/src/pages/ReviewPage.tsx`, `frontend/src/hooks/useReviewSession.ts`

---

## Phase 4 — Grammar & Exercises
Goal: Content from your books can be entered, browsed, and practiced.

- [x] **4.1 Grammar DRF viewsets + URLs**
  What: `ModelViewSet` for `GrammarRule`. Filterable by `?chapter=<id>` and `?category=<value>`.
  Done when: `GET /api/grammar/rules/?chapter=1` returns only rules from chapter 1; `?category=articles` filters by category.
  Key files: `backend/apps/grammar/views.py`, `backend/apps/grammar/urls.py`

- [x] **4.2 Grammar frontend page**
  What: Page at `/grammar`. Chapter + category filter dropdowns. Each rule rendered as a GrammarCard (title, category badge, content rendered as Markdown via `react-markdown`, example sentences). "Add Grammar Rule" form (title, category, chapter, content textarea, examples textarea). Follow DESIGN.md GrammarCard styles.
  Done when: Grammar rules display with rendered Markdown; filters work; adding a new rule persists and appears immediately.
  Key files: `frontend/src/pages/GrammarPage.tsx`, `frontend/src/components/grammar/GrammarCard.tsx`, `frontend/src/api/grammar.ts`

- [x] **4.3 Exercises DRF viewsets + attempt endpoint**
  What: `ModelViewSet` for `Exercise` (note: `correct_answer` must NOT appear in the default list/retrieve response — only in the attempt response). Custom action `POST /api/exercises/{id}/attempt/` accepts `{"user_answer": "..."}`, saves an `ExerciseAttempt`, and returns `{is_correct, correct_answer, ai_feedback: ""}`.
  Done when: `GET /api/exercises/` does NOT include `correct_answer` in any result. POSTing a correct answer to the attempt endpoint returns `{"is_correct": true, "correct_answer": "..."}`. Wrong answer returns `{"is_correct": false, ...}`.
  Key files: `backend/apps/exercises/views.py`, `backend/apps/exercises/urls.py`

- [x] **4.4 Exercises frontend page**
  What: Page at `/exercises`. Chapter + type filter. Each exercise: prompt → text input → Submit. After submit: correct answer revealed, green/red result shown, attempt recorded. "Next" button moves to the next exercise. "Add Exercise" form (chapter, type, prompt, correct_answer, optional hint/explanation).
  Done when: Submitting a correct answer shows green + correct answer. Wrong answer shows red + correct answer. Can add exercises. Filter by chapter works.
  Key files: `frontend/src/pages/ExercisesPage.tsx`, `frontend/src/components/exercises/ExerciseCard.tsx`, `frontend/src/api/exercises.ts`

---

## Phase 5 — Dashboard
Goal: A real home page that shows your progress at a glance.

- [x] **5.1 Stats API endpoint**
  What: `GET /api/stats/` returns a JSON object:
  ```json
  {
    "due_today": 4,
    "learned_total": 2,
    "reviewed_today": 7,
    "total_words": 30,
    "total_grammar_rules": 12,
    "total_exercises": 8
  }
  ```
  "Learned" = words with `interval > 21`. "Reviewed today" = ExerciseAttempts + word reviews since midnight local time.
  Done when: Endpoint returns correct counts that match admin data.
  Key files: `backend/apps/vocabulary/views.py` (add a `StatsView`)

- [x] **5.2 Dashboard page**
  What: Replace the placeholder at `/`. Six StatCards (due today, total learned, reviewed today, total words, grammar rules, exercises). "Start Review" button — disabled with count badge 0 if `due_today === 0`, links to `/review` otherwise. Chapter list with word counts per chapter.
  Done when: Stats reflect real API data; "Start Review" is disabled when `due_today = 0` and enabled when words are due.
  Key files: `frontend/src/pages/Dashboard.tsx`, `frontend/src/components/ui/StatCard.tsx`

---

## Phase 6 — AI Integration
Goal: the LLM generates content suggestions and checks free-text exercise answers.

> **Note (current reality):** the provider was switched from Claude/Anthropic to **Google Gemini** (`gemini-2.5-flash`, free key). The client lives in `apps/ai_assistant/llm.py` (not `claude.py`) and reads `GEMINI_API_KEY`. The brick text below is the original plan, kept for history.

- [x] **6.1 Claude API client in Django**
  What: Add `anthropic` to requirements. Create `apps/ai_assistant/claude.py` with five functions: `suggest_words(chapter_title, chapter_description, count)`, `explain_grammar(topic)`, `generate_exercises(chapter_title, word_list)`, `check_exercise_answer(prompt, correct_answer, user_answer)`, `chat(message, history)`. Load `ANTHROPIC_API_KEY` from `.env`. All functions use `claude-sonnet-4-20250514`.
  Done when: Running `suggest_words("Greetings", "basic German phrases", 5)` in Django shell returns a text response from Claude.
  Key files: `backend/apps/ai_assistant/claude.py`, `backend/.env` (ANTHROPIC_API_KEY), `backend/.env.example`

- [x] **6.2 AI Django views + URLs**
  What: Five `POST` endpoints under `/api/ai/`:
  - `/api/ai/suggest-words/` → body: `{chapter_title, description, count}` → calls `suggest_words()`
  - `/api/ai/explain-grammar/` → body: `{topic}` → calls `explain_grammar()`
  - `/api/ai/generate-exercises/` → body: `{chapter_title, word_list}` → calls `generate_exercises()`
  - `/api/ai/check-answer/` → body: `{prompt, correct_answer, user_answer}` → calls `check_exercise_answer()`
  - `/api/ai/chat/` → body: `{message, history: [...]}` → calls `chat()`
  All return `{"content": "<Claude response text>"}`. Missing required fields return 400.
  Done when: POSTing to each endpoint via curl or Postman returns a Claude response.
  Key files: `backend/apps/ai_assistant/views.py`, `backend/apps/ai_assistant/urls.py`

- [x] **6.3 AI panel component**
  What: `AIPanel.tsx` — a slide-in panel from the right side (fixed position overlay, ~480px wide). Accepts `initialPrompt` prop. Shows a text area pre-filled with the prompt, a Submit button, and a response area. Loading state shows a spinner. "Dismiss" button closes it. Wire "AI Suggest" buttons on Word Bank (pre-fill: `"Suggest 10 vocabulary words for chapter: [chapter title]"`). Wire "Generate Exercises" on Exercises page.
  Done when: Clicking "AI Suggest" on a chapter in the Word Bank opens the panel with a pre-filled prompt; submitting shows Claude's response; closing the panel works.
  Key files: `frontend/src/components/ai/AIPanel.tsx`, `frontend/src/hooks/useAI.ts`, `frontend/src/api/ai.ts`

- [x] **6.4 AI Assistant chat page**
  What: Full-page chat interface at `/ai`. Conversation history stored in React state (resets on page refresh — no persistence needed). Suggested prompt chips shown on empty conversation: "Suggest words for greetings", "Explain the German case system", "When do I use 'doch'?". User input at the bottom (Enter to send). Each exchange calls `POST /api/ai/chat/` with the full history. Messages rendered in the chat area (user right-aligned, assistant left-aligned). AI feedback from `check_exercise_answer` is displayed below the answer reveal in `ExerciseCard.tsx` (call the endpoint automatically after each attempt).
  Done when: Multi-turn conversation works in the session. Clicking a chip pre-fills and sends. AI feedback appears on Exercises page after submitting an answer.
  Key files: `frontend/src/pages/AIAssistantPage.tsx`

---

## Phase 7 — Polish
Goal: Charts, bulk import, dark mode, ready to share.

- [x] **7.1 Progress charts**
  What: Install Recharts. Dashboard gets a `ReviewActivityChart` — a bar chart showing reviews per day for the last 7 days (requires a new `GET /api/stats/activity/` endpoint returning `[{date, count}]`). Word Bank gets a per-chapter progress summary: bar chart of words per interval bucket (new / 1–6 days / 7–21 days / learned >21 days).
  Done when: Charts render with real data; showing zero bars on days with no reviews (not crashing).
  Key files: `frontend/src/components/charts/ReviewActivityChart.tsx`, `frontend/src/components/charts/ChapterProgressChart.tsx`

- [x] **7.2 CSV bulk word import**
  What: Backend: `POST /api/vocabulary/import/` — accepts `multipart/form-data` with a CSV file and a `chapter_id` field. CSV columns: `english`, `german`, `notes` (optional). Bulk-creates words; skips rows where a Word with the same `english + chapter` already exists. Returns `{"created": N, "skipped": M}`. Frontend: "Import CSV" button on Word Bank opens a file input + chapter selector.
  Done when: Uploading a 10-row CSV creates 10 words. Uploading the same file again returns `{"created": 0, "skipped": 10}`.
  Key files: `backend/apps/vocabulary/views.py` (ImportView), `frontend/src/components/vocabulary/CSVImportButton.tsx`

- [x] **7.3 Dark/light mode toggle**
  What: Add a `ThemeToggle` button to the sidebar. Use a React context (`ThemeContext`) to manage the current theme. Store preference in `localStorage`. Toggle adds/removes the `dark` class on `<html>`. All DESIGN.md tokens already support dark mode — just verify every page looks correct.
  Done when: Toggling switches all pages; preference survives a page refresh; no tokens are hardcoded (they all flip correctly via the `dark:` prefix).
  Key files: `frontend/src/contexts/ThemeContext.tsx`, `frontend/src/components/layout/ThemeToggle.tsx`

---

## Post-plan work (added after Phases 0–7)
These were added in collaboration after the original plan finished. See `KNOWLEDGE_BASE.md` §10 (Roadmap) for full detail.

**Done since the plan:**
- Deep-editorial **dark-first redesign** (slate + indigo, DESIGN.md updated).
- Word Bank overhaul (chapter pills, pagination, overview stats, per-word performance tracking, paste-list importer).
- Interactive **exercise types** (multiple_choice, matching, sentence_order, word_bank) with server-side grading.
- **Drills** hub: Gender Triage, Blind Forge, Unscramble, Flash Recall, Sentence Shuffle, Match Pairs.
- Original **Lektion 1** exercise set (9 exercises, authored — not copied from the workbook).
- Collapsible sticky sidebar; clickable chapter detail pages.

## Phase 8 — Grammar navigation redesign ✅ DONE
- [x] **8.1 Topic-card gallery** — replaced the pill menus with cards grouped by Lektion + a live search box + a reading view (prev/next). No menus.

## Phase 9 — AI provider switch + chat ✅ DONE
- [x] **9.1 Provider → Gemini** — `apps/ai_assistant/llm.py` uses `google-genai` (`gemini-2.5-flash`) behind the existing `/api/ai/*` endpoints; `GEMINI_API_KEY` in `.env`; graceful 503 kept; AGENTS.md updated.
- [x] **9.2 Chat live** — AI Assistant chat works end-to-end on the user's free key.

## Phase 10 — Speak-to-AI v1 (Recite) ✅ DONE (superseded by Phase 16)
- [x] **10.1 Recite-a-text** — `/speak` page: paste text → study → speak (browser Web Speech API, de-DE) → word-diff highlight + short Gemini note. NOTE: Phase 16 below replaces this with the server-side "retell in your own words" pipeline.

## Phase 11 — Exercise content build-out (ONGOING)
- [x] **11.0 Original Lektion 1 set** (9 interactive exercises, authored).
- [ ] **11.1 Original per-lesson sets** across remaining lessons. NOT verbatim from copyrighted books.
- [ ] **11.2 "Paste-your-own" exercise importer** so the user can add specific exercises themselves.
- [ ] **11.3 Question-style variants** (matching variants; Odd One Out / Build the Question / Speed Gender drills); plus the decided-but-unbuilt **voice conversation practice** (voice in + voice out via browser TTS, gentle corrections).

---

# Spec v2 — the big build (decisions locked 2026-06-18)

> Source: the owner's feature spec. **Locked decisions:** transcription + grading use **Gemini** (free key, behind a swappable interface — NOT paid Whisper/Claude); **content is shared, progress is per-user** (teacher→student curation comes later); recitation **audio is discarded** after transcription; thresholds use the **recommended defaults** below. All tunable numbers live in Django settings, not hardcoded.
>
> **Recommended defaults:** video suggestions unlock after **A2** (at B1); history track shows English+German through **A2**, German-only from **B1**; video source = **hand-curated list** per CEFR level; streak = **2** freeze tokens, **+1 per 14-day** unbroken streak (capped), auto-consumed on a missed scheduled day.

## Phase 12 — Deployment foundation
- [x] **12.1 Postgres (Neon)** — `dj-database-url` + `psycopg[binary]`; `DATABASES` reads `DATABASE_URL` (ssl_require + conn_max_age) and falls back to local SQLite when unset. Deps in requirements.txt. **Use Neon, not Render's bundled Postgres.**
- [x] **12.2 Data migration path** — Neon provisioned; ran `migrate` + `seed_menschen` against it (559 words, 15 chapters, 18 grammar rules, 33 exercises loaded). Render deploys re-run `migrate` automatically.
- [x] **12.3 Prod config** — env-driven `ALLOWED_HOSTS`/`CORS_ALLOWED_ORIGINS`/`CSRF_TRUSTED_ORIGINS`; WhiteNoise (CompressedManifest static, `STATIC_ROOT`); `gunicorn`; SMTP email backend when `EMAIL_HOST` set (else console); prod hardening when `DEBUG=False` (SSL redirect, HSTS, secure cookies, proxy header). `render.yaml` (backend Blueprint) + `frontend/vercel.json` (Vite + SPA rewrite). `.env.example` documents all prod vars. Verified: collectstatic OK (154 files), wsgi imports, `check --deploy` clean except the dev SECRET_KEY (Render generates one).

## Phase 13 — Accounts & multi-user foundation (BIG — foundational)

> **Access model (decided 2026-06-19, owner):** the app is **freemium / guest-friendly**, not fully login-walled.
> - **Guest-OK** (free to the owner, read-only or cheap, server-rate-limited): Grammar, Exercises, Word Bank (browse), Review (limited, progress NOT saved), Books (browse). Guests are capped by a **daily action limit** (localStorage) → then a **sign-up wall**.
> - **Account-only** (costs the owner / abusable / speech): **Drills, AI Assistant, Recite (speak)**, plus anything that **writes per-user progress** or **edits content** (add/import words, add chapters, save SRS reviews).
> - **Anti-abuse:** server-side **DRF throttling** (`AnonRateThrottle`/`UserRateThrottle`) is the real DDoS/spam guard — the localStorage cap is just UX. Passwords are hashed (Django PBKDF2, via allauth) — security requirement satisfied.

- [x] **13.1 Auth** — `django-allauth` + `dj-rest-auth` + DRF token. **Now social-login-only:** account creation via **Google/GitHub** OAuth (code flow → token), then onboarding sets username + password + name (`profile_complete` flag, accounts migration 0007); username/password login as a fallback. No email/phone verification (`ACCOUNT_EMAIL_VERIFICATION=none`). `apps.accounts` + `UserProfile` auto-created via signal. Frontend: `AuthPage` (Google/GitHub buttons + username login), `OAuthCallbackPage`, `WelcomePage` (profile setup), `lib/oauth.ts`; token interceptor + 401 auto-logout; **guest-aware app shell**. _(Originally email/password; pivoted to social login to drop the verification requirement.)_
- [x] **13.2 Per-user data migration** — added nullable `user` FK to `WordProgress` (now FK not OneToOne, `unique_together(user, word)`, created on-demand), `ReviewLog`, `ExerciseAttempt`; content models stay global. Removed the auto-create-progress signal. Per-user queries: `due`/`due-counts` treat unseen words as new/due, `WordSerializer.progress` is the requesting user's row (prefetched) or null, `review` persists only for signed-in users (guests get computed-but-unsaved), Stats/Activity are per-user. Data migration assigns pre-existing single-user rows to the first user (owner) or drops them if no account exists. Per-action auth (content edits require login). **Verified:** A↔B isolation, guest non-persistence, owner's legacy 560 rows preserved.
- [x] **13.3 Endpoint protection + throttling** — `UserProfile` exposed via `/api/auth/user/` (13.1). Content writes auth-gated (13.2). AI endpoints now **account-only** (`IsAuthenticated`) + tighter per-user caps (`ai_burst` 12/min, `ai_daily` 120/day) to protect Gemini quota. Global `AnonRateThrottle` (120/min) + `UserRateThrottle` (600/min) as the spam/DDoS guard — all rates configurable via env. Drills/Recite are frontend-gated (no dedicated backend endpoints). **Verified:** guest AI→401, authed AI→200, 429 after burst. _(Flagged separately: wrap non-config AI errors in a clean 502 instead of raw 500.)_
- [x] **13.4 Guest limit + sign-up wall (frontend)** — `lib/guestLimit.ts` (daily action cap in localStorage, `GUEST_DAILY_ACTION_LIMIT`=20) + `GuestLimitContext` (`useGuestLimit().guard()` — signed-in unlimited; guests counted, opens `SignUpWall` modal when capped). Guards wired into ExerciseCard submit, ReviewPage rate, GenderTriage answer. **On-page blur lock:** account-only routes render `LockedFeature` (blurred content + "log in to use" overlay) instead of redirecting; sidebar lock badges removed. Gender Triage (der·die·das) opened to guests; other drills show a lock + LockedFeature. `ACCOUNT_ONLY_PATHS` = `/ai`,`/speak`; `/drills` hub now public. tsc+eslint clean (browser verify deferred per token budget).
- [x] **13.5 Forward-compat for teachers** — `UserProfile.role` (student/teacher, default student) + `level_set` flag added (accounts migration 0002); exposed via `/api/auth/user/` and in the frontend `User` type. Content already shared + progress already per-user, so a future Teacher↔Student link model + per-student curation layers on without reshaping tables.

## Phase 14 — CEFR leveling
- [x] **14.1 Models** — `LevelDefinition` (cefr/order/required_lessons/required_reviews, seeded A1–C2 via migration 0004) + `UserLessonProgress` (user, chapter, score, completed_at). Both in `apps.accounts`, admin-registered.
- [x] **14.2 Gating engine + onboarding** — `leveling.evaluate_level(user)` computes completion-gated `can_advance` (lessons + reviews vs the level's thresholds), exposed at `GET /api/accounts/level-status/`. Onboarding flow: authored locally-graded **placement test** (`/api/accounts/placement-test/`) + quick-pick + `POST /api/accounts/set-level/` (sets cefr_level + level_set); frontend `/onboarding` is forced after first login until a level is chosen, with ±1 adjust after the test. **Note:** the engine's `can_advance`/unlock signal is consumed by content-unlock UI in Phase 15 (Mon/Wed/Fri schedule).

## Phase 15 — Lesson schedule + streaks
- [x] **15.1 Mon/Wed/Fri unlock** — `scheduling.py` schedule primitives (`is_unlock_day`/`next_unlock_date`, `LESSON_UNLOCK_WEEKDAYS` configurable, default Mon/Wed/Fri); surfaced via `GET /api/accounts/streak/` + the dashboard banner ("New lesson available today" / "Next new lesson: <day>"). Reviews remain available any day. **Note:** schedule is surfaced + drives streak logic; hard per-lesson content-locking (blocking access to a not-yet-unlocked chapter) is deferred to the unlock UI in Phases 17/18.
- [x] **15.2 Streaks + freeze tokens** — `StreakRecord` (current/longest streak, freeze_tokens_available, last_active_date); `register_activity()` increments on each review/exercise (best-effort), auto-consumes a freeze per missed **scheduled** day and only resets when freezes run out; earns +1 freeze per `STREAK_FREEZE_EARN_DAYS` (14, capped `STREAK_FREEZE_MAX`=5); 2 initial tokens — all in settings. Verified with controlled dates + live review.

## Phase 16 — Recitation v2 (retell in your own words) — replaces Phase 10
- [x] **16.1 Record + upload** — `RecitePage` records via MediaRecorder (max-duration auto-stop), POSTs the blob as multipart to `/api/recitation/attempt/`. Audio is read in-memory and **never stored** (only transcript + grading saved on `RecitationAttempt`). `/speak` route now points here (old SpeakPage retired).
- [x] **16.2 Transcribe (Gemini)** — `apps/recitation/transcribe.py`: `Transcriber` ABC + `GeminiTranscriber` (multimodal `Part.from_bytes`) + `get_transcriber()` factory — swap for paid Whisper/Azure without caller changes.
- [x] **16.3 Grade (Gemini)** — `grading.py` `grade_retelling(source, transcript)` → JSON (`response_mime_type=application/json`): coverage_score, covered, missed, grammar_errors (typed: article/case/verb/word_order), summary; meaning-based (own words OK).
- [x] **16.4 Pronunciation (proxy)** — Gemini flags likely mis-said words from odd transcription → `pronunciation_notes` (same swappable interface).
- [x] **16.5 Cost control** — `RECITATION_DAILY_CAP` (5), `RECITATION_MAX_AUDIO_SECONDS` (120, client-enforced), `RECITATION_MAX_AUDIO_MB` (10, server-enforced) — all settings/env; AI throttles applied; account-only.
- [x] **16.6 Feedback card** — RecitePage shows coverage %, covered ✅ / missed, grammar corrections (strike→fix + type), pronunciation notes, summary, and a collapsible transcript. _(Note: real-audio transcribe/grade path needs a mic + live Gemini to exercise; guard paths — auth 401, validation 400, cap 429 — verified.)_

## Phase 17 — Video / show suggestions
- [x] **17.1 Unlock** — `GET /api/accounts/../videos/` (`apps.videos`) gates on `VIDEO_UNLOCK_MIN_LEVEL` (default **B1**, env-configurable); returns entries at/below the user's level. Below the threshold the page shows a friendly "unlocks at B1" panel; guests get the login wall (account-only). Verified A1→locked, B1→A1–B1 entries, guest→401.
- [x] **17.2 Curated source** — `ShowSuggestion` model (title, description, url, platform, cefr_level), admin-editable; seeded with 14 real hand-curated resources (DW/Easy German/ZDF/ARD/Netflix/YouTube) across A1–C1 via migration 0002. No external API. Frontend `VideosPage` groups by level with cards (platform badge, external link) + sidebar "Videos" entry.

## Phase 18 — German history track
- [x] **18.1 Always-available track** — `apps.history`: `HistoryLesson` (title, era, order, body_en, body_de, quiz JSON) + `UserHistoryProgress`. `HistoryLessonViewSet` (ReadOnly + `complete` action) at `/api/history/`, account-only; list/detail strip quiz answers, `complete` grades server-side + marks done. No schedule gating. Frontend `HistoryPage` (era-grouped list → lesson + per-lesson MC quiz with reveal). Seeded 6 authored lessons (HRE → Reformation → 1871 → Weimar → division/Wall → reunification).
- [x] **18.2 Language progression** — each lesson stores `body_en` + `body_de`; the page shows German always and English alongside **through A2**, German-only from **B1** (driven by the user's `cefr_level`).

## Phase 19 — Generic book/reading content
- [ ] **19.1 Generic model** — `Book` (exists) + `Chapter` (exists) + new `Passage` with **CEFR-level tagging**, so public-domain / licensed / self-written readers slot in without schema change.
- [ ] **19.2 Licensing gate** — flag: confirm usage rights before publishing any non-public-domain book. Source/content deferred (owner provides later).

## Post-18 — Landing page + UI polish (ongoing)
- [x] **Landing page** — marketing `/` for guests (Munich parallax hero, value props, how-it-works, der/die/das teaser, feature showcase, CEFR path, culture hook, stats, FAQ + CTA + footer); signed-in users get the dashboard at `/`.
- [x] **Account menu + pages** — Facebook-style dropdown in the sidebar footer; `SettingsPage` (account + level changer + theme) and a public standalone `PrivacyPage`.
- [ ] ~~**UI polish pass (page-by-page)**~~ — superseded by **Phase 21 (Design v2)** below; individual 21st.dev component grabs may still happen inside Phase 21 bricks.

## Remaining open items (decide during build)
- Exact CEFR threshold tuning for video unlock + history language switch (defaults set; revisit once real progression speed is seen).
- Whether to ever store recitation audio for "listen back" (currently discarded → would need Cloudflare R2/S3).
- Source/licensing of "other books" content (owner to provide).
- **Auth = social login (Google + GitHub) only.** Account creation is OAuth-only; after first sign-in the user completes onboarding (username + password + name; birthday optional) and can then log in with either provider or username + password. **No email verification** (Google/GitHub already verify the email). Email/password registration was removed. OAuth credentials via env (`GOOGLE_CLIENT_*`, `GITHUB_CLIENT_*` backend; `VITE_*_CLIENT_ID` frontend). Live-site callback URLs only for now.
- **Email (SMTP) is now optional** — wired (dj-rest-auth password endpoints + `EMAIL_*` env) but unused until the password-reset flow below ships.
- [ ] **Password reset / forgot password (planned).** Backend endpoints exist via `dj_rest_auth.urls` (`/api/auth/password/reset/` + `/confirm/`). To finish: point the reset email link at the SPA (custom adapter or `PasswordResetSerializer` URL), add a "Forgot password?" link on the login page + a `/reset-password/:uid/:token` page that POSTs the new password, and configure a real SMTP sender. No new models needed.

---

## Phase 20 — Hardening (from `AUDIT.md`, 2026-07-06)
Goal: every audit finding fixed. The canonical list with details/severities/file refs lives in **`AUDIT.md`** — tick both places. Suggested order: security first, then bugs, then dead code + readability.

- [x] **20.1 Critical security** — S1 `complete_onboarding` locked after first run; S2 password required server-side for delete / reset-progress / deactivate (+ Settings UI collects it). ⚠️ **S5 (rotate Neon/Brevo/Gemini/Cloudinary keys) is an OWNER ops task — still pending in the dashboards.**
- [x] **20.2 Abuse hardening** — S3 scoped login throttle; S4 avatar size/type validation; S7 preferences key whitelist + size cap; S9 phone validation.
- [x] **20.3 Bug fixes** — B1 recitation multipart boundary (audio upload broken); B2 danger-zone error swallowing; B4 placement timer pause.
- [x] **20.4 Token/session hardening** — S6: pick and implement token expiry/rotation strategy (also unblocks Settings v2 "active sessions"); S8 frontend security headers in `vercel.json`.
- [x] **20.5 Dead code + readability** — D1 knip/vulture sweep; R1–R5 splits (ExerciseCard, ReviewPage, InteractiveInputs, HistoryPage, accounts/views.py); R6 size convention into CONTRIBUTING.md. (D2/B3 Menschen removal waits for Phase 22 content.)

## Phase 21 — Design v2 "Cinematic" (spec: `DESIGN.md` → Design v2 section)
Goal: a premium, **image-led cinematic** look adapted from spaceship.com's structure/motion, fused with our der/die/das identity. **Landing/marketing page FIRST**; extend to in-app pages only after owner review. Accent = German-flag inspired (red/gold) for now, swappable to der-blue. Owner's #1 priority: big Berlin/Munich photography. (Supersedes the earlier Bauhaus draft; the reverted 21.1-foundation branch is gone.)

- [x] **21.1 Landing redesign** — cinematic full-bleed Berlin/Munich hero (parallax + dark overlay), scroll-reveal "moments" (IntersectionObserver fade-up, respect reduced-motion), photo band between sections, keep the der/die/das interactive tester, pill CTAs, transparent-to-solid top bar on scroll. Self-hosted Space Grotesk via `@fontsource` (NOT Google Fonts — prod CSP blocks it). German-flag accent added as a swappable `--brand` token. eslint + build clean.
**Owner decisions for the in-app extension (locked 2026-07-14):** the whole app goes **dark-only cinematic** (drop the light/dark toggle); **imagery in-app stays minimal/functional** (no marketing photography — dark surfaces + brand accent + subtle glow only); **navigation** keeps today's nav items but is restyled to a **spaceship-style top bar on desktop** (the left rail is retired on desktop) and a **better collapsible left drawer on mobile** — both collapsible; **build order starts with Settings + Profile**, everything else documented below for later. Design details live in `DESIGN.md` → "Design v2 — Cinematic" → in-app section.

- [x] **21.2 Dark-only foundation** — `ThemeProvider` now just pins `dark` on `<html>` (removed the toggle + its localStorage light path + `useTheme`); deleted `ThemeToggle` + dropped its Settings usage; `.dark` tokens rebuilt to the near-black cinematic canvas with `--primary`/`--accent`/`--ring` mapped to the `--brand` red; Space Grotesk applied to `h1–h4` globally; body glow switched to `--brand`. der/die/das colours unchanged. tsc + eslint + build clean.
- [x] **21.3 Navigation shell** — retired the left rail. New `TopBar`: spaceship-style top bar with logo, standalone Dashboard + AI Assistant links, and grouped dropdown menus (Practice / Library / Explore) that open on hover+click, close on outside-click/route-change, and highlight the active group. New `MobileNav` collapsible left drawer (grouped, backdrop, closes on tap) driven by a hamburger in the bar. Shared `navItems.ts` config feeds both. `Layout` drops `Sidebar`, main spans full width. Active states use the brand accent. tsc + eslint + build clean.
- [x] **21.4 Settings v2** — rebuilt `SettingsPage` in the dark cinematic language: spaceship-style **vertical tab rail** (desktop, sticky) that becomes a **horizontal scrolling tab strip** on mobile, with a single panel showing the active section. Tabs: Profile / Security / Preferences / Data / Danger zone (the last tinted with the danger token). The existing section components drop in unchanged and adopt the dark palette via tokens; only the active tab mounts. tsc + eslint + build clean. **Deferred (owner's call — own later brick):** the **active-sessions** list (needs a new backend list/revoke-tokens endpoint) and any richer new preference rows.
- [ ] **21.5 Profile v2** — the account/profile surface in the new language (identity header, avatar, stats), consistent with Settings v2.
- [ ] **21.6 Dashboard v2** — restyle `Dashboard` (cards, stats, next-actions) dark cinematic + brand accent.
- [ ] **21.7 Study surfaces v2** — restyle each study page to the system, in groups (each its own branch). Progress:
  - [x] **Core group (branch `redesign/study-core`)** — Review, Word Bank, Grammar. All three were already fully tokenized (adopt the dark palette automatically); the cohesion pass added a shared `components/layout/PageHeader` (bold Space Grotesk title + subtitle + actions) used across them, and aligned card hovers to the brand accent (`hover:border-primary/50`, dropped dead light-mode shadows). tsc + eslint + build clean.
  - [ ] Exercises · Drills · Recite (practice group)
  - [ ] Videos · History · Books (content group)
  - [ ] AI Assistant
- [ ] **21.8 Auth pages v2** — `AuthPage`/`OnboardingPage`/`WelcomePage` aligned to the cinematic language (they bridge the landing and the app).

## Phase 22 — Content population
Goal: the site is actually full of level-tagged learning material. Copyright rule stands: books provide **facts/structure only** (topics, grammar points, type/count of exercises, wordlists); every stored item is authored original.

- [ ] **22.1 Curriculum A1.1 (blocked on owner)** — owner supplies the per-Lektion structure (grammar points, exercise types + counts, Wortliste); original items are authored to exactly that spec and loaded via an idempotent seed command into local + Neon (= production). Then A1.2 → C1.2 the same way, level by level. Replaces the thin "Menschen" seed books (AUDIT B3/D2).
- [ ] **22.2 Grammar reference library** — standalone, level-tagged grammar section covering the full A1–B1 topic canon (tables + examples, original text), browsable independent of lesson progress.
- [ ] **22.3 Videos + History expansion** — grow curated video suggestions per level; add more original German-history lessons (each with quiz).
- [x] **22.4 Honest numbers** — DONE. Investigation first: there were **no hardcoded marketing figures left** — the cinematic landing (21.1) had already dropped the old stats section, and the Dashboard already reads real per-user stats. So this fulfilled the *intent*: new **`GET /api/stats/public/`** (`PublicStatsView`, AllowAny, 15-min cache) returns live COUNT(*) of curated content (words 587 / exercises 60 / grammar 21 / history 6 / videos 14 — can never over-claim), and the landing gained a **"Real content, today"** stats moment showing four of them. Degrades gracefully (renders nothing if the API is cold/down, so no row of zeros). tsc + eslint + build + ruff + check clean.

> **Note:** Phase 23 (below) supersedes/absorbs most of Phase 22 — the curriculum seed becomes the path content pipeline (23.3), the grammar library becomes gated Grammar (23.10), videos/history expansion happens in 23.11/23.12. Finish the remaining Phase 21.7 page-cohesion branches (merge them), then pivot to Phase 23; the leftover 21.7 pages are redesigned inside Phase 23 anyway.

## Phase 23 — Learning Path (Duolingo model) — the big pivot
Goal: turn the app into a **Duolingo-style guided path** with **energy limits**, a **free/premium tier**, and **strict level-gating**, wrapped in a friendlier **"dark + depth"** visual system. Owner-locked decisions live in `AGENTS.md` → "Spec v3" and the visual spec in `DESIGN.md` → "Design v3". Built brick-by-brick; **Stripe payments come last** (premium is a manual admin flag until then). MVP scope = **A1 only** first, then expand level by level.

**Locked model (2026-07-15, owner Q&A):**
- **Hierarchy:** Level (A1…C1) → **Unit** (theme) → **Lesson** ("day"). A lesson bundles **~6 mixed items** (exercises + a drill + a few review cards). Progression is **strictly linear within your current level** (finish lesson N to unlock N+1; ahead is locked + blurred).
- **Level-up:** finish (at/near 100%) your level's path → unlock a **Goethe-style checkpoint exam**; **pass → promoted**, **fail → sent back to review** and retry. Placement test still sets the *starting* level; no free level-skipping.
- **Level-gating everywhere (consistent):** you only ever see content **≤ your level** (below = optional review, fully unlocked; current = linear; future = locked). Applies to path, Word Bank, Grammar, Videos, History.
- **Energy (free users):** start **3**, each **new** lesson costs 1, refill **+1 every ~4h (cap 3)**. Spent **on completion** (quitting is free). Redoing lessons, Review, Word Bank, Grammar, Drills are **always free**. **Premium = unlimited energy.**
- **Tiers:** Free = full path (energy-limited) + Review + Word Bank + Grammar + Videos + History + Books. **Premium ($2.99/mo or ~$24/yr, 7-day trial) = unlimited energy + AI Assistant + AI explanations + Recite (speech).** Free users see AI/Recite **locked with an upsell**.
- **Content:** **pre-generated once, admin-approved**, shared (cheap). **Books = structure only** (owner provides **A1 books**); all stored items **authored original**. Grammar topics map to the **specific lessons that teach them** (grammar only lives on some book chapters), unlocking with that lesson.
- **Gamification:** **XP + per-lesson crowns + streak** (leagues/leaderboards later, not now).
- **Data:** **additive** — new path/energy/premium/conversation models alongside existing SRS/streak/level models; **retire the thin Menschen seed**.

Bricks (dependency order):
- [x] **23.1 Data model foundation** — DONE. `apps/curriculum` (Unit/Lesson/LessonItem + PathLessonProgress + EnergyState), premium fields on `UserProfile`, gating.py + energy.py helpers, admin, migrations. (Checkbox was stale after the branch reconcile — the code shipped long ago; see the 23.1 changelog entry.)
- [x] **23.2 Visual system "dark + depth"** — DONE. Design v3 tokens (`--surface-2` + 6 section accents) + `SectionCard`/`LockOverlay`/`PathNode`/`NextUp`/`EnergyMeter` + `/ui-kit`. (Checkbox was stale after the reconcile; shipped.)
- [x] **23.3 Content pipeline + A1 seed (first slice)** — DONE. Owner supplied the A1 books (**Menschen A1.1/A1.2**); structure read via `pdftotext` (12 Lektionen in 4 Modules). `apps/curriculum/a1_curriculum.py` holds **original authored** content for **Module 1** (L1 greetings, L2 family & languages, L3 free time) — books gave themes/structure only, no text copied. `manage.py seed_a1_path` builds Book → Chapter/Unit → Words/Grammar/Exercises → Lessons → LessonItems, **idempotent** (`update_or_create`; verified over two runs → no duplicates). Seeded: **3 units / 6 lessons / 30 items / 27 words / 18 exercises / 3 grammar**. Exercise types all deterministically gradable (multiple_choice, translation, fill_blank, article, conjugation, sentence_order). Gating verified end-to-end against real content (A1 user: L1 open → L2 locked → completes L1 → L2 opens, U2 still locked). ruff + check clean.
  - [ ] **23.3b Full A1 coverage (Lektionen 4–24)** — the **coverage rule** (`AGENTS.md` → Spec v3) requires A1 to contain **everything Menschen A1.1 + A1.2 (Kursbuch *and* Arbeitsbuch) cover at A1**: every Lektion's Wortschatz, Grammatik, and exercise types — authored original. **Mapping (locked): 1 Lektion = 1 Unit**, sliced into as many ~6-item day Lessons as its content needs. **A1 = 24 Units** (A1.1 = L1–12, A1.2 = L13–24). **Done: L1–3 (now at full depth). Remaining: L4–24 (21 Lektionen).** Author in chunks (a module = 3 Lektionen per brick) into `a1_curriculum.py`; `seed_a1_path` needs no changes (idempotent, data-driven). Per Lektion, mine the Kursbuch for theme/grammar/Redemittel and the Arbeitsbuch for exercise types/counts + the Wortliste.
    - [x] **23.3b-M1 Deepen Module 1 (L1–3) to real book depth** — DONE. The first-slice Module 1 was too thin (27 words / 3 grammar / 18 exercises). Rewrote `a1_curriculum.py` L1–3 to match a real Menschen Lektion: now **3 units / 12 lessons / 72 items / 78 words / 6 grammar (2 per Lektion) / 46 exercises** across all 6 renderable types (MC 12, fill_blank 9, translation 7, sentence_order 7, conjugation 6, article 5). **This is the density template for L4–24.** Limited to the six exercise types the lesson player actually renders (`word_bank`/`matching` grade server-side but have no input UI). `seed_a1_path` gained **prune passes** (stale LessonItems past a shrunk lesson's end; orphaned `seed-a1-` exercises; renamed seed grammar rules — scoped to the seed book so legacy Menschen grammar is untouched) so re-seeding after content edits leaves no ghosts. **Verified:** all 46 exercises round-trip through the real `grade()` (46 ok / 0 bad); every review/grammar ref resolves; MC answers ∈ options; sentence_order tokens are permutations of the answer; exam pool = 46 (≥ 12); re-run idempotent (pruned 0). ruff + format + check clean.
- [x] **23.4 Path page** — DONE. **Backend:** `GET /api/curriculum/path/` (IsAuthenticated) returns level, energy (current/max/premium/seconds_until_next), `next_up`, and units ≤ the user's level with each lesson's `state` (completed/current/available/locked) + crown; `gating.path_states()` computes all states in **one bulk pass** (the per-lesson `is_lesson_unlocked` would be N queries). Forward-level units are never serialized at all. **Frontend:** `PathPage` at `/path` (RequireAuth) — unit sections as accented `SectionCard`s with a **winding column of `PathNode`s**, `NextUp` banner, `EnergyMeter` in the header; "Path" added as a top-level nav item (top bar + mobile drawer). **Verified:** API tested as an A1 user (L1 current, rest locked), after completing L1 → L1 completed+crown, L2 current, `next_up` advances, later units still locked; guest → 401. tsc + eslint + build + ruff + check clean.
  - [x] **23.4b Unit page + swirly trail (owner restructure)** — DONE. Owner's call: the path overview shows **only the stacked, clickable unit containers** (no trail squeezed between them); each opens a **unit page** (`/path/:unitId`) with the **winding road on the left** and a **review panel on the right** (that Lektion's grammar + full Wortschatz) so the page isn't bare. New `GET /api/curriculum/units/<id>/` (level-gated; refuses above-level units). New **`Unit.chapter` FK** (migration `0002_unit_chapter`) formalising *1 Lektion = 1 Unit = 1 Chapter*, so the panel shows the **whole** Lektion's vocab (9) instead of only the 3 words its lessons reference. New `LessonTrail` — nodes placed on a **sampled sine curve** with the road drawn along the same curve (a real curling road, not left/right steps).
  - [x] **23.4c Dashboard "Continue" echo** — DONE. New `components/dashboard/ContinuePath` reuses the path's `next_up` + the shared `NextUp` banner, deep-linking to the unit that holds the next lesson; shown on the Dashboard under the hero. Renders nothing when caught up / no path. tsc + eslint + build clean.
- [x] **23.5 Lesson player** — DONE. **Grading (`grading.py`)** is deterministic + **server-side** for all 6 seeded types (answers are stripped from the API payload, so they can't be read from the client; the solution is revealed only *after* an attempt). Forgiving on case/whitespace/edge-punctuation, **strict on umlauts/ß** ("schon" ≠ "schön"); simple types may list `|`-separated alternatives. **Endpoints:** `GET /lessons/<id>/` (items, answers stripped, `is_new`; **402** if a free user is out of energy for a *new* lesson), `POST /lessons/<id>/answer/` (immediate per-item feedback, records nothing), `POST /lessons/<id>/complete/` (**re-grades every answer authoritatively**, awards XP/crown, consumes energy). **Rules verified:** pass ≥60%; energy spent only on a **successful first completion** (redo free, fail free, quit free); premium bypasses energy; locked lesson → 403. **Frontend:** `LessonPlayerPage` at `/path/:unitId/lesson/:lessonId` — progress bar + quit, per-item UI (multiple-choice, text, sentence-order token builder, review card, grammar card), correct/incorrect feedback, and a summary (XP / crown / energy) that invalidates the path + unit queries. Trail nodes are now **clickable** (unlocked only). tsc + eslint + build + ruff + check clean.
- [x] **23.6 Energy system** — DONE. The model/regen/consume landed in 23.1 and the 402 + out-of-energy screen in 23.5; this brick made it **live and global**. New **`GET /api/curriculum/energy/`** so the meter can tick without loading the path; a shared `_energy_payload()` now feeds the energy/path/complete responses (one shape, no duplication) and adds `refill_hours`. New **`useEnergy()` hook** — React Query + a **1s local countdown** that **self-refetches when it hits zero** (the moment a bolt actually regenerated), plus a 5-min safety poll and refetch-on-focus; premium never ticks. **`EnergyMeter` moved into the `TopBar`** (always visible, hidden on the smallest screens) and removed from the PathPage header; finishing a lesson invalidates `energy` so the bar drops immediately. **Verified:** full → no countdown; −1 → ~4h countdown; **regen-on-read** (no cron: 4h elapsed → back to 3); drained + 1h elapsed → ~3h left; premium → `∞`, no countdown; guest → 401. tsc + eslint + build + ruff + check clean.
- [x] **23.7 Premium tier (flag, no payments)** — DONE. New **`accounts/permissions.py::IsPremium`** (gates on `profile.has_premium`, **never** a hardcoded user list) applied to **all AI endpoints** (via the existing `_AI_PERMISSIONS`) and **Recite**; unlimited energy was already wired in 23.1/23.6. Premium exposed to the client on `/api/auth/user/` (`has_premium`, `premium_until`, `trial_started_at`) so the UI gates on one field. New **`accounts/views/premium.py`**: `GET /api/accounts/premium/` (status + `trial_available`) and `POST /api/accounts/premium/trial/` — the **one-time 7-day trial**, guarded by `trial_started_at` so it can't be farmed. **Frontend:** `PremiumLock` upsell (perks + "Start 7-day free trial", content blurred behind it) and a `RequirePremium` route wrapper mirroring `RequireAuth`, applied to `/ai` + `/speak`. **Verified:** free → AI 403 + Recite 403; trial → premium 7 days + AI 200; second trial → 400; expired → `has_premium` false + AI 403 again. tsc + eslint + build + ruff + check clean. Admin toggle works via the existing UserProfile fields. Stripe remains 23.16.
- [x] **23.8 Level-gating everywhere (data + API layer)** — DONE. Made the ≤-level rule **real** rather than per-page ad-hoc. New **`apps/accounts/levels.py`** is the single source of truth (`level_rank`, `visible_levels`, `is_level_visible`, `visible_levels_for(user)` — guests get the lowest level only); `curriculum.gating` now re-exports from it instead of keeping a second rank table, and `videos` dropped its third copy (`CEFR_ORDER`/`_order`). **Content had no level to gate on**, so: added **`Chapter.cefr_level`** (migration `books/0002`, default A1 — Words/Grammar inherit it via one join; the seed sets it) and **`HistoryLesson.cefr_level`** (migration `history/0003`, default A1). **Enforced server-side** on Word Bank (`WordViewSet`), **Review** (`due_words_for` — otherwise forward vocab leaked in the back door), Grammar (`GrammarRuleViewSet`), History (`HistoryLessonViewSet`); Videos keeps its **B1 unlock** *and* now the ≤-level cap. **Verified:** A1 user sees no B1/C1 anything; B1 sees B1 but no C1; C1 sees all; review doesn't leak; guests see A1 only; videos unlocked=False at A1, and at B1 return only A1–B1. ruff + check + tsc + eslint + build clean.
  - [x] **23.8b Per-page lock/blur + "next up" UI** — DONE (delivered inside the page redesigns): blurred locked words (23.9), locked grammar topics + "Next topic" banner (23.10), Videos ≤-level + unlock card (23.11), History ≤-level (23.12), path "Next up" + Dashboard "Continue" (23.4/23.4c).
  - [x] **23.8c Level the legacy content** — DONE (verify + decision, no data change). Investigated: the legacy vocab is **Menschen A1.1 (492 words) + A1.2 (68 words)** and the 6 history lessons — **all genuinely A1**, so the `books/0002` A1 default was *correct*, not a mislabel; nothing to relevel. Owner chose to **keep** it (fuller Word Bank ~587 / Grammar ~21 for the demo) rather than retire; full **retirement of the Menschen seed stays deferred to 23.3b** (when authored A1 curriculum replaces it). No forward-level content is exposed (verified in 23.8).
- [x] **23.9 Word Bank v2** — DONE. **`Word` had no part of speech**, so grouping needed one: added `Word.part_of_speech` (migration `vocabulary/0006`) + **`vocabulary/pos.py`** with `guess_part_of_speech` (German nouns are capitalised / carry der-die-das; infinitives end -en/-eln/-ern, with a length floor + stoplist so "gern"/"gestern" aren't verbs). `Word.save()` guesses only when blank — **explicit values always win**, so curated content + admin fixes stick. Data migration `0007` backfilled the ~570 legacy rows (**587 classified, 0 blank**: 360 nouns / 115 other / 100 verbs / 11 phrases). The 27 curated A1 words now carry **explicit** POS (the guesser called `Hallo`/`Danke` nouns — they're phrases). **API:** `WordSerializer` exposes `cefr_level` (from the chapter) + `part_of_speech` + **`locked`**; `locked_chapter_ids_for()` locks Lektionen **at your own level you haven't reached** (below-level = open review; legacy/user-added chapters with no unit are never locked). **Frontend:** rebuilt `WordBankPage` — grouped **Level → part of speech** (no Lektion numbers), per-level accent, search, locked words blurred + lock icon, "Add Words" kept, and **AI-generate shown locked for free users**. **Dead code:** the rewrite orphaned `WordRow` + `WordOverview` → deleted. **Verified:** before any lesson all 27 path words locked → after finishing U1/L1 only U1's 9 unlock (27→18); legacy words never lock; reseed idempotent (587, no dupes); auto-guess on create works. ruff + check + tsc + eslint + build clean.
- [x] **23.10 Grammar v2** — DONE. **Backend:** new **`grammar/unlocking.py::grammar_unlock_map(user)`** — a topic unlocks with **the lesson that teaches it** (grammar lives on only some Lektionen, so it's tied to specific lessons, not general progress); below-level topics are open review, a topic taught by several lessons opens when **any** completes, and topics **no lesson teaches** (the 18 legacy rules) stay open rather than vanishing. `GrammarRuleSerializer` gained `cefr_level` (via chapter), `locked`, and `unlock_lesson` (`{id,title,unit_id,unit_title,unit_order,lesson_order}` — null once unlocked) which powers the next-topic hint; the viewset supplies the map via context. curriculum is imported lazily so `grammar` keeps no hard dependency on it. **Frontend:** rebuilt `GrammarPage` — grouped **Level → topic** (category) with per-level accent, no Lektion numbers; locked topics blurred + lock + "finish X to unlock" tooltip; a **"Next topic"** banner naming the topic that unlocks first (sorted by unit/lesson order) and deep-linking to its unit; search; reading view kept (skips locked topics). **Dead code / spec fix:** the public **"Add topic" form was removed** (`GrammarForm` + `createGrammarRule` deleted) — Spec v3 says content is pre-generated + admin-approved + shared/global, so users injecting global grammar contradicted it; admin still adds via Django admin. **Verified:** with nothing done the 3 seeded topics are locked with the right unlock lessons → finishing U1/L2 unlocks exactly `sein & Personalpronomen`; the 18 legacy rules never lock; guests see 0 locked; forward-level grammar still hidden (A1 can't see a C1 rule, C1 can). ruff + check + tsc + eslint + build clean.
- [x] **23.11 Videos v2** — DONE. Added `ShowSuggestion.image_url` (migration `videos/0003`, optional) + admin "Artwork" column; serializer exposes it. **Hotlinking channel logos was rejected on purpose** — the prod CSP allows images only from `'self' data: images.unsplash.com res.cloudinary.com`, so third-party logos would be **silently blocked in production** (same trap as Google Fonts in 21.1), they're someone else's IP, and their URLs rot. Instead the new **`SourceArt`** component *draws* the source when `image_url` is blank: a deterministic per-platform gradient tile + initials (DW/ZDF/ARD…) — no external fetch, no CSP issue, no copyright exposure — and renders the image (with graceful fallback) when set to a Cloudinary/Unsplash asset the owner controls. **Frontend:** `VideosPage` rebuilt on the v3 kit — artwork-led cards, per-level accent sections, `PageHeader`, and a `SectionCard` upsell for the locked state. Level-gating unchanged (already server-side from 23.8). **Verified:** A2 → `unlocked=false`, 0 picks; B1 → 9 picks, levels A1–B1 only, planted C1 pick invisible; C1 → sees it; payload carries `image_url` (blank → tile). ruff + check + tsc + eslint + build clean.
- [x] **23.12 History v2** — DONE. Added `HistoryLesson.excerpt` + `image_url` (migration `history/0004`), both optional; admin gained level/era filters + an "Image" column. **`excerpt` is derived from the body when blank** (`_derive_excerpt`: strips markdown, clips to ~180 chars on a word boundary) so the 6 existing lessons became article cards with **no data entry**. Images follow the same rule as 23.11 — the prod CSP allows only `'self' data: images.unsplash.com res.cloudinary.com`, so hotlinking is blocked in prod and historical imagery is a copyright minefield; new **`EraArt`** *draws* a deterministic per-era gradient tile when `image_url` is blank, and renders an owner-set Cloudinary/Unsplash asset (with fallback) when present. **Frontend:** `LessonList` rebuilt as **news-article cards** (hero + title + excerpt + level + completed check) grouped by era with per-era accents; `HistoryPage` moved onto `PageHeader` + loading/empty states. Level-gating already server-side (23.8). **Verified:** A1 → 6 articles, planted B2 article invisible; B2 → 7, sees it; card payload carries `excerpt` (derived) + `image_url` (blank → tile). ruff + check + tsc + eslint + build clean.
- [x] **23.13 AI chat history** — DONE. `ai_assistant` had **no models at all** (chat was client-side only, lost on refresh). Added `Conversation` (user FK, title, `-updated_at` ordering = sidebar order) + `Message` (role/content) — migration `ai_assistant/0001` — with `apply_auto_title()` filling the title from the first user message (plain truncation, **no AI call** for a cosmetic string). New `conversations.py`: `GET/POST /api/ai/conversations/`, `GET/PATCH/DELETE /api/ai/conversations/<id>/`, `POST /api/ai/conversations/<id>/messages/` (persists the user turn, replays the last 20 turns as context into `llm.chat`, persists the reply, returns both). Every view scopes to `request.user` → another user's chat is a **404**. Premium-gated + throttled via the existing `_AI_PERMISSIONS`/`_AI_THROTTLES`; a 503 from the model persists **nothing** (no half turns). Admin added (conversation + inline read-only messages). The one-shot `/ai/chat/` endpoint **stays** — the AI slide-over panel asks throwaway questions with nothing to resume. **Frontend:** `api/conversations.ts` + types; `AIAssistantPage` rebuilt ChatGPT-style — conversation sidebar (new/resume/rename inline/delete), persisted thread, suggestions on empty, markdown replies. **Verified:** auto-title from first message; history replayed into `llm.chat` (stub-patched, no quota spent); thread persists (4 msgs); **isolation — another user gets 404 on GET/DELETE and sees 0 convos**; rename works, empty title/message → 400; delete → 204 cascades; **free user → 403**. ruff + check + tsc + eslint + build clean.
- [x] **23.14 Level exam** — DONE. New `LevelExamAttempt` (migration `curriculum/0003`) + `exam.py`. **Questions are sampled from the level's own exercises** rather than authored separately — the exam stays in sync as content grows (23.3b) and needs no extra authoring; only deterministically-gradable types are sampled (no `free_text`, which needs AI). **The question set is frozen on the attempt** and graded against on submit, so a client can't substitute easier questions. Endpoints: `GET /api/curriculum/exam/` (progress + unlocked), `POST …/exam/start/` (403 while locked), `POST …/exam/submit/` (grades, and **promotes only from the level actually examined**, forward-only). Tunables: `EXAM_UNLOCK_RATIO` (0.9), `EXAM_PASS_THRESHOLD` (0.8), `EXAM_QUESTION_COUNT` (12). **Refactor:** extracted `grading.public_exercise()` (single answer-stripper, shared by lesson player + exam) and `components/exercises/ExerciseInput` + `lib/exercises.isAnswered` (shared answer controls) — the lesson player now uses both, so the two can't drift. **Frontend:** `ExamPage` at `/path/exam` (routed before `/path/:unitId`) — locked state with a progress bar, intro, one-question-at-a-time with Back/Next (no per-question feedback — it's an exam), and a result screen that refreshes the user on promotion; `PathPage` gained an unlocked-checkpoint banner. **Verified:** locked → start 403; **no answer leak** in exam questions; blank submit → 0%, not promoted, still A1; resubmitting an attempt → 400; all-correct → 100% → **promoted A1→A2**. ruff + check + tsc + eslint + build clean. **Note:** supersedes the dormant Phase 14 `evaluate_level`/`LevelDefinition` threshold logic, which reported `can_advance` but never actually promoted anyone — retire it in a cleanup brick.
- [x] **23.15 Gamification polish** — DONE. New **`GET /api/curriculum/gamification/`** — read-only aggregation over data the lesson player already writes (`PathLessonProgress.xp_earned`/`crown`), nothing new stored: `total_xp` + `crowns` + `lessons_completed` (lifetime) and `level_lessons_done/total` (current level). Dashboard gained a **`GamificationRow`** (Total XP / Crowns / Lessons done / level progress tiles) between the streak banner and the word-stats. Per-lesson **crown states already render** on the path nodes + unit trail (23.4/23.5), and the **streak banner already existed** (Phase 15) — this brick fills the one real gap: XP + crowns were awarded but never shown anywhere. Leagues/leaderboards deferred. **Verified:** fresh user → all zeros; after 3 lessons → 30 XP / 3 crowns / 3 done. ruff + check + tsc + eslint + build clean.
- [ ] **23.16 Stripe payments (last)** — real checkout + webhook + subscription state, monthly + annual, 7-day trial → paid; replaces the manual premium flag.
