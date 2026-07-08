# Code Audit — 2026-07-06

> Full-codebase audit: bugs, security, dead/legacy code, readability. Each item is a
> checkbox brick — tick when fixed. Severity: 🔴 high · 🟠 medium · 🟡 low.
>
> **Status (2026-07-06): Phase 20 complete.** All code items done + verified
> (ruff · manage.py check · eslint · npm run build all green; security items
> behaviourally tested). **3 items remain open by design:** **S5** (rotate keys —
> ops task, only the owner can do it in the dashboards), **B3 + D2** (retire the
> "Menschen" seed books / `seed_menschen` — deferred to Phase 22, they die when
> the new curriculum content lands).

Baseline at audit time: `eslint` ✓ · `npm run build` ✓ · `ruff` ✓ · `manage.py check` ✓ ·
no missing migrations · no orphaned frontend files · no TODO/FIXME markers.

---

## 1. Bugs

- [x] **B1 🔴 Recitation audio upload is broken** — `frontend/src/api/recitation.ts:14`
  hardcodes `Content-Type: multipart/form-data`, which strips the multipart boundary so
  Django can't parse the file. Identical to the avatar bug already fixed in
  `api/account.ts`. Fix: `{ "Content-Type": undefined }` + comment. One line.
- [x] **B2 🟠 Destructive actions swallow failures** — in
  `components/settings/DangerZoneSection.tsx`, `resetProgress().catch(() => {})` and
  `deactivateAccount().catch(() => {})` ignore errors and then show success ("Progress
  reset.") / log the user out anyway. A failed request looks like it worked. Fix:
  surface the error via `errorText`, only report success on 2xx.
- [ ] **B3 🟠 "Menschen" brand name + thin legacy content in production DB** — the seeded
  books are titled **"Menschen A1.1" / "Menschen A1.2"** (a Hueber trademark) and hold
  only ~5 exercises/handful of grammar per level. Superseded by the Phase 22 curriculum
  plan: when new content lands, rename/replace these books and retire `seed_menschen`.
- [x] **B4 🟡 Placement test timer keeps counting while Gemini grades** — cosmetic;
  pause the elapsed timer once submit starts (`PlacementTestForm`).

## 2. Security

- [x] **S1 🔴 `complete_onboarding` is re-callable forever** —
  `backend/apps/accounts/views.py:271`. Any authenticated user (or stolen token) can
  POST it at any time to set a **new username + password without knowing the old
  password**, bypassing both the change-password flow and the 30-day username cooldown.
  Fix: reject with 403 when `profile.profile_complete` is already `True`.
- [x] **S2 🔴 Destructive endpoints don't require the password** — *policy decided:
  password required for all three.* Currently `delete_account` checks the password
  **only if the client sends one** (omit the key → account deleted), and
  `reset_progress` / `deactivate_account` never ask. Since every user sets a password in
  onboarding, make the password **mandatory server-side** for delete, reset-progress,
  and deactivate; update the Settings UI to collect it for each.
- [x] **S3 🟠 No brute-force throttle on login** — `/api/auth/login/` only falls under
  the global anon rate (120/min/IP): ~172k password guesses/day per IP. Add a scoped
  throttle (e.g. `login: 5/min`) on the login view; consider the same for
  `complete_onboarding` and the social-login code exchange.
- [x] **S4 🟠 Avatar upload accepts any file, any size** — `upload_avatar` streams
  whatever it gets to Cloudinary. Add a size cap (~5 MB) and `content_type`
  check (`image/*`) before uploading (mirror the recitation size-cap pattern).
- [ ] **S5 🔴 Rotate exposed credentials (ops, not code)** — the Neon DB password, Brevo
  SMTP key, Gemini API key, and Cloudinary secret were all shared in plaintext during
  development chats. Rotate all four in their dashboards, then update Render env +
  `backend/.env`. (Old Resend key too, if the account still exists.)
- [x] **S6 🟠 Auth tokens never expire and live in `localStorage`** — DRF tokens are
  permanent; any XSS = permanent account takeover. Mitigations (pick during
  implementation): scheduled token rotation, expiring tokens (e.g. django-rest-knox),
  or move to httpOnly cookie auth. Also prerequisite for the Settings v2 "active
  sessions / per-device logout" feature (one global token can't do per-device).
- [x] **S7 🟡 `preferences` JSON is unbounded** — `update_profile` merges arbitrary
  client JSON into `UserProfile.preferences` (any keys, any size). Whitelist known
  preference keys and cap payload size.
- [x] **S8 🟡 No security headers on the frontend** — add CSP,
  `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy` via `vercel.json`
  `headers`. Backend already gets HSTS/SSL redirect from Django's prod block.
- [x] **S9 🟡 Unvalidated free-text `phone`** — accept only `+`, digits, spaces, max
  length; or drop the field until SMS verification exists.
- [x] **S10 🟡 Prompt-injection surfaces documented** — placement free-write, recite
  transcript, and AI chat all flow into Gemini prompts. Blast radius is limited to the
  requesting user (their own level/feedback), so acceptable — but keep user text
  clearly delimited in prompts and never let AI output drive privileged actions.

## 3. Dead / legacy code

- [x] **D1 Export-level dead-code sweep** — file-level scan found no orphans; run
  automated export-level tools once (`npx knip` on frontend, `vulture` on backend),
  review, and delete confirmed dead exports.
- [ ] **D2 `seed_menschen` + `_menschen_vocab.py` (630 lines) + `_menschen_lessons.py`
  (499 lines)** — becomes fully dead the moment Phase 22 curriculum content lands;
  delete then (tracked by B3).
- [x] **D3 `pypdf` installed in venv but absent from `requirements.txt`** — intentional
  (dev-only PDF tool). Either uninstall or note it; never ship it in requirements.

## 4. Readability (functions/components too big to scan)

- [x] **R1 `ExerciseCard.tsx` (217)** — one component juggles all 9 exercise types +
  submission + reveal + AI feedback. Split: per-type answer renderer already partly in
  `InteractiveInputs`; extract `useExerciseAttempt` hook + `AnswerReveal` component.
- [x] **R2 `ReviewPage.tsx` (241)** — SRS session state machine (queue, rating,
  requeueing, completion) is inline in the page. Extract a `useReviewSession` hook;
  page becomes layout only.
- [x] **R3 `InteractiveInputs.tsx` (231)** — four interactive input types in one file;
  split into `components/exercises/inputs/{MultipleChoice,Matching,SentenceOrder,WordBank}.tsx`.
- [x] **R4 `HistoryPage.tsx` (204, 3 functions)** — list, reader, and quiz in one file;
  split into `components/history/{LessonList,LessonReader,LessonQuiz}.tsx`.
- [x] **R5 `backend/apps/accounts/views.py` (~300)** — seven unrelated concerns in one
  module (leveling, streak, profile, avatar, social login, onboarding, danger ops).
  Split into a `views/` package: `leveling.py`, `profile.py`, `social.py`, `danger.py`.
- [x] **R6 Convention** — adopt a soft cap: pages ≤ ~150 lines (layout + hooks), any
  logic beyond that moves to hooks/components. Document in CONTRIBUTING.md.
