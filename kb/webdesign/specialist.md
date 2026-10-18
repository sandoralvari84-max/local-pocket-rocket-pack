# Web design — specialist layer (precise facts models get wrong)

Depth beyond the basics: exact specifics, recent changes, and the misconceptions models repeat confidently.

## Core Web Vitals — the details that matter
- **INP replaced FID in March 2024** as a Core Web Vital. A model trained earlier will say FID — it's wrong now.
  Good INP < 200 ms, needs-work 200–500, poor > 500.
- Vitals are judged at the **75th percentile of real field data (CrUX)**, not lab averages. A good lab score with a
  bad p75 still fails. LCP good < 2.5 s, CLS good < 0.1.
- Lazy-loading the **LCP image hurts** LCP — never `loading="lazy"` above the fold. Preload it instead.

## CSS the model misremembers
- Specificity is (inline, id, class/attr/pseudo-class, element) compared left-to-right — it is **not** additive across
  columns (11 classes never beat 1 id). `!important` and inline are separate, higher tiers.
- `:where()` has **zero** specificity; `:is()` takes the specificity of its most specific argument. Cascade layers
  (`@layer`) override specificity by layer order entirely.
- Flexbox: items have `min-width: auto` by default, so a flex child **won't shrink below its content** unless you set
  `min-width: 0` — the classic "my flex item overflows" bug.
- Modern, now baseline: container queries (`@container`), `:has()` (parent selector), `aspect-ratio`, `clamp()`,
  subgrid, logical properties. Check caniuse for the user's target, but these are widely supported as of 2024–25.

## Accessibility specifics
- Accessible name precedence: `aria-labelledby` > `aria-label` > associated `<label>`/content > `title`. Don't stack them.
- `aria-hidden="true"` on a focusable element is a trap — it hides it from screen readers but it's still tabbable.
- Prefer native elements; "no ARIA is better than bad ARIA." `role="button"` on a `<div>` also needs tabindex + key
  handlers + `aria-pressed` where relevant — a real `<button>` gives all that free.
- Contrast 4.5:1 normal / 3:1 large (≥24px, or ≥18.66px bold) and 3:1 for UI components and focus indicators.

## Misconceptions to reject
- "Use px for fonts" — breaks user zoom/preferences; use `rem`. "Set width in px for responsiveness" — use relative units.
- "More `<div>`s are fine" — semantic elements drive accessibility and SEO. "Carousels boost engagement" — they
  usually don't; most users never see slide 2.

## Sources
- web.dev Core Web Vitals — https://web.dev/articles/vitals ; MDN CSS specificity, selectors.
- WAI-ARIA APG — https://www.w3.org/WAI/ARIA/apg/ ; caniuse.com for support.
