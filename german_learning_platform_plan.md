# German Learning Platform — Development Blueprint

---

## 1. Project Overview

A personal German learning web app with:
- Vocabulary flashcards (free-text input with article, e.g. "der Hund")
- Spaced repetition system (SRS) using the SM-2 algorithm (same as Anki)
- Grammar reference pages populated from your books
- Book exercises with AI-assisted answer checking
- Claude AI assistant for content generation and language help
- Content added progressively, chapter by chapter

No login required for v1. Single-user.

---

## 2. Tech Stack

| Layer | Technology | Why |
|---|---|---|
| Frontend | React 19 + TypeScript (TSX) | Industry standard, strong typing teaches good habits |
| Frontend build | Vite | Fast dev server, simple config |
| Styling | Tailwind CSS + shadcn/ui | Component library built on Tailwind, teaches composition |
| Backend | Django 5 + Django REST Framework | Python, clean ORM, great for learning |
| Database | SQLite (dev) → PostgreSQL (prod later) | Zero config for now |
| AI | Claude API (claude-sonnet-4) via backend | Strong language model, you already use it |
| HTTP client | Axios (frontend → backend) | Simple, widely used |
| State management | React Query (TanStack Query) | Handles server state, caching, loading states cleanly |

---

## 3. Architecture

```
┌─────────────────────────────────┐
│        React + TypeScript       │  http://localhost:5173
│  (Vite, Tailwind, shadcn/ui)    │
└────────────┬────────────────────┘
             │ HTTP / REST (JSON)
             ▼
┌─────────────────────────────────┐
│     Django + DRF (REST API)     │  http://localhost:8000
│  /api/vocabulary/               │
│  /api/grammar/                  │
│  /api/exercises/                │
│  /api/ai/                       │
└────────────┬────────────────────┘
             │
      ┌──────┴──────┐
      ▼             ▼
  SQLite DB    Claude API
  (local)    (api.anthropic.com)
```

The frontend NEVER calls Claude directly. All AI calls go through your Django backend. This keeps your API key safe and lets you add caching, logging, and rate limiting later.

---

## 4. Project Folder Structure

```
german-platform/
├── backend/                    ← Django project
│   ├── manage.py
│   ├── requirements.txt
│   ├── .env                    ← ANTHROPIC_API_KEY goes here
│   ├── config/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── apps/
│       ├── books/              ← Book + Chapter models
│       │   ├── models.py
│       │   ├── serializers.py
│       │   ├── views.py
│       │   └── urls.py
│       ├── vocabulary/         ← Words + SRS logic
│       │   ├── models.py
│       │   ├── serializers.py
│       │   ├── views.py
│       │   ├── urls.py
│       │   └── srs.py          ← SM-2 algorithm
│       ├── grammar/            ← Grammar rules
│       │   ├── models.py
│       │   ├── serializers.py
│       │   ├── views.py
│       │   └── urls.py
│       ├── exercises/          ← Book tasks + attempts
│       │   ├── models.py
│       │   ├── serializers.py
│       │   ├── views.py
│       │   └── urls.py
│       └── ai_assistant/       ← Claude integration
│           ├── claude.py       ← Claude API client
│           ├── views.py
│           └── urls.py
│
└── frontend/                   ← React + TypeScript project
    ├── package.json
    ├── tsconfig.json
    ├── vite.config.ts
    └── src/
        ├── main.tsx
        ├── App.tsx
        ├── types/
        │   └── index.ts        ← All TypeScript interfaces
        ├── api/
        │   ├── client.ts       ← Axios instance
        │   ├── vocabulary.ts
        │   ├── grammar.ts
        │   ├── exercises.ts
        │   └── ai.ts
        ├── hooks/
        │   ├── useVocabulary.ts
        │   ├── useSRS.ts
        │   └── useAI.ts
        ├── components/
        │   ├── ui/             ← shadcn/ui components live here
        │   ├── layout/
        │   │   ├── Sidebar.tsx
        │   │   └── Layout.tsx
        │   ├── vocabulary/
        │   │   ├── FlashCard.tsx
        │   │   ├── WordForm.tsx
        │   │   └── WordList.tsx
        │   ├── grammar/
        │   │   └── GrammarCard.tsx
        │   ├── exercises/
        │   │   └── ExerciseCard.tsx
        │   └── ai/
        │       └── AIPanel.tsx
        └── pages/
            ├── Dashboard.tsx
            ├── Review.tsx
            ├── WordBank.tsx
            ├── GrammarPage.tsx
            ├── ExercisesPage.tsx
            └── AIAssistant.tsx
```

---

## 5. Database Models (Django)

### books/models.py

```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='chapters')
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['number']
        unique_together = ['book', 'number']

    def __str__(self):
        return f"Chapter {self.number}: {self.title}"
```

### vocabulary/models.py

```python
class Word(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='words')
    english = models.CharField(max_length=200)          # shown to user: "dog"
    german = models.CharField(max_length=200)           # correct answer: "der Hund"
    notes = models.TextField(blank=True)                # optional: usage note
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.english} → {self.german}"


class WordProgress(models.Model):
    """SM-2 spaced repetition state for each word."""
    word = models.OneToOneField(Word, on_delete=models.CASCADE, related_name='progress')
    repetitions = models.IntegerField(default=0)        # number of successful reviews
    ease_factor = models.FloatField(default=2.5)        # SM-2 ease factor
    interval = models.IntegerField(default=1)           # days until next review
    next_review = models.DateField(auto_now_add=True)   # when to show next
    last_reviewed = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.word.english} — next: {self.next_review}"
```

### grammar/models.py

```python
class GrammarRule(models.Model):
    CATEGORY_CHOICES = [
        ('articles', 'Articles (der/die/das)'),
        ('cases', 'Cases (Nominativ, Akkusativ, etc.)'),
        ('verbs', 'Verbs & Conjugation'),
        ('sentence_structure', 'Sentence Structure'),
        ('pronouns', 'Pronouns'),
        ('adjectives', 'Adjectives'),
        ('other', 'Other'),
    ]

    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='grammar_rules')
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    content = models.TextField()                        # Markdown supported
    example_sentences = models.TextField(blank=True)   # One per line
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

### exercises/models.py

```python
class Exercise(models.Model):
    TYPE_CHOICES = [
        ('translation', 'Translate to German'),
        ('fill_blank', 'Fill in the Blank'),
        ('article', 'Choose Correct Article'),
        ('conjugation', 'Conjugate the Verb'),
        ('free_text', 'Free Text Answer'),
    ]

    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='exercises')
    exercise_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    prompt = models.TextField()                          # The question shown to user
    correct_answer = models.TextField()                  # Expected answer
    hint = models.TextField(blank=True)
    explanation = models.TextField(blank=True)           # Shown after answering
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.exercise_type}] {self.prompt[:60]}"


class ExerciseAttempt(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='attempts')
    user_answer = models.TextField()
    is_correct = models.BooleanField()
    ai_feedback = models.TextField(blank=True)           # Claude's feedback if used
    attempted_at = models.DateTimeField(auto_now_add=True)
```

---

## 6. API Endpoints (Django REST Framework)

### Books & Chapters
| Method | URL | Action |
|---|---|---|
| GET | `/api/books/` | List all books |
| POST | `/api/books/` | Create a book |
| GET | `/api/books/{id}/chapters/` | List chapters for a book |
| POST | `/api/books/{id}/chapters/` | Add a chapter |

### Vocabulary
| Method | URL | Action |
|---|---|---|
| GET | `/api/vocabulary/words/` | List all words (filter by `?chapter=id`) |
| POST | `/api/vocabulary/words/` | Add a word |
| DELETE | `/api/vocabulary/words/{id}/` | Delete a word |
| GET | `/api/vocabulary/due/` | Get all words due for review today |
| POST | `/api/vocabulary/words/{id}/review/` | Submit review result, returns updated SRS state |

Review endpoint request body:
```json
{ "quality": 4 }
```
Quality scale (shown to user as buttons): 0=Again, 2=Hard, 4=Good, 5=Easy

### Grammar
| Method | URL | Action |
|---|---|---|
| GET | `/api/grammar/rules/` | List all rules (filter by `?chapter=id` or `?category=articles`) |
| POST | `/api/grammar/rules/` | Add a grammar rule |
| PUT | `/api/grammar/rules/{id}/` | Update a rule |
| DELETE | `/api/grammar/rules/{id}/` | Delete a rule |

### Exercises
| Method | URL | Action |
|---|---|---|
| GET | `/api/exercises/` | List exercises (filter by `?chapter=id`) |
| POST | `/api/exercises/` | Add an exercise |
| POST | `/api/exercises/{id}/attempt/` | Submit an answer |

### AI Assistant
| Method | URL | Action |
|---|---|---|
| POST | `/api/ai/suggest-words/` | Generate vocabulary suggestions for a chapter topic |
| POST | `/api/ai/explain-grammar/` | Explain a grammar concept |
| POST | `/api/ai/generate-exercises/` | Generate exercises for a chapter |
| POST | `/api/ai/check-answer/` | Check a free-text exercise answer |
| POST | `/api/ai/chat/` | Open-ended German language question |

---

## 7. TypeScript Types (frontend/src/types/index.ts)

```typescript
export interface Book {
  id: number;
  title: string;
  description: string;
  chapters: Chapter[];
}

export interface Chapter {
  id: number;
  book: number;
  number: number;
  title: string;
  description: string;
}

export interface Word {
  id: number;
  chapter: number;
  english: string;
  german: string;
  notes: string;
  progress: WordProgress;
}

export interface WordProgress {
  repetitions: number;
  ease_factor: number;
  interval: number;
  next_review: string;  // ISO date string
  last_reviewed: string | null;
}

export interface ReviewResult {
  quality: 0 | 2 | 4 | 5;  // Again | Hard | Good | Easy
}

export interface GrammarRule {
  id: number;
  chapter: number;
  title: string;
  category: string;
  content: string;
  example_sentences: string;
}

export interface Exercise {
  id: number;
  chapter: number;
  exercise_type: string;
  prompt: string;
  hint: string;
  // correct_answer is NOT sent to frontend for security
}

export interface ExerciseAttempt {
  user_answer: string;
  is_correct: boolean;
  correct_answer: string;  // revealed after attempt
  ai_feedback: string;
}

export interface AIResponse {
  content: string;
}
```

---

## 8. SRS Algorithm — SM-2 (vocabulary/srs.py)

```python
from datetime import date, timedelta
from dataclasses import dataclass

@dataclass
class ReviewInput:
    repetitions: int
    ease_factor: float
    interval: int
    quality: int  # 0=Again, 2=Hard, 4=Good, 5=Easy

@dataclass
class ReviewOutput:
    repetitions: int
    ease_factor: float
    interval: int
    next_review: date

def calculate_next_review(r: ReviewInput) -> ReviewOutput:
    if r.quality < 3:
        # Wrong answer — reset
        new_reps = 0
        new_interval = 1
    else:
        # Correct answer — advance
        if r.repetitions == 0:
            new_interval = 1
        elif r.repetitions == 1:
            new_interval = 6
        else:
            new_interval = round(r.interval * r.ease_factor)
        new_reps = r.repetitions + 1

    # Update ease factor
    new_ef = r.ease_factor + (0.1 - (5 - r.quality) * (0.08 + (5 - r.quality) * 0.02))
    new_ef = max(1.3, new_ef)  # never drop below 1.3

    next_review = date.today() + timedelta(days=new_interval)

    return ReviewOutput(
        repetitions=new_reps,
        ease_factor=round(new_ef, 2),
        interval=new_interval,
        next_review=next_review,
    )
```

---

## 9. Vocabulary Answer Checking Logic

The user types their answer in a text input. Checking happens on the **frontend** first (instant feedback) and optionally confirmed by Claude for near-misses.

```typescript
// frontend/src/components/vocabulary/FlashCard.tsx

function checkAnswer(userInput: string, correctAnswer: string): 'correct' | 'close' | 'wrong' {
  const normalize = (s: string) => s.trim().toLowerCase();

  if (normalize(userInput) === normalize(correctAnswer)) {
    return 'correct';
  }

  // Check if article is right but noun has a typo
  const [correctArticle, ...correctWordParts] = correctAnswer.split(' ');
  const [userArticle, ...userWordParts] = userInput.split(' ');
  const correctWord = correctWordParts.join(' ');
  const userWord = userWordParts.join(' ');

  const articleCorrect = normalize(userArticle) === normalize(correctArticle);
  const distance = levenshteinDistance(normalize(userWord), normalize(correctWord));

  if (articleCorrect && distance <= 2) {
    return 'close';  // show yellow: "Almost! Check your spelling"
  }

  return 'wrong';
}
```

After the user submits, show 4 buttons: **Again / Hard / Good / Easy** — these map to quality scores 0/2/4/5 and are sent to the review endpoint.

---

## 10. AI Integration (backend/apps/ai_assistant/claude.py)

```python
import anthropic
from django.conf import settings

client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """You are a German language tutor assistant embedded in a learning platform.
You help a learner who is at an early stage of learning German.
Be concise, accurate, and encouraging. Always include examples with translations.
When suggesting vocabulary, always include the correct article (der/die/das) with nouns."""


def suggest_words(chapter_title: str, chapter_description: str, count: int = 10) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": (
                f"Suggest {count} useful German vocabulary words for a chapter titled "
                f"'{chapter_title}' ({chapter_description}). "
                f"Format each as: English | German (with article) | Example sentence"
            )
        }]
    )
    return response.content[0].text


def check_exercise_answer(prompt: str, user_answer: str, correct_answer: str) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": (
                f"Exercise: {prompt}\n"
                f"Expected answer: {correct_answer}\n"
                f"Student's answer: {user_answer}\n\n"
                f"Is the student's answer correct or acceptable? "
                f"Give brief feedback in 1-2 sentences. "
                f"If wrong, explain the mistake clearly."
            )
        }]
    )
    return response.content[0].text


def chat(message: str, conversation_history: list) -> str:
    messages = conversation_history + [{"role": "user", "content": message}]
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=800,
        system=SYSTEM_PROMPT,
        messages=messages
    )
    return response.content[0].text
```

---

## 11. Frontend Pages — What Each One Does

### Dashboard (pages/Dashboard.tsx)
- Words due today (count + "Start Review" button)
- Stats: total words, total learned (interval > 21 days), reviews done today
- Recent chapters added
- Quick links to all sections

### Review Session (pages/Review.tsx)
- Shows English word one at a time
- User types German answer (article + word)
- Submit → immediate feedback (correct/close/wrong)
- Reveal correct answer
- User clicks Again / Hard / Good / Easy
- Session ends when all due words are done, shows summary

### Word Bank (pages/WordBank.tsx)
- Filter by chapter (dropdown)
- Table: English | German | Next Review | SRS progress
- "Add Word" button → form (English, German, Chapter)
- "AI Suggest" button → opens AI panel pre-filled with chapter context

### Grammar (pages/GrammarPage.tsx)
- Filter by chapter or category
- Each rule displayed as a card: title, content (rendered markdown), examples
- "Add Grammar Rule" form
- "Ask AI to explain this" button on each card

### Exercises (pages/ExercisesPage.tsx)
- Filter by chapter and type
- One exercise at a time
- User types answer → submit → show correct answer + AI feedback
- "Generate exercises for this chapter" button (calls AI)

### AI Assistant (pages/AIAssistant.tsx)
- Chat interface, conversation history in React state
- Suggested quick prompts:
  - "Explain the German case system"
  - "Suggest 10 words for Chapter [X]"
  - "Give me exercises for [topic]"
  - "When do I use 'doch'?"

---

## 12. Development Phases

### Phase 1 — Foundation (Week 1–2)
Goal: Two running servers, one talking to the other.

Backend tasks:
1. `django-admin startproject config .` inside `/backend`
2. Install: `djangorestframework`, `django-cors-headers`, `python-dotenv`, `anthropic`
3. Create apps: `books`, `vocabulary`, `grammar`, `exercises`, `ai_assistant`
4. Register in `INSTALLED_APPS`, configure CORS for `localhost:5173`
5. Create `Book` and `Chapter` models, run migrations
6. Add serializers and basic viewsets for books/chapters
7. Test with `curl` or Postman

Frontend tasks:
1. `npm create vite@latest frontend -- --template react-ts`
2. Install: `axios`, `@tanstack/react-query`, `react-router-dom`, `tailwindcss`
3. Install shadcn/ui: `npx shadcn@latest init`
4. Set up `App.tsx` with router and 6 routes
5. Create `Sidebar.tsx` and `Layout.tsx`
6. Create Axios client pointing to `http://localhost:8000/api`
7. Verify you can fetch and display the books list

Milestone: Frontend shows list of books fetched from Django.

---

### Phase 2 — Vocabulary + SRS (Week 3–4)
Goal: Full review session works end-to-end.

Backend tasks:
1. Create `Word` and `WordProgress` models, migrate
2. Signal: auto-create `WordProgress` when a `Word` is saved (`post_save`)
3. Implement `srs.py` with `calculate_next_review()`
4. `GET /api/vocabulary/due/` — filter words where `progress__next_review <= today`
5. `POST /api/vocabulary/words/{id}/review/` — apply SM-2, save, return updated progress

Frontend tasks:
1. `WordForm.tsx` — form to add a word (chapter selector, English, German)
2. `WordList.tsx` — table of all words with progress indicator
3. `FlashCard.tsx` — the card component with input + submit + quality buttons
4. `Review.tsx` page — fetch due words, loop through them, show summary at end
5. Levenshtein distance helper function for "close" detection

Milestone: Full SRS review loop works. Add 10 words, review them, see next review dates update.

---

### Phase 3 — Grammar & Exercises (Week 5–6)
Goal: Content from books can be entered and browsed.

This is where you provide your books. For each chapter you'll:
- Enter grammar rules as text (markdown supported)
- Enter exercises with prompts and correct answers

Backend tasks:
1. `GrammarRule` model + CRUD endpoints
2. `Exercise` and `ExerciseAttempt` models + endpoints
3. `POST /api/exercises/{id}/attempt/` — check answer, save attempt

Frontend tasks:
1. `GrammarCard.tsx` — renders markdown content
2. `GrammarPage.tsx` — filterable list of rules, add form
3. `ExerciseCard.tsx` — prompt + input + submit + reveal
4. `ExercisesPage.tsx` — filterable exercise list

Milestone: Can add grammar rules and exercises from Chapter 1, practice them.

---

### Phase 4 — AI Integration (Week 7–8)
Goal: Claude helps generate and check content.

Backend tasks:
1. Add `ANTHROPIC_API_KEY` to `.env`, load in `settings.py`
2. Build `claude.py` client with all functions
3. Create views for all 5 AI endpoints
4. Add basic rate limiting (Django's cache framework) — optional

Frontend tasks:
1. `AIPanel.tsx` — slides in from right, reusable across pages
2. `AIAssistant.tsx` page — full chat interface
3. Add "AI Suggest" buttons to WordBank and ExercisesPage
4. Hook up AI feedback display in `ExerciseCard.tsx`

Milestone: Can ask Claude to generate 10 words for a chapter, approve and bulk-add them.

---

### Phase 5 — Polish (Week 9+)
- Dashboard with real stats (words due, streak, total learned)
- Progress charts (Recharts — already in your React available libraries)
- CSV import for words (bulk-add a chapter's vocabulary at once)
- Dark/light mode toggle
- Mobile-responsive layout

---

## 13. Setup Commands (run once)

### Backend
```bash
mkdir german-platform && cd german-platform
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install django djangorestframework django-cors-headers python-dotenv anthropic

django-admin startproject config backend
cd backend
python manage.py startapp books
python manage.py startapp vocabulary
python manage.py startapp grammar
python manage.py startapp exercises
python manage.py startapp ai_assistant
```

### Frontend
```bash
cd ..  # back to german-platform/
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install axios @tanstack/react-query react-router-dom
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
npx shadcn@latest init
```

---

## 14. Key Django Settings to Configure

```python
# backend/config/settings.py (additions)

import os
from dotenv import load_dotenv
load_dotenv()

INSTALLED_APPS = [
    ...
    'rest_framework',
    'corsheaders',
    'apps.books',
    'apps.vocabulary',
    'apps.grammar',
    'apps.exercises',
    'apps.ai_assistant',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # must be FIRST
    ...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # no auth in v1
    ]
}

ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
```

---

## 15. Git Structure

```bash
german-platform/
├── .gitignore       ← include: venv/, node_modules/, .env, db.sqlite3
├── backend/
└── frontend/
```

Use one Git repo with two subfolders. Commit at the end of each phase.

---

## What You Don't Need Yet

- Books: needed in Phase 3 (grammar + exercises)
- Vocabulary word lists: can start entering from Phase 2 onward, one chapter at a time
- Deployment: this is a local-first project for now

---

## Summary Table

| Phase | What you build | New skills learned |
|---|---|---|
| 1 | Django project structure, DRF viewsets, React router, Axios | Django apps, CORS, TypeScript interfaces |
| 2 | SRS algorithm, review session UI, signals | Django signals, Python dataclasses, React state/hooks |
| 3 | Grammar + exercise CRUD, markdown rendering | Django FKs, DRF nested routes, controlled forms in TSX |
| 4 | Claude API client, AI endpoints, chat UI | Anthropic SDK, async views, React streaming patterns |
| 5 | Dashboard stats, CSV import, charts | Django aggregations, file uploads, Recharts |
