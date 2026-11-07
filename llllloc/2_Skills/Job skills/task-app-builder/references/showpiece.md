# SHOWPIECE build — award-level web tech

Source: Nyx-abu/awwwards-ui-skill (MIT). Use when `llllloc:task-design` set the visitor mode to PERSUADE or EXPERIENCE. The design choices (layout, type, color, spacing, the motion story) live in `llllloc:task-design`. This file is how to build them so they run smooth and fast.

## Contents
1. Source-backed inputs
2. Motion and smooth scroll
3. Custom cursor
4. 3D and depth
5. React and Framer Motion patterns
6. Spring settings
7. Stack fit
8. Performance and security
9. Text safety checklist

## 1. Source-backed inputs

Use these as principles. Never copy their look.
- `motion.zajno.com`: the motion words to use. Easing, offset and delay, fade paired with movement, transform and morph, masking, depth, parallax, zoom continuity.
- `styles.refero.design`: strict tokens, structured type scales, consistent spacing.
- `ui.aceternity.com`, `componentry.fun`: React plus Framer Motion patterns. Bento grids, sticky scroll cards, kinetic text, magnetic docks.
- `recent.design/x`: spring physics for UI feedback.
- Awwwards Directory and Awwwards GSAP tags: the page categories and the tech mix (GSAP, Canvas, Three.js, WebGL, React, Vite).

Motion guides attention. Layout makes hierarchy. Interaction invites exploration. Every piece stays accessible and measurable.

## 2. Motion and smooth scroll

The motion story (the signature moment, the stagger ranges, fade with movement, shape continuity) is decided in `llllloc:task-design` RULE 7. This section builds it.
- Libraries: Lenis or GSAP ScrollTrigger for smooth scroll and scroll reveals. On plain HTML, CSS scroll timelines and IntersectionObserver.
- Easing in code: spatial movement uses a clear cubic-bezier or a spring (section 6). Linear only for spinners, marquees and progress bars.
- Masks and morphs: `clip-path`, SVG masks, FLIP for layout-like moves (`motion-performance.md`, section 3).
- Parallax: move layers by `transform` only, from one `requestAnimationFrame` loop or a scroll timeline. Foreground moves most, background least.
- Variable fonts: animate an axis only when it is the signature, and only on short headings.

## 3. Custom cursor

- Desktop only. Gate with `@media (pointer: fine)`. Off with reduced motion.
- A `position: fixed` div, moved inside one `requestAnimationFrame` loop.
- Magnetic snap or stretch toward interactive items on hover.
- `mix-blend-mode: difference` over high-contrast type or images, when it helps the reveal.
- Never hide the system cursor over inputs or text you can select. Mark the cursor `aria-hidden="true"`.

## 4. 3D and depth

- Use at least two depth techniques (parallax, mask, zoom, layered planes, WebGL), tied to scroll, pointer or viewport. None may shift layout.
- WebGL or Three.js background (particles, fluid noise, shader distortion) only when the subject earns it. A corporate site gets refined type and quiet hovers, not a shader.
- `backdrop-filter: blur()` sparingly, over real depth only. Never animate a large blur.

## 5. React and Framer Motion patterns

- Velocity scroll and marquee: `useScroll` plus `useSpring` plus `useTransform` on x.
- Bento grid: asymmetric cells. Stagger with `initial={{ opacity: 0, y: 20 }}` and `whileInView={{ opacity: 1, y: 0 }}`.
- Sticky scroll cards: `position: sticky` or scroll tracking.
- Kinetic text: per-word or per-letter variants, `staggerChildren: 0.05`.
- Magnetic component: track `onMouseMove`, clamp the x and y offset, return to center on `onMouseLeave`.

## 6. Spring settings

Use springs, not `ease-in-out`, for hover, press and drag in this mode.
- Snappy (cards, modals): `{ type: "spring", stiffness: 300, damping: 20 }`
- Fluid (hover, cursor): `{ type: "spring", stiffness: 150, damping: 15, mass: 0.5 }`
- Heavy (hero reveal): `{ type: "spring", stiffness: 100, damping: 30 }`

## 7. Stack fit

- Next.js: load Three.js and GSAP with dynamic import and `ssr: false`.
- Plain HTML and CSS: CSS `@keyframes`, scroll timelines, IntersectionObserver. No heavy library for a simple reveal.
- Existing site: apply the craft without breaking what works.

## 8. Performance and security

- Lazy-load heavy media: `loading="lazy"` or dynamic import.
- Three.js: call `geometry.dispose()`, `material.dispose()`, `renderer.dispose()` on unmount.
- Scroll and pointer handlers only write values. One `requestAnimationFrame` loop reads them. No layout reads inside handlers.
- Text scramble or SVG morph with user input: sanitize with DOMPurify before `innerHTML`.
- Reduced motion switches off Lenis, Three.js and GSAP:
  ```js
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!reduce) { initAnimations(); }
  ```

## 9. Text safety checklist

- No text element uses `position: absolute` inside a fixed-height box. Use flex and `margin-top: auto`.
- Stacked cards (zoom, carousel, slides): only the active card is visible. Others get `opacity: 0` and a lower `z-index`.
- Every card and panel has at least `1rem` padding. Text never touches an edge.
- Text over color or image has protection: a verified color, a semi-opaque backing, or a shadow.
- Bars and meters inside cards use flex or grid, never `position: absolute` that can clip.
