# PRODUCT build — the calm baseline

Source: ibelick/ui-skills `baseline-ui` (MIT). Use when `llllloc:task-design` set the visitor mode to OPERATE or READ: app screens, dashboards, tools, forms, settings, admin views. The goal: the tool disappears into the task. The look rules (gradients, glow, one accent) live in `llllloc:task-design` RULE 11. This file holds the build rules.

Change from the source: the stack rules apply only when the project already uses that stack. A new standalone page follows the project's stack or plain HTML, CSS and JS.

## Stack (when the project uses it)

- Tailwind project: use Tailwind defaults unless custom values exist or are asked for. Use a `cn` helper (`clsx` plus `tailwind-merge`) for class logic. `tw-animate-css` for small entrances.
- JS animation in React: `motion/react` (formerly `framer-motion`).
- Keyboard or focus behavior: use accessible primitives (Base UI, React Aria, Radix). Use the project's own primitives first. Never mix two primitive systems in one interaction. Never rebuild keyboard or focus logic by hand unless asked.

## Components and interaction

- Icon-only buttons get an `aria-label`.
- Destructive or permanent actions use an alert dialog.
- Loading uses skeletons shaped like the real content.
- Use `100dvh`, never `100vh` (`h-dvh`, never `h-screen`). `dvh` follows the real visible screen on phones.
- Fixed elements respect `env(safe-area-inset-*)`.
- Errors appear next to the action that caused them.
- Never block paste in an input.
- Empty states give one clear next action.

## Motion

- No decorative animation unless asked.
- Animate only `transform` and `opacity`. Never width, height, top, left, margin or padding.
- Avoid animating color or background, except small local items (text, icons).
- `ease-out` on entrance. No custom easing curves unless asked.
- Interaction feedback: 200ms or less.
- Pause loops when off screen. Respect `prefers-reduced-motion`.
- Never animate large images, full-screen surfaces, or a large `blur()` or `backdrop-filter`.
- `will-change` only during an active animation.

## Type

- Headings: `text-wrap: balance`. Body: `text-wrap: pretty`.
- Numbers in data: `font-variant-numeric: tabular-nums`.
- Dense UI: truncate or line-clamp, with the full value reachable (tooltip or detail view).
- Never change letter spacing unless asked.

## Layout

- One fixed `z-index` scale. No random values.
- Square items: one size value (`size-*`), not separate width and height.

## React note

- Never use `useEffect` for anything render logic can express.
