# Components

Default stack: React + TypeScript + Tailwind. Match existing project conventions first.

---

## Buttons

Three variants. One size default (`md`). Disabled always via `disabled` prop, never opacity alone.

```tsx
// Primary — one per view section
<button className="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-lg hover:bg-indigo-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-600 focus-visible:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors">
  Save changes
</button>

// Secondary — supporting actions
<button className="inline-flex items-center gap-2 px-4 py-2 bg-white text-gray-700 text-sm font-medium rounded-lg border border-gray-300 hover:bg-gray-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-600 focus-visible:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors">
  Cancel
</button>

// Tertiary/ghost — low-emphasis actions
<button className="inline-flex items-center gap-2 px-4 py-2 text-indigo-600 text-sm font-medium rounded-lg hover:bg-indigo-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-600 focus-visible:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors">
  Learn more
</button>

// Icon button — use aria-label, no text
<button aria-label="Close" className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-600 transition-colors">
  <XIcon className="w-4 h-4" />
</button>
```

**Sizes:** `sm` → `px-3 py-1.5 text-xs`, `md` → `px-4 py-2 text-sm`, `lg` → `px-5 py-2.5 text-base`.

**Destructive variant:** Same structure as primary but `bg-red-600 hover:bg-red-700 focus-visible:ring-red-600`.

---

## Forms

Label above input. Error below. Hint below label when present.

```tsx
// Text input
<div className="space-y-1">
  <label htmlFor="email" className="block text-sm font-medium text-gray-700">
    Email address
  </label>
  <p className="text-xs text-gray-500">We'll never share your email.</p>  {/* hint — optional */}
  <input
    id="email"
    type="email"
    className="block w-full px-3 py-2 text-sm border border-gray-300 rounded-lg bg-white text-gray-900 placeholder:text-gray-400
      focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-transparent
      aria-invalid:border-red-500 aria-invalid:ring-red-500
      disabled:bg-gray-50 disabled:text-gray-500 disabled:cursor-not-allowed
      transition-shadow"
    aria-describedby="email-error"
  />
  {/* error */}
  <p id="email-error" className="text-xs text-red-600" role="alert">
    Please enter a valid email address.
  </p>
</div>
```

```tsx
// Select
<select className="block w-full px-3 py-2 text-sm border border-gray-300 rounded-lg bg-white text-gray-900
  focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-transparent
  disabled:bg-gray-50 disabled:cursor-not-allowed">
  <option value="">Choose an option</option>
  <option value="a">Option A</option>
</select>

// Textarea — same classes as input, add resize-y
<textarea className="block w-full px-3 py-2 text-sm border border-gray-300 rounded-lg bg-white text-gray-900 placeholder:text-gray-400 resize-y min-h-[100px]
  focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-transparent" />
```

Error state is communicated via `aria-invalid="true"` on the input and `aria-describedby` linking to the error message. Never rely on color alone.

---

## Cards

Content card is the workhorse. Hover state lifts the shadow, never changes the background.

```tsx
<div className="bg-white rounded-xl border border-gray-200 p-6 hover:shadow-md transition-shadow">
  <div className="flex items-start justify-between gap-4">
    <div>
      <h3 className="text-base font-semibold text-gray-900">Card title</h3>
      <p className="text-sm text-gray-500 mt-1">Supporting description text goes here.</p>
    </div>
    <span className="shrink-0 text-xs font-medium text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded-full">
      Badge
    </span>
  </div>
  <div className="mt-4 pt-4 border-t border-gray-100 flex items-center justify-between">
    <span className="text-xs text-gray-400">Updated 3 hours ago</span>
    <button className="text-sm font-medium text-indigo-600 hover:text-indigo-700">View →</button>
  </div>
</div>
```

Clickable card: wrap in `<a>` or add `role="button"`, move hover/focus to the outer element. Don't nest interactive elements inside a clickable card.

---

## Navigation

### Top Nav

```tsx
<header className="sticky top-0 z-40 bg-white border-b border-gray-200">
  <nav className="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between gap-8">
    <a href="/" className="text-lg font-bold text-gray-900 shrink-0">Logo</a>
    <ul className="hidden md:flex items-center gap-1">
      {links.map(link => (
        <li key={link.href}>
          <a href={link.href}
            className="px-3 py-2 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors aria-[current=page]:text-indigo-600 aria-[current=page]:bg-indigo-50">
            {link.label}
          </a>
        </li>
      ))}
    </ul>
    <div className="flex items-center gap-2">
      {/* auth buttons or avatar */}
    </div>
  </nav>
</header>
```

### Side Nav

```tsx
<aside className="w-56 shrink-0 flex flex-col gap-1 py-4">
  {sections.map(section => (
    <div key={section.label}>
      <p className="px-3 mb-1 text-xs font-semibold text-gray-400 uppercase tracking-wide">
        {section.label}
      </p>
      {section.links.map(link => (
        <a key={link.href} href={link.href}
          className="flex items-center gap-2.5 px-3 py-2 text-sm text-gray-700 rounded-lg hover:bg-gray-100 hover:text-gray-900 transition-colors aria-[current=page]:bg-indigo-50 aria-[current=page]:text-indigo-700 aria-[current=page]:font-medium">
          <link.icon className="w-4 h-4 shrink-0" />
          {link.label}
        </a>
      ))}
    </div>
  ))}
</aside>
```

### Breadcrumb

```tsx
<nav aria-label="Breadcrumb">
  <ol className="flex items-center gap-1 text-sm text-gray-500">
    {crumbs.map((crumb, i) => (
      <li key={crumb.href} className="flex items-center gap-1">
        {i > 0 && <span className="text-gray-300">/</span>}
        {i < crumbs.length - 1
          ? <a href={crumb.href} className="hover:text-gray-900 transition-colors">{crumb.label}</a>
          : <span className="text-gray-900 font-medium" aria-current="page">{crumb.label}</span>
        }
      </li>
    ))}
  </ol>
</nav>
```

---

## Modals / Dialogs

Use the native `<dialog>` element or a headless library (Radix `Dialog`, Headless UI `Dialog`). Never roll your own focus trap.

```tsx
// Using Radix Dialog as reference pattern
import * as Dialog from '@radix-ui/react-dialog'

<Dialog.Root open={open} onOpenChange={setOpen}>
  <Dialog.Portal>
    <Dialog.Overlay className="fixed inset-0 bg-black/40 backdrop-blur-sm data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0" />
    <Dialog.Content className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-lg bg-white rounded-xl shadow-xl p-6
      data-[state=open]:animate-in data-[state=closed]:animate-out
      data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0
      data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95
      focus:outline-none">
      <div className="flex items-start justify-between gap-4 mb-4">
        <Dialog.Title className="text-lg font-semibold text-gray-900">
          Dialog title
        </Dialog.Title>
        <Dialog.Close className="p-1.5 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100 transition-colors">
          <XIcon className="w-4 h-4" />
        </Dialog.Close>
      </div>
      <Dialog.Description className="text-sm text-gray-600 mb-6">
        Supporting description.
      </Dialog.Description>
      {/* content */}
      <div className="flex justify-end gap-2 mt-6">
        <Dialog.Close asChild>
          <button className={secondaryBtn}>Cancel</button>
        </Dialog.Close>
        <button className={primaryBtn}>Confirm</button>
      </div>
    </Dialog.Content>
  </Dialog.Portal>
</Dialog.Root>
```

Rules: always include a visible close button, always allow `Escape` to close, focus must return to the trigger element on close.

---

## Empty / Loading / Error States

Every data-dependent view needs all three. Design them first, not as an afterthought.

```tsx
// Empty state
<div className="flex flex-col items-center justify-center py-16 text-center">
  <div className="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center mb-4">
    <InboxIcon className="w-6 h-6 text-gray-400" />
  </div>
  <h3 className="text-base font-semibold text-gray-900">No results found</h3>
  <p className="text-sm text-gray-500 mt-1 max-w-xs">
    Try adjusting your filters or add a new item to get started.
  </p>
  <button className={primaryBtn + " mt-4"}>Add item</button>
</div>

// Skeleton loading — match the shape of real content
<div className="animate-pulse space-y-3">
  <div className="h-4 bg-gray-200 rounded w-3/4" />
  <div className="h-4 bg-gray-200 rounded w-1/2" />
  <div className="h-4 bg-gray-200 rounded w-5/6" />
</div>

// Error state
<div className="rounded-lg border border-red-200 bg-red-50 p-4 flex gap-3">
  <AlertCircleIcon className="w-5 h-5 text-red-500 shrink-0 mt-0.5" />
  <div>
    <p className="text-sm font-medium text-red-800">Something went wrong</p>
    <p className="text-sm text-red-700 mt-0.5">
      Unable to load your data. <button className="underline hover:no-underline" onClick={retry}>Try again</button>
    </p>
  </div>
</div>
```

Skeleton shapes must mirror the real content layout — don't show a single bar when the real content is a grid of cards.
