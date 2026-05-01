# Interactions

Motion communicates state. If nothing changes state, nothing should animate.

---

## Hover States

Change one of these: color, background, shadow, or border. Never all four at once.

**What to change:**
- Text links: `text-gray-600 hover:text-gray-900` — color shift only
- Buttons: `bg-indigo-600 hover:bg-indigo-700` — one shade darker
- Cards: `hover:shadow-md` — shadow lift (no background change)
- Nav items: `hover:bg-gray-100` — subtle background tint
- Icon buttons: `text-gray-400 hover:text-gray-600 hover:bg-gray-100` — color + tint

**What NOT to change on hover:**
- Size or scale (unless it's a card or tile with clear affordance)
- Layout or position of surrounding elements
- Border-radius (inconsistent and jarring)
- Font weight (causes layout shift)

```tsx
// Correct — one change, purposeful
<a className="text-gray-600 hover:text-gray-900 transition-colors">Link</a>

// Wrong — too many changes
<a className="text-blue-500 hover:text-blue-800 hover:bg-blue-50 hover:scale-105 hover:font-bold transition-all">Link</a>
```

---

## Focus States

Keyboard focus rings are required. Never `outline-none` without a replacement.

**Default pattern:** `focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-600 focus-visible:ring-offset-2`

Use `focus-visible` (not `focus`) so mouse users don't see rings on click — keyboard users always do.

```tsx
// Always include on interactive elements
<button className="... focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-600 focus-visible:ring-offset-2">

// On dark backgrounds, offset creates contrast:
<button className="... focus-visible:ring-white focus-visible:ring-offset-2 focus-visible:ring-offset-indigo-700">
```

Never remove focus rings in global CSS with `* { outline: none }`. If the design calls for a custom ring, provide one — don't remove the default and leave nothing.

---

## Transition Durations

Three tiers. Match duration to the spatial scale of the change.

| Tier | Duration | Use |
|------|----------|-----|
| Micro | `150ms` | Color, background, border, opacity |
| Medium | `250ms` | Size changes, shadow shifts, opacity fades |
| Large | `400ms` | Panel slides, modal enter/exit, page transitions |

Default easing: `ease-out` for enter (starts fast, decelerates into place), `ease-in` for exit (starts slow, accelerates out).

```tsx
// Tailwind duration classes
transition-colors          // 150ms (Tailwind default for colors)
transition-shadow          // 150ms
duration-150               // explicit micro
duration-200               // light medium
duration-300               // standard medium
duration-400               // large (custom — add to tailwind.config)
```

Tailwind's `transition` shorthand defaults to 150ms. Set `duration-*` explicitly when deviating.

```ts
// tailwind.config.ts — add 400ms tier
theme: {
  extend: {
    transitionDuration: {
      '400': '400ms',
    }
  }
}
```

---

## Easing Curves

**Default:** `ease-out` (`cubic-bezier(0, 0, 0.2, 1)`) — use for 90% of transitions.

**Enter:** `ease-out`. Element decelerates into its resting position. Feels responsive.

**Exit:** `ease-in` (`cubic-bezier(0.4, 0, 1, 1)`). Element accelerates out. Feels intentional.

**Symmetric fade:** `ease-in-out` for opacity fades where enter/exit are equivalent.

**When to use spring:** Only for playful, physical interactions where overshoot communicates energy — drag and drop, a character bouncing in, a notification that "pops." In React, reach for Framer Motion's `spring` type. Do not use spring on form validation errors, modals, or navigation — it slows down task-oriented UI.

```tsx
// Framer Motion spring — use sparingly
<motion.div
  initial={{ scale: 0.8, opacity: 0 }}
  animate={{ scale: 1, opacity: 1 }}
  transition={{ type: 'spring', stiffness: 300, damping: 25 }}
/>

// Standard ease-out enter — default
<motion.div
  initial={{ opacity: 0, y: 8 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.2, ease: 'easeOut' }}
/>
```

---

## Micro-animations

Small, purposeful. Each one must answer: what state just changed?

### Button Press

Communicate "click registered" with a brief scale-down.

```tsx
<button className="active:scale-95 transition-transform duration-75">
  Submit
</button>
```

75ms feels instant and physical. Don't go lower — it becomes imperceptible.

### Toast Enter / Exit

Slide in from the bottom (or top-right for notification toasts), fade out.

```tsx
// With Framer Motion
<AnimatePresence>
  {visible && (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 8 }}
      transition={{ duration: 0.2, ease: 'easeOut' }}
      className="fixed bottom-4 left-1/2 -translate-x-1/2 bg-gray-900 text-white text-sm px-4 py-2 rounded-lg shadow-lg"
    >
      {message}
    </motion.div>
  )}
</AnimatePresence>
```

Exit is faster than enter (150ms vs 200ms) — the UI shouldn't wait for you to leave.

### Skeleton Loading

Pulse communicates "content is coming." Use `animate-pulse` from Tailwind. Match the real content layout.

```tsx
// One skeleton per content type — match the grid/list you're replacing
<div className="space-y-3 animate-pulse">
  <div className="flex items-center gap-3">
    <div className="w-10 h-10 bg-gray-200 rounded-full" />
    <div className="flex-1 space-y-2">
      <div className="h-3 bg-gray-200 rounded w-1/3" />
      <div className="h-3 bg-gray-200 rounded w-1/2" />
    </div>
  </div>
</div>
```

Don't use a spinner when you know the content shape. Skeleton is always preferred — it holds layout and sets expectations.

### Dropdown / Popover Open

Scale in from the origin point (anchor element), fade.

```tsx
<motion.div
  initial={{ opacity: 0, scale: 0.95, y: -4 }}
  animate={{ opacity: 1, scale: 1, y: 0 }}
  exit={{ opacity: 0, scale: 0.95, y: -4 }}
  transition={{ duration: 0.15, ease: 'easeOut' }}
  className="absolute top-full mt-1 w-48 bg-white rounded-lg border border-gray-200 shadow-lg py-1"
>
```

`transformOrigin` should match where the dropdown originates — `origin-top-left` for left-anchored, `origin-top-right` for right-anchored.

---

## When to Reach for the Animation Studio Skill

This file covers UI state transitions. Use the `animation-studio` skill instead when:

- The animation is **decorative** (hero sections, loaders, background motion, lottie)
- You're building **cinematic sequences** or timeline-based motion
- The work involves **Remotion**, **GSAP**, **Three.js**, or frame-by-frame control
- You need **scroll-driven** animations beyond simple intersection observer fades
- The motion is **the product** (onboarding animations, product demos, marketing videos)

Rule of thumb: if it's a state transition on a user action, it lives here. If it tells a story or plays without user input, use `animation-studio`.
