# Front-end web design & development — fundamentals (mentor-curated seed, round 1)

Curated starting reference. Facts here are from the authoritative sources listed at the end. Refine over later rounds.

## Semantic HTML
- Use elements for their meaning, not their look: `header`, `nav`, `main`, `article`, `section`, `aside`, `footer`.
- One `h1` per page; keep heading levels in order (don't skip from h2 to h4) — screen readers use them to navigate.
- Use `button` for actions and `a` for navigation; never a `div` with a click handler for either.
- Label every form control with `label for=...`; group related controls with `fieldset`/`legend`.
- Give every meaningful image an `alt` describing its purpose; decorative images get empty `alt=""`.

## Responsive, mobile-first layout
- Design for small screens first, then add complexity at wider widths with `min-width` media queries.
- Always include `<meta name="viewport" content="width=device-width, initial-scale=1">`.
- Modern layout uses Flexbox (one-dimensional rows/columns) and CSS Grid (two-dimensional layouts); avoid floats for layout.
- Prefer relative units (`rem`, `%`, `fr`, `ch`) over fixed `px` for text and layout so it scales.
- Test reflow at 320 px wide with no horizontal scrolling (a WCAG requirement).

## Accessibility (a11y) basics — WCAG 2.1 AA
- POUR principles: content must be Perceivable, Operable, Understandable, Robust.
- Colour contrast: at least 4.5:1 for normal text, 3:1 for large text and UI components.
- Everything usable by keyboard alone; visible focus states; logical tab order.
- Use landmarks and ARIA only when native HTML can't express it ("no ARIA is better than bad ARIA").
- Don't rely on colour alone to convey meaning; respect `prefers-reduced-motion`.

## Performance — Core Web Vitals
- LCP (Largest Contentful Paint): main content visible — aim under 2.5 s.
- CLS (Cumulative Layout Shift): visual stability — aim under 0.1 (set width/height on images and ads).
- INP (Interaction to Next Paint): responsiveness to input — aim under 200 ms.
- Compress and lazy-load images, use modern formats (WebP/AVIF), minimise and defer JavaScript.

## Good practice
- Progressive enhancement: a working HTML/CSS baseline first, JavaScript as an enhancement.
- Check browser support for a feature on caniuse.com before relying on it.
- Keep CSS maintainable: consistent naming, design tokens (CSS custom properties) for colour/spacing/type.

## Sources (authoritative)
- MDN Web Docs — https://developer.mozilla.org/en-US/docs/Learn
- web.dev Learn (HTML, CSS, Accessibility, Performance, Forms, Design) — https://web.dev/learn/
- WCAG 2.1 Quick Reference — https://www.w3.org/WAI/WCAG21/quickref/
- Core Web Vitals — https://web.dev/articles/vitals
- Browser support tables — https://caniuse.com/
- HTML living standard — https://html.spec.whatwg.org/
