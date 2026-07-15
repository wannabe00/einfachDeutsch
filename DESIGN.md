# German Learning Platform — Design System

> Read before building any UI brick. Every page must follow these rules. Tokens map to Tailwind v3 CSS variables in `src/index.css`. Keep this doc and the tokens in sync.

---

# Design v2 — Cinematic (APPROVED DIRECTION, not yet implemented)

> Decided 2026-07-06 with the owner. Direction: a **fusion** — the layout/motion
> DNA of spaceship.com (cinematic, scroll-storytelling, dark-first, premium)
> **plus our own der/die/das identity**. Adapted, NOT copied (our colours, our
> photos, our animations, our brand). **Scope: landing/marketing page FIRST**;
> in-app pages stay calmer/functional until the owner decides to extend it. This
> supersedes the earlier Bauhaus draft. Until the landing brick ships, Design v1
> (below) remains the source of truth.

## Why / one line
**Cinematic, image-led, premium — Germany as the star.** Big Berlin/Munich
photography, bold type, and scroll-driven "moments" make it feel like a launch
film, not a template. Still ownable via the der/die/das colour+shape system.

## THE MAIN THING: imagery (owner's #1 priority)
Real **Berlin + Munich photography is the hero of the identity** — full-bleed,
edge-to-edge, dramatically lit (Brandenburger Tor, Marienplatz, the Isar, Berlin
at night, U-Bahn, Reichstag). Patterns to use:
- **Full-bleed hero photo** behind the headline; dark gradient/overlay so white
  text stays legible.
- **Photo "moments"** between sections — each a full-viewport image with one big
  line of text over it (Spaceship-style scroll storytelling).
- Optional **duotone treatment** (photo tinted toward the accent) so photography
  and UI feel like one system.
- Sourcing: free Unsplash (verified URLs, graceful gradient fallback on error)
  or owner-provided files in `/public`. Never hotlink unverified URLs.

## Motion (adapted from Spaceship)
- **Scroll-reveal**: headings + text **fade up** (opacity 0→1 + translateY ~24px)
  as they enter the viewport (IntersectionObserver). Stagger children slightly.
- **Parallax** on hero photos (slow drift, already used on current landing).
- Honour `prefers-reduced-motion` — disable all of it.
- Keep it tasteful: one effect per section, fast (300–500ms ease-out).

## Colour (dark-first, German-flag accent — swappable)
- **Near-black canvas** (warm or neutral), white text, muted-gray subtext, ONE
  electric accent. Very high contrast.
- **Accent = German-flag inspired for now**: black canvas + an electric **red**
  (or **gold**) accent. Pick exact hex in the foundation brick. Keep it as the
  `--accent` token so it can be **swapped to der-blue later** with one change
  (owner may switch).
- der/die/das stay their brand colours (blue/rose/amber) in vocab contexts +
  charts; the single accent drives CTAs/links/focus so "clickable" ≠ "feminine".
- Semantic green/red/amber for feedback unchanged.

## Identity: der/die/das kept
Gender still = **shape + colour** (der ● blue / die ▲ rose / das ■ amber) on
ArticleBadge, flashcards, drills, and the logo mark (three shapes). This is what
keeps the cinematic look from being a generic dark SaaS clone.

## Typography
- **Space Grotesk** (self-hosted via `@fontsource` — NOT Google Fonts; the prod
  CSP `font-src 'self'` blocks external fonts). Big, bold headings (700),
  ~clamp(2.5rem→4rem), tight tracking. Muted subtext. Never justify.

## Layout: section "moments"
Landing = a sequence of full-width sections, each one idea: **giant heading + one
line + one CTA**, often over a photo. Generous vertical rhythm. Keep the existing
sections but make them cinematic: hero, der/die/das tester (our interactive
hook — keep it), feature strip, culture/photo band, CEFR path, FAQ + CTA + footer.

## Components
- **Pill CTAs** (rounded-full) — the one place we soften from flat/sharp; ghost +
  filled variants (filled = accent). Matches the premium feel.
- Cards: dark surfaces, subtle borders, hover lift.
- Nav: keep the app's top-bar + hover-sidebar skeleton for in-app pages. On the
  **landing**, a transparent cinematic top bar over the hero (logo left, Log in /
  Get started right), turning solid on scroll.

## In-app extension (owner-locked 2026-07-14)
The landing shipped (21.1); the owner then decided to extend the system inward.
Locked decisions for **all in-app pages**:
- **Dark-only.** The app drops the light/dark toggle and renders one dark
  cinematic theme everywhere. `ThemeContext` pins `dark`; `ThemeToggle` retires.
- **Minimal / functional imagery.** No marketing photography inside the app —
  the full-bleed Berlin/Munich photos stay on the landing only. In-app = near-
  black surfaces, the brand accent, and at most a *subtle* brand glow for depth.
  Working pages must stay fast and legible.
- **Navigation = spaceship-style top bar (desktop) + collapsible left drawer
  (mobile).** Keep today's nav items unchanged; only the shell changes. Desktop
  retires the left rail and moves primary nav into a restyled top bar (logo left,
  nav, `AccountMenu` right). Mobile gets a cleaner collapsible left drawer. Both
  collapsible. Active state uses the brand accent.
- **Type + accent** carry over from the landing (Space Grotesk headings, the
  swappable `--brand` accent) into the in-app token set.
- **der/die/das** colour+shape identity is unchanged in vocab/charts.
- **Build order:** Settings + Profile first, then dashboard, then study surfaces,
  then auth pages. See PROJECT_PLAN 21.2–21.8. One page per brick/branch.

## Phase 21 order (revised — landing first, then inward)
1. **21.1 Landing redesign** *(done)* — cinematic hero, section moments,
   der/die/das tester, interactive sightseeing backdrop, pill CTAs, `--brand`.
2. **21.2 Dark-only foundation** → **21.3 nav shell** → **21.4 Settings v2** →
   **21.5 Profile v2** → **21.6 Dashboard v2** → **21.7 study surfaces** →
   **21.8 auth pages**. (Details in PROJECT_PLAN.md.)

## What carries over from v1 unchanged
The cliché ban (no mascots/confetti/rainbow XP), German conventions (noun
capitalisation, der/die/das colours), token architecture (CSS vars + Tailwind,
never hardcode values), accessibility (AA contrast, focus rings, reduced motion,
44px targets), Lucide icons, self-hosted fonts.

# Design v3 — Learning Path "dark + depth" (Phase 23, APPROVED)

> Decided 2026-07-15 with the owner (Learning-Path pivot, PROJECT_PLAN Phase 23).
> The app becomes a **Duolingo-style guided path**. The Design v2 dark shell
> stays, but the flat near-black + thin-outline card look was too plain — v3 adds
> **depth and warmth** while keeping our identity. Marketing landing (v2) is
> unchanged. Applies to all in-app pages.

## Direction: "dark + depth" (not flat black)
- Keep a **dark base** but give it life: **layered gradients**, soft **glows**,
  subtle **imagery/illustration**, and **rounder, chunkier cards** with a hint of
  elevation — not hairline outlines on flat black.
- **Per-unit section colours:** each path unit gets its own accent (a small
  curated palette) so the path reads as colourful, Duolingo-like sections — while
  the global brand accent (**German-flag red `--brand`**) still drives primary
  CTAs/focus. der/die/das colours stay reserved for **gender** (grammar/vocab).
- Still premium and legible; playful, not childish. No rainbow-XP clutter.

## Core new components (build in 23.2, reuse everywhere)
- **Lesson node** — circular/rounded path step with 4 states: **completed**
  (crown/check, section colour), **current** ("Start" pulse), **available**,
  **locked** (greyed, lock icon, **label blurred**).
- **Lock/Blur overlay** — the one consistent "not unlocked yet" treatment across
  path, Word Bank, Grammar, Videos, History (blur the content + small lock +
  optional "unlock by finishing X").
- **"Next up" indicator** — a persistent banner/CTA showing the next lesson /
  grammar topic / section, on the path top, Dashboard, and each gated page.
- **Energy meter** — bolt/heart-style counter with a refill countdown; an
  out-of-energy state that offers "wait / go premium".
- **Premium lock + upsell** — the treatment for AI Assistant / Recite when free.
- **XP + crown** chips; keep the existing streak banner, restyled.

## Page-specific notes
- **Path (Practice):** Duolingo-style **vertical winding node path** grouped into
  unit sections (vertical-list variant kept for later). Header = "Continue" CTA.
- **Lesson player:** focused, one-item-at-a-time, progress bar, immediate
  correct/incorrect feedback (semantic green/red), end-of-lesson XP/crown summary.
- **Word Bank:** grouped **Level → part of speech**; unreached words lock/blurred.
- **Grammar:** grouped **Level → topic** (no lesson numbers); locked until the
  linked lesson is done; "next topic" indicator.
- **Videos:** cards with a **source image/logo**; ≤-level only.
- **History:** **news-article cards** — hero image + excerpt → full read; ≤-level.
- **AI Assistant:** ChatGPT-style two-pane — conversation list + thread.
- **Level exam:** distinct, more formal "checkpoint" styling (Goethe-like).

## Kept from v2 / v1
Space Grotesk headings + Inter body (self-hosted), der/die/das colour+shape,
token architecture (never hardcode), accessibility (AA, focus, reduced motion,
44px), Lucide icons. Gamification = XP + per-lesson crowns + streak (no leagues
yet). The v2 cinematic **landing** is untouched.

# Design v1 (CURRENT — in production until Phase 21 foundation lands)

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
