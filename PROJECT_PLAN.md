# German Learning Platform — Project Plan

Work proceeds one brick at a time. Say **"do the next brick"** to drive progress. Tick boxes as bricks complete. Full context: `KNOWLEDGE_BASE.md` (current state) and `DESIGN.md` (UI rules).

> **Status (2026-06-22):** Phases **0–18 done and live** in production (Vercel + Render + Neon), plus a marketing **landing page** + **account menu / Settings / Privacy**. **In progress:** a page-by-page **UI polish pass** (integrating hand-copied 21st.dev components, re-themed to our tokens). **Left:** Phase 11 (more exercise content + paste-your-own importer + voice practice + drill variants), Phase 19 (generic readers), plus ops polish (rotate secrets, prod SMTP/domain for mandatory email verification, optional Google OAuth).

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
Goal: Claude generates content suggestions and checks free-text exercise answers.

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

- [x] **13.1 Auth** — `django-allauth` + `dj-rest-auth` + DRF token: email/password (verification optional in dev, console email backend). `apps.accounts` + `UserProfile`(cefr_level) auto-created via signal. Frontend: token interceptor + 401 auto-logout, `AuthContext`, `AuthPage` (login/register), **guest-aware app shell** (sidebar user/logout, account-only routes gated). Google OAuth deferred (needs owner's OAuth creds).
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
- [ ] **UI polish pass (page-by-page)** — go through each page (Dashboard, Review, Word Bank, Grammar, Exercises, Drills, Recite, Videos, History, Books, AI, Auth/Onboarding) improving layout/visual quality, integrating hand-copied **21st.dev** components re-themed to our DESIGN tokens (via the Magic MCP at dev time; components are copied into the repo, no runtime dependency).

## Remaining open items (decide during build)
- Exact CEFR threshold tuning for video unlock + history language switch (defaults set; revisit once real progression speed is seen).
- Whether to ever store recitation audio for "listen back" (currently discarded → would need Cloudflare R2/S3).
- Source/licensing of "other books" content (owner to provide).
