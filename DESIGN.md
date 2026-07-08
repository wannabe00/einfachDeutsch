# German Learning Platform — Design System

> Read before building any UI brick. Every page must follow these rules. Tokens map to Tailwind v3 CSS variables in `src/index.css`. Keep this doc and the tokens in sync.

---

# Design v2 — Bauhaus (APPROVED DIRECTION, not yet implemented)

> Decided 2026-07-06 with the owner. Everything in this section is the plan for the
> redesign (PROJECT_PLAN Phase 21). Until the foundation brick lands, the v1 system
> below this section remains the source of truth for any UI work.

## Why / one line
**German modernism for learning German.** Bauhaus: strong grid, flat geometric shapes,
confident type, functional color. Distinctive and ownable — the opposite of a shadcn/AI
template — and thematically *ours* (the movement is German). Keep v1's discipline (no
gamification kitsch, whitespace, honest copy); replace its anonymous look.

## Identity system: gender = shape + color
The der/die/das colors become the **brand palette**, and each article also gets a
**geometric shape** — the classic Bauhaus trio:

| Article | Color | Shape |
|---|---|---|
| **der** (m.) | blue | ● circle |
| **die** (f.) | rose | ▲ triangle |
| **das** (n.) | amber | ■ square |

- The shape+color pair appears on `ArticleBadge` (accessibility win: gender is no longer
  color-only), flashcards, drills, and as the app's logo mark (three shapes in a row).
- **Semantic rule:** inside vocabulary contexts the three colors always mean gender.
  In *chrome* (decoration, section markers, charts, hero graphics) they may be used as
  brand colors — but **interactive elements** (buttons, links, focus) use only the
  primary accent (der-blue) plus the semantic green/red/amber, so no one ever confuses
  "this is clickable" with "this is feminine".

## Typography
- **One geometric grotesk everywhere: Space Grotesk** (via `@fontsource`), weights
  400/500/700. Fallback `system-ui`. (Body copy may fall back to Inter if long-form
  readability suffers — decide in the foundation brick.)
- Poster-scale headings: display `clamp(2.5rem → 4rem)/1.05`, weight 700, tracking
  `-0.03em`. Section labels: **uppercase, small, letter-spaced** (`text-xs tracking-[0.15em]`).
- Big numerals as design elements: section numbers ("01 — Grammatik"), stat values,
  Lektion numbers rendered oversized in muted or article colors.
- German study text keeps its v1 rule: always visually louder than surrounding UI chrome.

## Color (dark-first)
Both themes stay; **dark is the designed-first experience**, light is a warm "paper"
variant (off-white, near-black ink) rather than a gray SaaS light mode. Exact HSL values
are chosen in the foundation brick and written into `src/index.css` — direction:
- Dark canvas: near-black with a *warm* tint (not blue-slate), flat (drop the indigo glow).
- Light canvas: warm paper `~40 20% 96%`, ink text.
- Primary accent = **der-blue**; die-rose and das-amber appear in geometry, badges,
  charts, and highlights. Retire the separate indigo accent (one less color competing).
- Semantic green/red/amber unchanged.

## Surfaces, borders, shape language
- **Flat blocks, hard edges.** Radius drops from `rounded-xl` to `rounded-sm` (cards)
  and `rounded-none` where it feels right; pills only for small badges.
- Borders become **visible and intentional**: 1.5–2px solid, often in `--foreground`,
  instead of hairline gray. Structure over shadow — shadows only as an optional solid
  **offset block** (`4px 4px 0` in border color) on hover/active, never blur.
- Recurring decorations: thin **diagonal-stripe bands**, oversized outline shapes
  cropped at section edges, thick horizontal rules between sections.

## Imagery
- **Geometric SVG compositions** (the three shapes, grids, arcs) are the default visual
  for heroes, empty states, and feature cards — built in-repo, no stock.
- Keep **2–3 real Munich/Berlin photos** (landing hero, dashboard hero, culture band) —
  treated with a **duotone/overlay** in brand colors so photography and geometry feel
  like one system.
- No other stock photography, no illustrations-of-people packs, no 3D blobs.

## Navigation shell (restyle, same skeleton)
Keep the top bar + hover-expand sidebar behaviour. Restyle: square icon tiles in the
rail; the active item is a **filled color block** (der-blue with white icon); wordmark
`einfachDeutsch` set in Space Grotesk with the three-shape logo mark; top bar gets a
2px bottom rule instead of a soft shadow.

## Settings v2 (the priority page)
Replace the stacked-cards pile with **vertical tab nav + one focused panel**
(GitHub/Stripe pattern). Left rail lists tabs; right side shows exactly one panel.
Rows inside a panel: label + description left, control right, thin rule between rows —
no nested cards.

**Tabs and contents:**
1. **Profile** — avatar (shape-framed), name/surname, username (30-day note inline),
   birthday, email (read-only), level (read-only + "set by test/admin" note).
2. **Account & Security** — change password (button reveals form, confirm field),
   connected accounts (Google/GitHub, read-only list), active sessions with per-device
   logout *(needs backend token rework — see AUDIT S6)*, log out everywhere.
3. **Learning** — daily goal, new words/day, review session size, exercise difficulty
   mix, show/hide hints, auto-advance after correct answers, schedule weekdays.
4. **Appearance** — theme (light/dark/**system**), accent color (der-blue / die-rose /
   das-amber), font size (S/M/L), reduced motion.
5. **Language & Region** — UI language (EN/DE), formality (du/Sie) used in prompts and
   feedback, umlaut keyboard bar on/off, timezone.
6. **Data & Privacy** — export my data, privacy policy, notification emails toggles.
7. **Danger zone** — reset progress / deactivate / delete, each **password-confirmed**
   (AUDIT S2), visually separated with the danger color.

New preferences are stored in the existing `UserProfile.preferences` JSON (whitelisted
keys — AUDIT S7); items marked *needs backend* get their own bricks.

## Per-page redesign notes (Phase 21 order)
1. **Foundation** — new tokens/typography/shape components (`ShapeMark`, `SectionLabel`,
   `GeoDivider`), restyled Button/Input/Card primitives, nav restyle. The whole app
   changes feel in one brick.
2. **Settings v2** — as specced above.
3. **Dashboard** — duotone hero, oversized due-count numeral, stat blocks with thick
   rules, quick-launch tiles with shape icons.
4. **Landing** — same sections as today, restyled: poster hero (duotone Marienplatz +
   giant grotesk headline), der/die/das teaser becomes shape+color (it's the brand),
   geometric feature grid, culture band photos duotoned.
5. **Review + Exercises + Drills** — flashcard as flat block with 2px border and
   article shape watermark; quality buttons as color blocks; exercise inputs restyled.
6. **Remaining pages** — Word Bank, Grammar, Books, Videos, History, Recite, AI,
   Auth/Onboarding/Placement (wizard steps get "Schritt 03 / 07" oversized numerals).

## What carries over from v1 unchanged
The cliché ban table, German conventions (noun capitalization, gender colors), token
architecture (CSS vars + Tailwind mapping, never hardcode values), accessibility rules
(AA contrast, focus rings, reduced motion, 44px targets), Lucide icons, desktop-first
responsive behaviour.

---

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
