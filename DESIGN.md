# German Learning Platform — Design System

> Read before building any UI brick. Every page must follow these rules. Tokens map to Tailwind v3 CSS variables in `src/index.css`. Keep this doc and the tokens in sync.

## Aesthetic in one line
Clean, focused, scholarly. The UI should disappear so you can think about German, not about the interface. Think a well-designed language textbook that became digital — not a gamified app.

## Palette (current): Deep Editorial, dark-first
The app defaults to **dark mode** (slate canvas `224 24% 6%`, surface `224 20% 11%`, text `220 20% 94%`) with an **indigo accent** (`239 84% 67%`). Light mode is a cohesive cool-slate variant with a deeper indigo (`243 75% 59%`). A faint indigo radial glow sits top-left of the canvas for subtle depth. Article colors stay distinct from the indigo accent: **der** = blue (`213 90% 65%`), **die** = rose, **das** = amber. All values live in `src/index.css` (`:root` + `.dark`). The token table below documents the *roles*; the exact HSL values in `index.css` are the source of truth.

## Avoid the "language app" clichés (non-negotiable)
The design goal is a serious study tool, not a game. These are banned:

| Don't | Do instead |
|---|---|
| Cartoon mascots, streak flames, celebration confetti | Plain text stats, honest progress numbers |
| Neon greens and oranges, rainbow XP bars | One calm accent blue; color only for functional signals |
| "You're on a 7-day streak! 🔥" notifications | "7 days in a row" in muted caption text |
| Giant rounded-everything, bubbly pill buttons | Restrained radius; mostly rectangles; pills only for badges |
| Emoji in UI copy (✨ 🚀 💡) | Lucide icons or no icon at all |
| SaaS motivational copy ("Unlock your potential!") | Concrete copy: "3 words due", "Add a word", "Review" |
| Multiple accent colors competing | One accent (`--accent`), semantic red/green/amber only |
| Heavy drop shadows, glassmorphism | Hairline borders, subtle shadow only on hover |
| Purple/violet gradients | Solid neutral surfaces |

When in doubt: remove. Whitespace and a good flashcard beat any effect.

## German-specific conventions (non-negotiable)
- **German nouns are always capitalized** in the UI — "der Hund", never "der hund". Enforce this in the FlashCard and WordRow components.
- **Article color-coding** is the primary visual signal of grammatical gender — a widely-used memory aid:
  - `der` (masculine) → blue (`--article-der`)
  - `die` (feminine) → rose (`--article-die`)
  - `das` (neuter) → amber (`--article-das`)
  - `ein/eine` (indefinite) → muted gray (no special color)
- These three colors are the **only** place in the UI where gender carries a color signal. Don't repurpose them for anything else.

## Color tokens (`src/index.css @layer base`)

Define as CSS custom properties in `:root` (light) and `.dark` (dark). Tailwind maps them via `tailwind.config.ts → theme.extend.colors`.

| Token | Light (HSL) | Dark (HSL) | Use |
|---|---|---|---|
| `--background` | `0 0% 100%` | `240 10% 4%` | page background |
| `--surface` | `240 5% 96%` | `240 4% 11%` | cards, panels, inputs on bg |
| `--foreground` | `240 10% 4%` | `0 0% 95%` | primary text |
| `--muted-foreground` | `240 4% 46%` | `240 5% 65%` | secondary text, labels, captions |
| `--border` | `240 6% 90%` | `240 4% 22%` | hairlines, dividers, input borders |
| `--accent` | `221 83% 53%` | `217 91% 60%` | primary actions, links |
| `--accent-hover` | `221 83% 45%` | `217 91% 70%` | hover state |
| `--success` | `142 72% 29%` | `142 71% 45%` | correct answer, in-stock |
| `--success-bg` | `142 76% 95%` | `142 76% 10%` | correct answer background tint |
| `--danger` | `0 84% 50%` | `0 91% 64%` | wrong answer, errors |
| `--danger-bg` | `0 86% 97%` | `0 86% 9%` | wrong answer background tint |
| `--warning` | `38 92% 44%` | `43 96% 56%` | "close" answer, near-miss |
| `--warning-bg` | `43 96% 95%` | `43 96% 10%` | close answer background tint |
| `--article-der` | `221 83% 53%` | `217 91% 60%` | masculine article badge |
| `--article-die` | `336 74% 58%` | `336 74% 70%` | feminine article badge |
| `--article-das` | `38 92% 44%` | `43 96% 56%` | neuter article badge |

Light/dark: follow the system (`prefers-color-scheme`). The `ThemeToggle` in the sidebar adds/removes the `dark` class on `<html>` (brick 7.3). Design and test every screen in **both** schemes.

**Never hardcode hex or HSL values in components** — always use the token via Tailwind class or CSS variable.

## Typography
- Font: **Inter** (via Google Fonts or `@fontsource/inter`). Fallback: system-ui.
- Scale: display `2.5rem/1.2` bold · h1 `2rem` · h2 `1.5rem` · h3 `1.125rem` · body `1rem/1.6` · small `0.875rem` · caption `0.75rem`
- Weights: 600 headings/buttons, 400 body, 500 labels.
- **German text in UI** (the word being studied) uses a slightly larger size or weight than surrounding English labels — visually separates what you're learning from the chrome.
- Tight tracking on headings (`-0.02em`). Never justify text.

## Spacing & layout
- 4px base scale (Tailwind default). Be generous — studying requires visual calm.
- **Sidebar:** 240px fixed, left side. Main content fills the rest with `max-width 900px` centered, `px-6`.
- Section rhythm: `py-8` between major sections.
- **Radius:** cards/panels `rounded-xl`, inputs `rounded-md`, badges/pills `rounded-full`.
- **Shadow:** `shadow-sm` resting, `shadow-md` on hover for cards. No heavy elevation.
- Hairline borders (`--border`) over shadows for structure.

## Responsive
- Desktop-first (this is primarily a study tool used at a desk).
- Sidebar collapses to a bottom nav strip on mobile (< 768px).
- FlashCard: max-width `480px`, centered, always has breathing room.

## Motion
- Subtle and fast (150–200ms ease-out).
- FlashCard answer reveal: short slide-in from below.
- Panel slide-in (AI panel): 250ms ease-out from the right.
- Honor `prefers-reduced-motion: reduce` — disable all transitions.

## Iconography
- **One icon set: Lucide** (`lucide-react`). 20px inline, 24px standalone. Stroke inherits `currentColor`.
- Interactive icons need `aria-label`.
- No emoji as icons.

## FlashCard — the core interaction
The most important component. It must be calm, focused, and give honest feedback.

- Centered on the page, max-width ~480px, `rounded-xl`, `shadow-sm` border.
- **Front state:** shows the English word large (`text-2xl font-semibold`); chapter badge in the top-right corner (small, muted).
- **Input state:** plain text input below the word, full width, placeholder "Type in German with article…"; Submit button.
- **Feedback states** (applied as border color + background tint):
  - Correct → `--success` border + `--success-bg` background + "✓ Correct!" in success color
  - Close → `--warning` border + `--warning-bg` background + "Almost — check your spelling"
  - Wrong → `--danger` border + `--danger-bg` background + "The answer is: [correct answer]" shown in `--foreground`
- **Quality buttons** (appear after submit, before moving to next card):
  - Again (`--danger` tint) — quality 0
  - Hard (orange-ish, `--warning` tint) — quality 2
  - Good (`--accent` tint) — quality 4
  - Easy (`--success` tint) — quality 5
  Labels: "Again", "Hard", "Good", "Easy". Show interval hint below each: "(tomorrow)", "(3 days)", etc.

## ArticleBadge component
A small pill badge that renders the article part of a German word in its gender color.
- Parse the German string to extract the article (first word).
- `der` → blue background (light tint of `--article-der`)
- `die` → rose background (light tint of `--article-die`)
- `das` → amber background (light tint of `--article-das`)
- Unknown/other → muted gray
- Font: `text-xs font-medium`. Shown inline next to the noun.

## SRS progress indicator
Small visual on word rows in the Word Bank:
- New (reps=0) → gray dot
- Learning (interval ≤ 6) → yellow dot
- Review (7–21 days) → blue dot
- Learned (> 21 days) → green dot
No numbers — just the dot + tooltip on hover.

## GrammarCard
- `rounded-xl` card with `--surface` background, `--border` border.
- Title in `text-base font-semibold`, category badge (small, muted) top-right.
- Content: Markdown rendered with `react-markdown`. Style `<code>` blocks with `--surface` background and `font-mono`. Style `<strong>` in `--foreground`.
- Example sentences: rendered in a visually distinct block — left border in `--accent` color, `pl-3`, muted background.

## Component inventory
Build these as bricks require them.

**Primitives:** `Button` (variants: `default`, `secondary`, `ghost`, `destructive`), `Input`, `Textarea`, `Select`, `Badge`, `Card`, `Skeleton`, `Separator`, `Tooltip`

**Layout:** `Sidebar` (nav links, collapse on mobile), `ThemeToggle`, `PageHeader` (title + action slot)

**Vocabulary:** `FlashCard`, `ArticleBadge`, `WordRow` (table row: english | ArticleBadge + noun | chapter | SRS dot | next_review), `SRSQualityButtons`, `WordForm` (add word inline form)

**Grammar:** `GrammarCard`, `GrammarForm`

**Exercises:** `ExerciseCard` (prompt + input + submit + reveal + AI feedback), `ExerciseForm`

**Dashboard:** `StatCard` (icon + number + label), `DueCountBadge`

**AI:** `AIPanel` (slide-in overlay), `ChatMessage` (user right / assistant left), `ChatComposer` (input + send)

**Charts (Phase 7):** `ReviewActivityChart`, `ChapterProgressChart`

## Accessibility (non-negotiable)
- WCAG AA contrast on all text + interactive elements.
- Visible focus ring on keyboard focus: `:focus-visible` → `2px solid var(--accent)` with `outline-offset: 2px`. Never remove without replacing.
- Semantic HTML: `<main>`, `<nav>`, `<section>`, `<article>`, labelled form controls.
- SRS quality buttons and article color badges: color is never the only signal — labels always accompany color.
- FlashCard input: `aria-label="Type the German translation"`.
- Hit targets ≥ 44px.
- `prefers-reduced-motion` respected.
