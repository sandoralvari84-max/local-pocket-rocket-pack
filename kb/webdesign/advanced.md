# Front-end — advanced / academic layer (mentor-curated, round 2)

Builds on web-fundamentals.md. Deeper mechanisms and current platform features.

## Browser rendering & the critical rendering path
- Parse HTML → DOM; parse CSS → CSSOM; combine → render tree; layout (reflow) → paint → composite.
- Layout is expensive; changing geometry triggers reflow, style-only changes trigger repaint; transforms/opacity can be composited on the GPU (cheapest).
- Render-blocking resources: CSS in `head`, synchronous scripts. Defer/async scripts; inline critical CSS; preconnect/preload key resources.

## CSS architecture
- The cascade resolves conflicts by origin/importance, then specificity (inline > id > class/attr/pseudo-class > element), then source order.
- `@layer` (cascade layers) gives explicit ordering independent of specificity; `:where()` has zero specificity for low-weight resets.
- Modern layout: Grid (incl. `grid-template-areas`, `subgrid`), Flexbox, container queries (`@container`), logical properties (`margin-inline`), `clamp()` for fluid type.
- Design tokens via custom properties; prefer `rem`/`ch`/`fr`; `color-mix()` and relative color syntax for systematic palettes.

## Accessibility, in depth
- WCAG is organised as principles (POUR) → guidelines → success criteria at levels A/AA/AAA; AA is the common legal/target bar.
- Accessible name computation: name comes from content, `aria-label`, `aria-labelledby`, or associated `label`; test with an accessibility tree inspector.
- Follow the ARIA Authoring Practices (APG) for widget patterns (combobox, dialog, tabs); manage focus explicitly for modals and SPA route changes; use `aria-live` for dynamic updates.

## Architecture & rendering strategies
- Component model with explicit state; unidirectional data flow; separate server state (caching, revalidation) from UI state.
- CSR vs SSR vs SSG vs ISR vs streaming/islands: trade-offs in TTFB, interactivity (hydration cost), SEO and cache-ability.
- Bundle discipline: code splitting, tree shaking, lazy loading, HTTP caching (ETag, immutable hashed assets), CDN.

## Security (front-end relevant)
- Content Security Policy (CSP) to mitigate XSS; Subresource Integrity (SRI) for third-party scripts; same-origin policy and CORS; `SameSite` cookies and CSRF tokens; never trust client input.

## Sources (authoritative)
- MDN Web Docs — https://developer.mozilla.org/
- web.dev — https://web.dev/
- WAI-ARIA Authoring Practices Guide — https://www.w3.org/WAI/ARIA/apg/
- WCAG 2.1 — https://www.w3.org/TR/WCAG21/
- HTML living standard — https://html.spec.whatwg.org/
