# German Learning Platform — Knowledge Base

> This is the **living state** of the project: what exists *right now*, how to run it, and what's next. New here? Read `WORKFLOW.md` first, then this file, then `PROJECT_PLAN.md`.
>
> **Plan vs. Knowledge Base:** `PROJECT_PLAN.md` = the *intended* future. This file = the *current reality*. Update the changelog at the bottom after every completed brick.

---

## 1. What this is

A personal German vocabulary and grammar study platform. Core features:
- **Vocabulary flashcards** — show English, type the German word with its article (e.g. "der Hund")
- **Spaced repetition (SM-2)** — same algorithm as Anki; words schedule themselves based on how well you know them
- **Grammar reference** — grammar rules entered from your textbooks, browsable and searchable
- **Book exercises** — tasks from your books with answer checking
- **Claude AI assistant** — generates vocabulary suggestions, explains grammar, creates exercises

Single-user. No authentication in v1. Content is added progressively as you work through chapters in your books.

---

## 2. Current status

- **Phase:** 0–7 complete; post-plan feature work ongoing (see §11 Roadmap).
- **Last completed:** interactive exercise types + 6 drills + original Lektion 1 exercise set + deep-editorial dark-first redesign.
- **In progress / next up:** Spec v2 — the big build (deployment, accounts, CEFR leveling, recitation v2, video/history/book tracks). Full phased plan in `PROJECT_PLAN.md`. Project just cleaned + linted (ruff backend, eslint frontend, both clean).
- **AI chat: LIVE.** Provider is **Google Gemini** (`gemini-2.5-flash`) via `apps/ai_assistant/llm.py`. `GEMINI_API_KEY` is set in `backend/.env`. Note: `gemini-2.0-flash` free quota was exhausted (429) so we use `2.5-flash`. Without a key, endpoints still return a graceful **503**.
- **Both servers:** backend (`venv_mac/bin/python manage.py runserver` → :8000); frontend (`npm run dev` → :5173). `tsc --noEmit` clean.
- **Note:** venv was recreated for macOS as `venv_mac/` (original `venv/` was Windows). node_modules also reinstalled for macOS. Filters use the chapter DB **id** (not lesson number) — after a `seed_menschen --reset` the ids shift.

### Feature inventory (what exists now)
- **Dashboard** — 6 stat cards, 7-day review activity chart, per-chapter due counts.
- **Review** — chapter-pick start screen, SM-2 flashcards, Skip (re-queues), umlaut buttons, quality buttons.
- **Word Bank** — chapter pills, 15/page pagination, overview (New/Learning/Review/Learned + accuracy/mistakes/correct + most-missed), Add Words popup (single + paste-list + CSV), "Generate with AI" button. Per-word performance tracked on the backend.
- **Grammar** — By-chapter ⇄ By-topic toggle, pill menus, topic quick-buttons, Markdown rules. **← being redesigned.**
- **Exercises** — chapter chooser; 9 types (translation, fill_blank, article, conjugation, free_text, multiple_choice, matching, sentence_order, word_bank); interactive renderers + server-side grading; original Lektion 1 set authored.
- **Drills** — Gender Triage, Blind Forge, Unscramble, Flash Recall, Sentence Shuffle, Match Pairs (all run off the user's own vocab/grammar data).
- **Books** — book + chapter list; chapters link to placeholder detail pages (teacher-panel ready).
- **AI Assistant** — chat page + slide-in AI panel (LIVE via Gemini).
- **Recite (speak-to-AI)** — paste a text → study → hide & speak it (Web Speech API, de-DE) → word-diff highlight (missing/extra, accuracy %) + short Gemini tutor note. Chrome/Edge only.
- **Chrome** — collapsible sticky sidebar, dark-first editorial theme + light mode toggle.

---

## 3. How to run locally

```bash
# Backend
cd backend
source venv/bin/activate          # Windows: venv\Scripts\activate
python manage.py runserver         # http://localhost:8000

# Frontend (separate terminal)
cd frontend
npm run dev                        # http://localhost:5173

# Type check (frontend)
cd frontend && npx tsc --noEmit

# Django system check
cd backend && python manage.py check
```

---

## 4. Tech stack & key decisions

| Area | Choice | Status |
|---|---|---|
| Backend framework | Django 5.2 LTS + Django REST Framework | built (DRF + CORS configured) |
| Backend language | Python 3.12+ | Python 3.12.10 |
| Frontend framework | React 19 + TypeScript + Vite | built (React 19.2, Vite 8, TS 6) |
| Styling | Tailwind v3 + shadcn/ui | built (Tailwind 3.4, zinc base, CSS vars, dark via `.dark`) |
| State (server) | React Query (@tanstack/react-query) | built (QueryClientProvider in main.tsx) |
| Routing | react-router-dom | built (BrowserRouter, 7 routes, layout route) |
| HTTP client | Axios | built (src/api/client.ts) |
| Database (dev) | SQLite (Django default) | built (migrated + seeded) |
| Database (prod, later) | PostgreSQL | not planned yet |
| SRS algorithm | SM-2 (custom implementation, no library) | not built |
| AI | Claude API via anthropic SDK (backend only) | not built |
| Markdown rendering | react-markdown | not built |
| Charts (Phase 7) | Recharts | not built |
| Auth | None in v1; Django auth in Phase 7+ | deferred |

---

## 5. Directory map (current reality)

```
german-platform/
├── AGENTS.md
├── CLAUDE.md
├── WORKFLOW.md
├── PROJECT_PLAN.md
├── KNOWLEDGE_BASE.md    ← this file
├── DESIGN.md
├── CONTRIBUTING.md
├── README.md
├── .gitignore
├── backend/                    ← Django project (brick 0.1)
│   ├── manage.py
│   ├── requirements.txt        ← frozen deps (Django 5.2.15, DRF, cors, dotenv, anthropic)
│   ├── .env.example
│   ├── venv/                   ← virtual environment (git-ignored)
│   ├── db.sqlite3              ← dev DB, built-in migrations applied (git-ignored)
│   ├── config/                 ← settings.py, urls.py, wsgi.py, asgi.py
│   └── apps/
│       ├── books/              ← models, serializers, views (BookViewSet), urls, admin, migrations, seed_data
│       ├── vocabulary/         ← models (Word/WordProgress), serializers, signals, admin; srs.py placeholder (Phase 3)
│       ├── grammar/            ← models (GrammarRule), serializers, admin; views/urls placeholder (Phase 4)
│       ├── exercises/          ← models (Exercise/ExerciseAttempt), serializers, admin; views/urls placeholder (Phase 4)
│       └── ai_assistant/       ← claude.py/views/urls placeholders (Phase 6)
└── frontend/                   ← React + TS + Vite (brick 0.3)
    ├── package.json            ← react 19.2, vite 8, axios, react-query, react-router-dom, react-markdown
    ├── index.html, vite.config.ts, eslint.config.js
    ├── tsconfig.json / tsconfig.app.json / tsconfig.node.json
    ├── node_modules/           ← git-ignored
    ├── public/                 ← favicon.svg, icons.svg
    └── src/
        ├── main.tsx            ← QueryClientProvider + BrowserRouter
        ├── App.tsx             ← Routes (7 pages under Layout)
        ├── index.css           ← Tailwind + DESIGN tokens (light/.dark)
        ├── vite-env.d.ts       ← typed VITE_API_BASE_URL
        ├── api/client.ts       ← Axios instance (other api/*.ts are placeholders)
        ├── lib/                ← utils.ts (cn), site.ts (SITE_NAME); levenshtein.ts placeholder
        ├── types/index.ts      ← all shared API interfaces
        ├── hooks/ contexts/    ← placeholders (filled in later phases)
        ├── components/
        │   ├── ui/             ← button, input, badge, card, separator (shadcn)
        │   ├── layout/         ← Layout.tsx, Sidebar.tsx (PageHeader/ThemeToggle placeholders)
        │   └── vocabulary/ grammar/ exercises/ ai/ charts/  ← placeholders
        └── pages/              ← 7 routed placeholder pages
```

This map grows with each brick. Update it here when new directories or key files appear.

---

## 6. Environment variables

### Backend (`backend/.env`) — git-ignored
| Var | Needed for | Set yet? |
|---|---|---|
| `ANTHROPIC_API_KEY` | Claude API (Phase 6) | no |
| `SECRET_KEY` | Django (auto-generated in settings) | auto |
| `DEBUG` | Django debug mode | yes (True for dev) |

### Frontend (`frontend/.env.local`) — git-ignored
| Var | Needed for | Set yet? |
|---|---|---|
| `VITE_API_BASE_URL` | Axios base URL | no (defaults to `http://localhost:8000/api`) |

All documented (no values) in `backend/.env.example` and `frontend/.env.example`.

---

## 7. API routes (current reality)

| Method | Route | Purpose |
|---|---|---|
| GET | `/api/` | Browsable API root (links to registered endpoints) |
| GET/POST | `/api/books/` | List / create books (nested `chapters` in each) |
| GET/PUT/PATCH/DELETE | `/api/books/{id}/` | Retrieve / update / delete a book |
| GET/POST | `/api/books/{id}/chapters/` | List / create chapters for a book |
| * | `/admin/` | Django admin (all models registered) |

---

## 8. Pages (current reality)

All routed and rendering placeholders (filled in later phases):

| Route | Component | Status |
|---|---|---|
| `/` | `Dashboard` | placeholder |
| `/review` | `ReviewPage` | placeholder |
| `/words` | `WordBankPage` | placeholder |
| `/grammar` | `GrammarPage` | placeholder |
| `/exercises` | `ExercisesPage` | placeholder |
| `/books` | `BooksPage` | **live** — lists books + chapters, inline add-chapter form |
| `/ai` | `AIAssistantPage` | placeholder |

Shared chrome: `components/layout/Layout.tsx` (sidebar + centered `max-w-900px` main) and `components/layout/Sidebar.tsx` (240px nav, active link highlighted via `NavLink`).

---

## 9. Known issues / open decisions

- **Dev DB is SQLite** (`backend/db.sqlite3`, git-ignored). Prod target: **Neon Postgres** (NOT Render's bundled Postgres — it auto-expires after 30 days). Migration path: `dumpdata`/`loaddata` once Neon is provisioned (Phase 12).
- **AI provider is Gemini** (`gemini-2.5-flash`). Transcription + grading for recitation v2 will also use Gemini, behind a swappable interface (so paid Whisper/Azure can drop in later). `gemini-2.0-flash` free quota was exhausted → use `2.5-flash`.
- **Multi-user is live** (Phase 13.1–13.2): email/password auth (token), content shared / progress per-user, freemium guest access. Remaining in Phase 13: server-side throttling (13.3), frontend guest daily-cap + sign-up wall (13.4), teacher forward-compat (13.5). Google OAuth deferred (needs owner's creds).
- Free-tier LLM quotas are low — chat/grading may 429 when exhausted (resets daily).

---

## 10. Roadmap — see PROJECT_PLAN.md "Spec v2"

The full phased plan now lives in **`PROJECT_PLAN.md`** (Phases 8–19). Phases 8–10 are **done** (grammar gallery, Gemini chat, recite v1). The big upcoming build (Spec v2) — with these **locked decisions** — is detailed there:

- **Hosting:** frontend → Vercel, backend → Render (persistent), DB → **Neon Postgres**.
- **AI:** all transcription + grading on **Gemini** (free key), behind a swappable `Transcriber`/grader interface (not paid Whisper/Claude).
- **Accounts:** content **shared**, progress **per-user** (`django-allauth` email + Google); teacher→student curation comes later.
- **Recitation v2:** retell-in-your-own-words → record → upload → Gemini transcribe + grade (content coverage, der/die/das + case errors, pronunciation proxy); **audio discarded** after transcription; configurable per-user daily cap.
- **Leveling:** CEFR A1–C2, completion-gated. **Schedule:** Mon/Wed/Fri unlocks, reviews any day, streak freeze tokens (2 + 1 per 14-day streak, auto-consumed, all configurable).
- **Defaults:** video suggestions unlock after **A2** (curated list per level); history track English+German through A2 then German-only from **B1**.

Still ongoing from the earlier roadmap: original per-lesson exercise sets, a "paste-your-own" exercise importer, voice conversation practice, and the extra drill/question-style variants (Phase 11).

---

## 11. Changelog (append newest at top)

- _2026-06-19 — Email verification (mandatory) DONE. `ACCOUNT_EMAIL_VERIFICATION="mandatory"` (+ `ACCOUNT_EMAIL_REQUIRED=True`); custom `AccountAdapter.get_email_confirmation_url` points the link at the SPA (`FRONTEND_URL` env, default :5173) → `/verify-email/<key>`. Registration now returns no token (just "Verification e-mail sent."); `LoginSerializer` blocks unverified accounts (superusers + legacy accounts with no EmailAddress row exempt, so the owner isn't locked out). **Dev:** link prints to runserver terminal (console email backend); **prod:** wire SMTP (Phase 12). Frontend: `registerUser` returns `{status: "logged_in" | "verify_email"}`, `AuthContext.register` only resolves the user when logged in, `AuthPage` shows a "Check your email" panel after register, new `VerifyEmailPage` at `/verify-email/:key` POSTs the key + shows verifying/success/error. **Verified (curl):** register→201 no token, pre-verify login→400, verify-email→200, post-verify login→200+token. ruff+tsc+eslint+django check clean — backend/apps/accounts/{adapter.py,serializers.py}, backend/config/settings.py, frontend/src/{api/auth.ts,contexts/AuthContext.tsx,pages/{AuthPage,VerifyEmailPage}.tsx,App.tsx}_

- _2026-06-19 — Phase 13.3 (Endpoint protection + throttling) DONE. **Throttling (settings REST_FRAMEWORK):** global `AnonRateThrottle` (`anon` 120/min) + `UserRateThrottle` (`user` 600/min) as the spam/DDoS ceiling; all rates env-overridable (THROTTLE_ANON/USER/AI_BURST/AI_DAILY). **AI endpoints now account-only:** every `/api/ai/*` view decorated `@permission_classes([IsAuthenticated])` + `@throttle_classes([AIBurstThrottle, AIDailyThrottle])` (new `apps/ai_assistant/throttles.py`, scopes `ai_burst` 12/min + `ai_daily` 120/day per user) to protect the free Gemini quota. Guest exercise auto-feedback (ExerciseCard → /ai/check-answer) now 401s for guests but degrades silently (no onError, feedback only renders when present; 401 interceptor only logs out when a token exists). Content-write gating done in 13.2; Drills/Recite are frontend-gated (no dedicated backend endpoints). **Verified (curl):** guest /ai/chat/→401, authed→200 (Gemini live), 429 after 12-burst. **Known gap (flagged as separate task):** non-AIConfigError exceptions from Gemini still surface as raw 500 — should become a clean 502. tsc/eslint untouched (no FE change needed), ruff+django check clean — backend/config/settings.py, backend/apps/ai_assistant/{views.py,throttles.py}_

- _2026-06-19 — Phase 13.2 (Per-user progress) DONE. **Models:** `WordProgress.word` OneToOne→FK (related_name `progress_records`) + nullable `user` FK + `unique_together(user, word)`; `ReviewLog` + `ExerciseAttempt` get nullable `user` FK. Content models (Word/Chapter/Grammar/Exercise) stay global. **Removed** the post_save signal that auto-created one WordProgress per Word — progress is now created on demand via `get_or_create(user, word)` in the review action. **Views (vocabulary):** `current_user()` + `due_words_for(user, chapter)` helpers (unseen words count as new/due; guest=None → all words due); `WordViewSet._with_user_progress` prefetches the requesting user's progress into `user_progress` (serializer `progress` field reads it, null otherwise); `review` persists + logs only for signed-in users (guest gets computed-but-unsaved SM-2 state, no 401); StatsView/ActivityView per-user (guest → content totals + zero activity, all words 'new'). Per-action permissions: content writes (create/update/destroy/import/bulk on words; create/update/destroy on exercises) require auth; reads + attempt + review are public. ExerciseAttempt records `user` (null for guests). **Migrations:** vocabulary 0004 (schema) + 0005 (data: assign pre-existing single-user rows to first user/owner, else drop) + exercises 0003. The owner's legacy 560 progress rows were preserved under their existing account. **Frontend:** `Word.progress` type now `WordProgress | null` (UI already null-guarded). **Verified end-to-end (curl + preview):** user A 560→559 due after one review; user B independent (560, sees A's word as null); guest review computes interval but adds no DB row; per-user stats correct; Word Bank renders 559 New/1 Learning for A with no console errors. tsc+eslint+ruff+django check clean — backend/apps/vocabulary/{models,views,serializers,signals,admin}.py + migrations 0004/0005, backend/apps/exercises/{models,views,admin}.py + migration 0003, frontend/src/types/index.ts_

- _2026-06-19 — Phase 13.1 (Auth + guest-aware shell) DONE. **Backend:** `apps.accounts` (UserProfile.cefr_level, auto-created via post_save signal, migration 0001); `django-allauth` + `dj-rest-auth` + DRF TokenAuthentication wired in settings (email-only login, no username — auto-generated; verification optional in dev; console email backend). Custom `RegisterSerializer`/`LoginSerializer`/`UserDetailsSerializer` (adds cefr_level). Endpoints: `/api/auth/registration|login|logout|user/`. Passwords hashed by Django PBKDF2 (security requirement satisfied). Dev CORS now accepts any localhost port (gated to DEBUG); prod keeps explicit allow-list. **Frontend:** token interceptor + 401 auto-logout (`auth:logout` event) in client.ts; `AuthContext` (bootstrap from stored token, login/register/logout); `AuthPage` (login+register modes); `api/auth.ts`; `lib/access.ts` (freemium policy: ACCOUNT_ONLY_PATHS = /drills /speak /ai, GUEST_DAILY_ACTION_LIMIT=20). **Guest-aware shell:** App.tsx no longer login-walls everything — Layout is public, only account-only routes wrapped in `RequireAuth`; Sidebar shows lock badges on gated items for guests + footer with user email/Log out (or Log in/Sign up). vite.config honors PORT env (for preview). **Verified in preview end-to-end:** guest dashboard loads, guest→/drills redirects to /login, register→201→token→user fetch→redirect, sidebar shows email+Log out. tsc + eslint + ruff + django check all clean. **Decided (owner):** freemium model — guests use free/read-only features (rate-limited server-side, daily cap then sign-up wall); Drills/AI/Recite + all per-user writes are account-only. Google OAuth deferred (needs owner's OAuth creds). **Next:** 13.2 per-user progress data migration — backend/apps/accounts/*, backend/config/{settings,urls}.py, frontend/src/{App.tsx,api/{client,auth}.ts,contexts/AuthContext.tsx,pages/AuthPage.tsx,lib/access.ts,components/layout/Sidebar.tsx,types/index.ts,vite.config.ts}_

- _2026-06-18 — Spec v2 planning + project cleanup/lint. **Planning:** reviewed the owner's 5-area feature spec; locked decisions (all-Gemini transcription+grading behind a swappable interface; content shared / progress per-user; discard recitation audio; recommended CEFR/streak defaults). Wrote the full phased plan into PROJECT_PLAN.md (Spec v2 = Phases 12–19: deployment/Neon, accounts/allauth, CEFR leveling, Mon/Wed/Fri schedule + streaks, recitation v2, video suggestions, history track, generic book content); marked Phases 8–10 done. Updated KB §2/§9/§10, AGENTS.md architecture. **Cleanup:** removed dead 86 MB Windows `venv/` + 9 empty scaffold placeholders; added `venv_mac/` to .gitignore. **Lint:** added ruff (`backend/ruff.toml`, select E/F/I/UP/B), `ruff check` + `ruff format` clean (13 files formatted); fixed 6 eslint errors (4 set-state-in-effect → render-time pattern in ReviewPage/WordBankPage/AIPanel + FlashCard relies on remount; 2 shadcn react-refresh disables). tsc + eslint + ruff + django check all clean; backend smoke-tested (200s) — PROJECT_PLAN.md, KNOWLEDGE_BASE.md, AGENTS.md, .gitignore, backend/ruff.toml, frontend src/pages/{ReviewPage,WordBankPage}.tsx, src/components/{ai/AIPanel,vocabulary/FlashCard,ui/{button,badge}}.tsx, backend/apps/* (ruff format)_

- _2026-06-18 — Recite (speak-to-AI) feature at /speak. Phases: edit (paste target text) → study (read it) → recite (text hidden, mic on) → result. Browser Web Speech API (`useSpeechRecognition` hook, lang de-DE, Chrome/Edge only; graceful "unsupported" message). Word-level LCS diff (`src/lib/worddiff.ts`) marks missing target words (strikethrough/red) + lists extras, shows accuracy %. Short AI tutor note reuses `aiCheckAnswer` (Gemini), fails silently if no quota. Sidebar "Recite" entry + /speak route. Verified: edit/study phases render, diff math correct (100% perfect, flags missing/extra). **Mic itself untested in preview (no microphone) — user verifies with real mic.** Next roadmap: more AI/speak features (free conversation, pronunciation) + per-lesson original exercises — frontend src/pages/SpeakPage.tsx, src/hooks/useSpeechRecognition.ts, src/lib/worddiff.ts, src/App.tsx, src/components/layout/Sidebar.tsx_

- _2026-06-18 — Grammar gallery redesign + Gemini chat + docs. **Grammar:** replaced the chapter/topic pill menus with a topic-card gallery — cards grouped under Lektion headings (title + category tag), live search box, click a card → reading view with chapter label, full Markdown rule, and prev/next through the (filtered) list. No dropdowns. **AI provider → Gemini:** renamed `apps/ai_assistant/claude.py` → `llm.py`, swapped Anthropic client for `google-genai` (model `gemini-2.5-flash`), same function signatures + AIConfigError + endpoint contract (frontend unchanged except 503 message text → GEMINI_API_KEY). Added `GEMINI_API_KEY` to settings + .env.example; installed google-genai (requirements). Updated AGENTS.md AI rules. User adds GEMINI_API_KEY to backend/.env to enable chat. **Docs:** KB §2 rewritten with feature inventory + status, §10 Roadmap added (grammar redesign, Gemini chat, speak-to-AI, original exercise build-out, question-style ideas); PROJECT_PLAN gained post-plan summary + Phases 8–11. Verified grammar gallery (cards/search/reading view) + chat graceful 503 in preview, tsc clean — frontend src/pages/GrammarPage.tsx, src/components/ai/AIPanel.tsx, src/pages/AIAssistantPage.tsx; backend apps/ai_assistant/llm.py, views.py, config/settings.py, .env.example; AGENTS.md, KNOWLEDGE_BASE.md, PROJECT_PLAN.md_

- _2026-06-18 — Flash Recall drill replaces Spot the Error (removed SpotTheError.tsx + makeErrorRound). FlashRecall: an authored example sentence flashes 3s (draining progress bar), then hides → type it from memory (umlaut bar), normalized check. 6 drills total now: Gender Triage, Blind Forge, Unscramble, Flash Recall, Sentence Shuffle, Match Pairs. Also authored a **fully original** Lektion 1 exercise set (9 exercises: word_bank, multiple_choice, sentence_order, matching ×2, translation, conjugation — greetings/sein/woher/du-vs-Sie/countries), loaded into chapter 5 (source "Lektion 1 (original)"); these are my content, NOT copied from the workbook. Verified Flash Recall both phases in preview, tsc clean — frontend src/components/drills/FlashRecall.tsx, src/pages/DrillsPage.tsx, src/lib/sentences.ts_

- _2026-06-18 — 3 more drills (now 6 total) from the user's own data (no copyrighted book text). **Spot the Error**: takes an authored grammar example sentence, ~60% of rounds swap one der/die/das to a wrong article; player taps the wrong word or "Looks correct". **Sentence Shuffle**: scrambles an example sentence's words, tap-to-rebuild, checks against original. **Match Pairs**: 5 rounds × 5 vocab German↔English, click-left-then-right, locks correct/flashes wrong. Helpers in src/lib/sentences.ts (collectSentences, makeErrorRound). Wired into DrillsPage hub. Verified all three render + grade in preview, tsc clean. **Note:** declined the user's request to reproduce the full Menschen Arbeitsbuch/Kursbuch verbatim (wholesale copyright reproduction); offered instead author-original lesson-matched exercises + a future paste-your-own importer. Earlier 5 L1 sample exercises remain (reworked, not verbatim) — frontend src/components/drills/{SpotTheError,SentenceShuffle,MatchPairs}.tsx, src/lib/sentences.ts, src/pages/DrillsPage.tsx_

- _2026-06-18 — Interactive exercise-type system. Exercise model gains `payload` (JSONField), `source`, broader TYPE_CHOICES (+multiple_choice, matching, sentence_order, word_bank); `correct_answer` now optional (migration 0002). Serializer emits a **solution-stripped** payload per type (options without answer; matching left + shuffled right; sentence tokens; word_bank text+bank). Attempt endpoint `grade()` handles all types server-side and returns a UI-friendly reveal. Frontend: `components/exercises/InteractiveInputs.tsx` (MultipleChoice/SentenceOrder tap-to-build/Matching click-to-pair/WordBank click-to-fill); ExerciseCard dispatches on type; attemptExercise accepts string | string[] | map. Verified all four render + grade in preview. **Next:** load the user's real Menschen A1.1 Arbeitsbuch Lektion 1 exercises into this system (parse from their local extracted text → local DB; verbatim workbook content stays on their machine, not in chat/committed source) — backend/apps/exercises/{models,serializers,views}.py + migration 0002, frontend/src/components/exercises/{ExerciseCard,InteractiveInputs}.tsx, src/api/exercises.ts, src/types/index.ts, src/lib/labels.ts_

- _2026-06-18 — UX batch + major features. **(a)** Review: Skip button (rotates word to queue end via a local queue), clickable umlaut bar (ä ö ü ß Ä Ö Ü, inserts at caret) in FlashCard + drills. **(b)** Word Bank: CSV import moved into Add-Words popup; chapter dropdown → pill buttons (reusable `components/layout/ChapterButtons.tsx`); 15-per-page pagination; `WordOverview` panel (New/Learning/Review/Learned + accuracy/mistakes/correct + most-missed); "Generate with AI" button; "Paste list" bulk importer. Backend: per-word tracking fields on WordProgress (times_seen/times_correct/times_wrong/lapses, migration 0003) updated in the review action; new POST /api/vocabulary/words/bulk/. **(c)** Grammar: dropdowns → "By chapter ⇄ By topic" toggle + chapter pills + category pills + per-rule topic-name quick buttons; backend orders rules ascending by book+Lektion. **(d)** Books: chapters now link to /chapters/:id → ChapterDetailPage (counts + word list + placeholder for future content/teacher panel). **(e)** Sidebar: collapsible (w-60↔w-16, persisted), sticky full-height, theme control inside. **(f)** Design overhaul: deep-editorial dark-first palette (slate + indigo accent) in index.css, dark is now the default theme, subtle indigo canvas glow. **(g)** Drills (games) at /drills: hub + 3 games using existing data — Gender Triage (der/die/das quick-fire), Blind Forge (type exact German, no hints), Unscramble (rebuild jumbled letters); shared DrillShell + src/lib/german.ts. Verified all in preview, tsc clean. Pending (await user content): sentence-based drills (Spot-the-error, Sentence-shuffle) + new exercise types — frontend src/pages/{ReviewPage,WordBankPage,GrammarPage,ExercisesPage,ChapterDetailPage,DrillsPage}.tsx, src/components/{drills/*,vocabulary/{UmlautBar,WordOverview,PasteWordsButton},layout/{ChapterButtons,Sidebar,ThemeToggle}}.tsx, src/index.css, backend/apps/vocabulary/{models,views,serializers}.py + migration 0003, apps/grammar/views.py_

- _2026-06-18 — Phase 7 (Polish) complete — **7.1** Recharts installed; new ReviewLog model (one row per review event — WordProgress only keeps the latest; migration 0002) written in the review action; GET /api/stats/activity/ → [{date,count}] for last 7 days (ReviewLog + ExerciseAttempt per local day). ReviewActivityChart (7-day bar) on Dashboard; ChapterProgressChart (New/Learning/Review/Learned buckets, computed client-side from word.progress) on Word Bank. **7.2** POST /api/vocabulary/words/import/ (multipart CSV: english,german,notes + chapter_id; skips english+chapter dupes, returns {created,skipped}); CSVImportButton on Word Bank (file input + chapter select). Verified: import 2 created then 2 skipped (idempotent). **7.3** ThemeProvider (localStorage 'theme', falls back to prefers-color-scheme, toggles `dark` class on <html>) wraps app in main.tsx; ThemeToggle (Sun/Moon) at sidebar bottom. Verified in preview: both charts render with real data, dark↔light toggle persists, no console errors. All tokens flip correctly — backend/apps/vocabulary/{models,views,urls}.py + migration 0002, frontend: recharts, src/components/charts/*, src/components/vocabulary/CSVImportButton.tsx, src/contexts/ThemeContext.tsx, src/components/layout/ThemeToggle.tsx, src/main.tsx, src/pages/{Dashboard,WordBankPage}.tsx, src/api/{stats,vocabulary}.ts_

- _2026-06-18 — Phase 6 (AI Integration) — all code built; needs ANTHROPIC_API_KEY in backend/.env to activate (graceful 503 + friendly UI message until then). **6.1** apps/ai_assistant/claude.py: 5 fns (suggest_words, explain_grammar, generate_exercises, check_exercise_answer, chat), model `claude-sonnet-4-20250514`, AIConfigError when key missing, shared TUTOR_SYSTEM prompt. **6.2** 5 POST endpoints under /api/ai/ (suggest-words, explain-grammar, generate-exercises, check-answer, chat) — 400 on missing fields, 503 on no key, else {"content": ...}; wired in config/urls.py. Verified: 400 + 503 paths. **6.3** AIPanel slide-in (right, 480px, backdrop, editable prompt → chat endpoint, Markdown+gfm response) via AIPanelContext provider in Layout; "AI Suggest" on Word Bank + "Generate Exercises" on Exercises open it pre-filled. **6.4** AIAssistantPage full chat (user-right/assistant-left bubbles, suggestion chips, in-session history, resets on refresh); ExerciseCard auto-calls /ai/check-answer after each attempt and shows AI tutor feedback (silently skipped without key). Added src/api/ai.ts, src/contexts/AIPanelContext.tsx, src/components/ai/AIPanel.tsx. Verified in preview: chat 503 path, slide-in panel, graceful degradation — backend/apps/ai_assistant/*, frontend/src/api/ai.ts, src/contexts/AIPanelContext.tsx, src/components/ai/AIPanel.tsx, src/pages/{AIAssistantPage,WordBankPage,ExercisesPage}.tsx, src/components/exercises/ExerciseCard.tsx, src/components/layout/Layout.tsx_

- _2026-06-18 — Phase 5 (Dashboard) + Review chapter picker — **5.1** StatsView at GET /api/stats/ (due_today, learned_total=interval>21, reviewed_today=WordProgress.last_reviewed today + ExerciseAttempts today, total_words/grammar/exercises). Added `/api/vocabulary/words/due/?chapter=` filter + new `/api/vocabulary/words/due-counts/` (total + per_chapter due map). **5.2** Dashboard: 6 StatCards (due-today accent-highlighted), Start Review button (disabled at 0 due), per-chapter due-count list. **Review enhancement:** start screen lets you pick All chapters or a specific chapter (with per-chapter due counts) before reviewing; "change" link to reselect; session summary has Review-more. Added src/api/stats.ts, fetchDueCounts, Stats type, StatCard component. Verified in preview: dashboard stats match API (546 due, 559 words, 18 grammar, 33 ex), Review filters to Lektion 1 (13 cards) — backend/apps/vocabulary/{views,urls}.py, frontend/src/pages/{Dashboard,ReviewPage}.tsx, src/components/ui/StatCard.tsx, src/api/{stats,vocabulary}.ts_

- _2026-06-18 — Phase 4 complete (Grammar & Exercises) — **4.1** GrammarRuleViewSet (?chapter & ?category filters) at /api/grammar/rules/; **4.3** ExerciseViewSet (?chapter & ?type filters) + POST /api/exercises/{id}/attempt/ (case-insensitive check, saves ExerciseAttempt, returns is_correct/correct_answer/explanation; correct_answer stays hidden in list/retrieve); both wired in config/urls.py. **4.2** GrammarPage + GrammarCard (react-markdown + **remark-gfm** for tables) + GrammarForm, chapter/category filters. **4.4** ExercisesPage + ExerciseCard (submit → green/red reveal + explanation) + ExerciseForm, chapter/type filters. Added src/lib/labels.ts (category/type label maps), AttemptResult/ExerciseType/GrammarCategory types. Installed remark-gfm. Verified end-to-end in preview: 18 rules render w/ tables, 33 exercises, correct & wrong attempt flows — backend/apps/grammar/{views,urls}.py, apps/exercises/{views,urls}.py, frontend/src/api/{grammar,exercises}.ts, src/components/{grammar,exercises}/*, src/pages/{GrammarPage,ExercisesPage}.tsx, src/lib/labels.ts_

- _2026-06-18 — Menschen content seeded — extracted the user's Wörterbuch + Menschen A1.1/A1.2 PDFs via pymupdf text layer (no OCR needed; born-digital). New idempotent `seed_menschen --reset` command builds two books: **Menschen A1.1** (Lektion 1–12, sections from dict) + **Menschen A1.2** (Lektion 13–16). Loaded 559 curated single-word vocab (Georgian dropped, English written fresh, OCR fixed, nouns carry articles), 18 author-original A1 grammar rules, 33 original exercises. Demo "Beginner German" book deleted. Data lives in `apps/books/management/commands/_menschen_vocab.py` + `_menschen_lessons.py`. Verified: 559 due words, flashcard correct/quality-button flow works end-to-end. Added pymupdf to backend venv (extraction tool only; not a runtime dep)._

- _2026-06-18 — warm palette + Inter font — updated index.css tokens from cold zinc to warm stone/sand (background `36 20% 99%`, surface `34 18% 95%`, etc.), added Inter via Google Fonts in index.html — frontend/src/index.css, frontend/index.html_
- _2026-06-18 — brick 3.5 — Review Session page: ReviewPage fetches due words, loops FlashCard → feedback → SRS quality buttons → POST review → next card, progress bar, session summary screen, empty state — frontend/src/pages/ReviewPage.tsx_
- _2026-06-18 — brick 3.4 — FlashCard component: FlashCard.tsx (correct/close/wrong verdict via normalize + Levenshtein, feedback border+bg tints, quality buttons with interval hints), levenshtein.ts pure fn — frontend/src/components/vocabulary/FlashCard.tsx, frontend/src/lib/levenshtein.ts_
- _2026-06-18 — brick 3.3 — Word Bank page: WordBankPage with live words table, chapter filter, Add Word form (WordForm.tsx), ArticleBadge.tsx (der=blue/die=rose/das=amber pills), WordRow.tsx (SRS dot: gray/amber/blue/green), vocabulary API module — frontend/src/pages/WordBankPage.tsx, src/components/vocabulary/*, src/api/vocabulary.ts_
- _2026-06-18 — brick 3.2 — SM-2 algorithm: pure Python calculate_next_review(reps, ef, interval, quality) in srs.py; POST /api/vocabulary/words/{id}/review/ updates WordProgress, returns updated state — backend/apps/vocabulary/srs.py, views.py_
- _2026-06-18 — brick 3.1 — Vocabulary viewsets + due-words: WordViewSet (CRUD, ?chapter filter, /due/ action filtered by next_review__lte=today, /review/ action), wired to /api/vocabulary/words/ — backend/apps/vocabulary/views.py, urls.py, config/urls.py_
- _2026-06-18 — macOS setup — recreated Python venv as venv_mac/ (venv/ was Windows .exe); reinstalled npm node_modules for darwin-arm64 — backend/venv_mac/, frontend/node_modules/_

> Format: `YYYY-MM-DD — brick X.Y — what changed — key files`
> Added manually (or by Claude) after each completed brick.

- _2026-06-09 — brick 2.2 — Books frontend page: src/api/books.ts (fetchBooks, createChapter), /books page with React Query — book cards list chapters, inline add-chapter form (number prefilled to next) POSTs to nested route and invalidates the books query; loading/error/empty states — `tsc --noEmit` + build clean — frontend/src/pages/BooksPage.tsx, src/api/books.ts_
- _2026-06-09 — brick 2.1 — Books/Chapters viewsets + URLs: BookViewSet (ModelViewSet) + custom GET/POST `chapters` action for /api/books/{id}/chapters/, SimpleRouter in apps/books/urls.py, included at /api/, api_root now links to book-list — verified GET /api/books/ (nested chapters), POST chapter (201) persists — backend/apps/books/views.py, urls.py, config/urls.py, config/views.py_
- _2026-06-09 — brick 1.6 — Seed data: idempotent `seed_data` command creates "Beginner German" + 2 chapters + 5 words + 2 grammar rules + 2 exercises; re-run skips cleanly — backend/apps/books/management/commands/seed_data.py_
- _2026-06-09 — brick 1.5 — Django admin: registered all models; WordAdmin (list english/german/chapter + WordProgressInline), GrammarRuleAdmin (filter chapter/category), ExerciseAdmin (filter chapter/type), Book w/ ChapterInline — backend/apps/*/admin.py_
- _2026-06-09 — brick 1.4 — DRF serializers: BookSerializer (nested read-only chapters), ChapterSerializer (book read-only), WordSerializer (nested read-only progress), WordProgress/GrammarRule/Exercise (correct_answer excluded)/ExerciseAttempt serializers — verified Word JSON nests progress, Exercise omits correct_answer — backend/apps/*/serializers.py_
- _2026-06-09 — brick 1.3 — Grammar + Exercise models: GrammarRule (category choices), Exercise (type choices, correct_answer/hint/explanation), ExerciseAttempt — migrated — backend/apps/grammar/models.py, apps/exercises/models.py_
- _2026-06-09 — brick 1.2 — Word + WordProgress models: Word (chapter FK) + WordProgress (SM-2 fields, OneToOne), post_save signal in vocabulary/signals.py registered via AppConfig.ready() auto-creates progress — verified auto-create + defaults — backend/apps/vocabulary/models.py, signals.py, apps.py_
- _2026-06-09 — brick 1.1 — Book + Chapter models: Book (title/description/created_at), Chapter (book FK, number, title, unique_together book+number) — migrated, import clean — backend/apps/books/models.py_
- _2026-06-09 — brick 0.6 — Axios + React Query + Router: src/api/client.ts (Axios instance, baseURL from VITE_API_BASE_URL with :8000/api default), env typed in vite-env.d.ts, QueryClientProvider + BrowserRouter wired in main.tsx, App.tsx routes all 7 pages under a Layout route, Sidebar (240px, NavLink active highlight) + Layout (centered max-w-900px) built, 7 placeholder pages created, frontend/.env.example documented — `tsc --noEmit` + build clean, all 7 routes serve 200 — frontend/src/api/client.ts, main.tsx, App.tsx, components/layout/*, pages/*_
- _2026-06-09 — brick 0.5 — Design tokens + TS types: added all DESIGN.md tokens (background, surface, foreground, muted-foreground, border, accent + accent-hover, success/danger/warning + bg tints, article der/die/das) to index.css for light + .dark; shadcn primitives (--primary, --ring, --destructive, --card, ...) derived from the DESIGN palette (primary actions/links = accent blue, radius bumped to 0.75rem); mapped new colors in tailwind.config (surface, accent-hover, success.bg, danger.bg, warning.bg, article.der/die/das); created src/lib/site.ts (SITE_NAME) and src/types/index.ts (Book, Chapter, Word, WordProgress, ReviewQuality/ReviewResult, GrammarRule, Exercise, ExerciseAttempt, AIResponse) — `tsc --noEmit` + build clean, tokens present in compiled CSS — frontend/src/index.css, tailwind.config.ts, src/lib/site.ts, src/types/index.ts_
- _2026-06-09 — brick 0.4 — Tailwind v3 + shadcn/ui: installed Tailwind 3.4 + postcss/autoprefixer + tailwindcss-animate + cva/clsx/tailwind-merge/lucide-react + radix slot/separator; tailwind.config.ts (zinc, darkMode class), postcss.config.js, index.css with zinc CSS vars + .dark, @/ alias (vite + tsconfig), components.json, cn() util, and button/input/badge/card/separator components; App.tsx demos Button + dark toggle — `tsc --noEmit` + `npm run build` clean, compiled CSS contains tokens/classes — frontend/tailwind.config.ts, frontend/src/index.css, frontend/src/components/ui/*, frontend/src/lib/utils.ts, components.json_
- _2026-06-09 — brick 0.3 — Vite + React + TS init: scaffolded via create-vite react-ts (React 19.2, Vite 8, TS 6, ESLint 10), installed axios + @tanstack/react-query + react-router-dom + react-markdown, named package, set HTML title — `tsc --noEmit` clean, `npm run dev` serves :5173 (HTTP 200) — frontend/package.json, frontend/src/*, frontend/vite.config.ts, tsconfig*_
- _2026-06-09 — brick 0.2 — DRF + CORS config: added rest_framework + corsheaders to INSTALLED_APPS, CorsMiddleware first, AllowAny default permission, CORS_ALLOWED_ORIGINS for :5173, /api/ browsable root view — verified GET /api/ = 200 and preflight returns Access-Control-Allow-Origin — backend/config/settings.py, backend/config/urls.py, backend/config/views.py_
- _2026-06-09 — brick 0.1 — Django project init: venv + deps installed (Django 5.2 LTS pinned over auto-selected 6.0), config/ settings·urls·wsgi·asgi written, five apps (books, vocabulary, grammar, exercises, ai_assistant) registered under apps/ with AppConfigs, .env.example + root .gitignore added; `manage.py check` clean, built-in migrations applied, runserver verified (admin login 200) — backend/config/*, backend/apps/*/apps.py, backend/requirements.txt_
- _2026-06-08 — planning — project docs created: AGENTS.md, CLAUDE.md, WORKFLOW.md, PROJECT_PLAN.md, KNOWLEDGE_BASE.md, DESIGN.md, CONTRIBUTING.md, README.md_
