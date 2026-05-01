# Design Language

## Type Scale

One scale. No custom one-offs. Use `clamp()` for fluid sizes where needed.

| Step | Name | Size | Weight | Use |
|------|------|------|--------|-----|
| 1 | `text-xs` | 12px | 400–500 | Labels, captions, timestamps |
| 2 | `text-sm` | 14px | 400–500 | Secondary body, UI labels |
| 3 | `text-base` | 16px | 400 | Primary body copy |
| 4 | `text-lg` | 18px | 500–600 | Lead text, card titles |
| 5 | `text-xl` | 20px | 600 | Section subheadings |
| 6 | `text-2xl` | 24px | 600–700 | Page subheadings |
| 7 | `text-3xl` | 30px | 700 | Page headings |
| 8 | `text-4xl+` | 36–48px | 700–800 | Hero headings, display |

Line height: `leading-tight` (1.25) for headings, `leading-relaxed` (1.625) for body. Never use `leading-loose` on headings.

Letter spacing: `tracking-tight` on display text (`text-3xl` and up), `tracking-normal` on body.

```tsx
// Page heading
<h1 className="text-3xl font-bold tracking-tight leading-tight text-gray-900">

// Body
<p className="text-base leading-relaxed text-gray-700">

// Caption
<span className="text-xs text-gray-500 font-medium uppercase tracking-wide">
```

---

## Color Scale

Use Tailwind's built-in 50–950 scale. Pick one brand hue and use it consistently.

**Default brand color: `indigo`** (swap to match project).

| Token | Tailwind | Use |
|-------|----------|-----|
| `bg-surface` | `gray-50` | Page background |
| `bg-card` | `white` | Card/panel background |
| `border` | `gray-200` | Default borders |
| `text-primary` | `gray-900` | Headings, strong text |
| `text-secondary` | `gray-600` | Body copy |
| `text-tertiary` | `gray-400` | Placeholders, disabled |
| `accent` | `indigo-600` | Primary actions, links |
| `accent-hover` | `indigo-700` | Hover on accent |
| `accent-subtle` | `indigo-50` | Tinted backgrounds, badges |
| `destructive` | `red-600` | Errors, delete actions |
| `success` | `green-600` | Confirmation, success states |
| `warning` | `amber-500` | Warnings, caution |

**Semantic tokens in tailwind.config.ts:**

```ts
// tailwind.config.ts
theme: {
  extend: {
    colors: {
      brand: colors.indigo,
      surface: colors.gray[50],
    }
  }
}
```

Dark mode: flip `gray-900` ↔ `white` and `gray-50` ↔ `gray-900` for surfaces. Accent colors shift one step lighter (`indigo-500` instead of `indigo-600`) on dark backgrounds for contrast.

---

## Spacing Scale

Base unit: **4px**. Use Tailwind's default scale (`p-1` = 4px, `p-2` = 8px, etc.).

| Scale | px | Use |
|-------|----|-----|
| `1` | 4px | Tight internal gaps (icon + label) |
| `2` | 8px | Input padding block, badge padding |
| `3` | 12px | Small component padding |
| `4` | 16px | Default component padding |
| `5` | 20px | Comfortable component padding |
| `6` | 24px | Card padding, section gaps |
| `8` | 32px | Between components |
| `10` | 40px | Section vertical padding |
| `12` | 48px | Large section gaps |
| `16` | 64px | Page section spacing |
| `24` | 96px | Hero vertical padding |

**Rule of thumb:** Components breathe at `p-4`–`p-6`. Sections breathe at `py-12`–`py-16`. Never use arbitrary values like `p-[13px]` — round to the nearest step.

---

## Contrast Rules

WCAG AA minimums (non-negotiable):
- **4.5:1** — normal text (< 18px or non-bold)
- **3:1** — large text (≥ 18px or ≥ 14px bold), UI components, focus indicators

Hard rules:
- `gray-600` on `white` passes at 5.9:1. Use for secondary text.
- `gray-400` on `white` fails at 2.9:1. Use only for decorative/placeholder text, never for informative content.
- `indigo-600` on `white` passes at 5.2:1. Safe for text and icon use.
- **Never use `gray-300` text on `white`** regardless of design intent.

Check tool: [https://webaim.org/resources/contrastchecker/](https://webaim.org/resources/contrastchecker/)

When to override: brand has a light color that fails — use it as a background tint only, never for text.

---

## Visual Hierarchy

Three levels. Every screen should have exactly one level-1 element.

**Level 1 — Primary:** What the user must see first.
- Largest type on the page, or most visually distinct element
- Full `text-gray-900` / `text-primary`
- Full-weight action (filled primary button)

**Level 2 — Secondary:** Supporting content, secondary actions.
- One step down in size or weight
- `text-gray-600` or reduced weight
- Ghost/outline buttons, secondary labels

**Level 3 — Tertiary:** Metadata, hints, decoration.
- `text-sm text-gray-400`
- Never competes with level 1 or 2 for attention

```tsx
// Correct: three clear levels
<div>
  <h2 className="text-2xl font-bold text-gray-900">Plan your trip</h2>        {/* L1 */}
  <p className="text-base text-gray-600 mt-1">Search and compare options</p>  {/* L2 */}
  <span className="text-sm text-gray-400 mt-1 block">Updated 2 hours ago</span> {/* L3 */}
</div>
```

**Weight as hierarchy signal:** Prefer weight (`font-semibold`, `font-bold`) over size increases when space is constrained. A `text-base font-semibold` heading over `text-sm font-normal` body is clear hierarchy without size jumping.

**Color as hierarchy signal:** Use `text-gray-900` → `text-gray-600` → `text-gray-400` to step down emphasis without changing size.
