# Web design — worked examples (mentor-curated, round 3: reasoning by example)

Each example shows the method: restate → retrieve facts → reason in steps → check → concise answer. Imitate this shape.

## Example 1 — "The page feels slow and jumps around as it loads. What's wrong and how do I fix it?"
- Restate: diagnose poor loading experience and fix it.
- Facts (web-fundamentals.md › Core Web Vitals): LCP < 2.5 s (main content), CLS < 0.1 (visual stability — set width/height on images/ads), INP < 200 ms; compress & lazy-load images, defer JS.
- Steps:
  1. "Jumps around" = high CLS. Most common cause: images/embeds with no reserved space. Fix: set explicit `width`/`height` (or `aspect-ratio`) so the browser reserves the box.
  2. "Feels slow" to first paint = high LCP. Fix: identify the LCP element (usually the hero image/heading), `preload` it, serve a modern compressed format (WebP/AVIF), and don't lazy-load the above-the-fold image.
  3. Sluggish on interaction = high INP. Fix: defer/split non-critical JavaScript; avoid long tasks on the main thread.
- Check: each fix maps to one vital (CLS→dimensions, LCP→preload/compress, INP→defer JS); consistent with the KB.
- Answer: Reserve image dimensions to stop the shifting (CLS), preload and compress the hero image and don't lazy-load it (LCP), and defer non-critical JS (INP). Measure before/after with the Core Web Vitals.

## Example 2 — "Is this clickable card accessible?"
- Restate: check a card component against accessibility basics.
- Facts (web-fundamentals.md › Semantic HTML, Accessibility; advanced.md › Accessibility): use `a`/`button` for the action not a `div`; meaningful `alt`; contrast ≥ 4.5:1 normal text; keyboard operable with visible focus; don't rely on colour alone.
- Steps:
  1. Is the whole card a real link/button? If it's a `div` with onclick, it's not keyboard-focusable → replace with `a`/`button` or add proper role + tabindex + key handlers (prefer native).
  2. Does the image have a purposeful `alt` (or empty `alt` if decorative)?
  3. Text contrast ≥ 4.5:1? Focus state visible on tab?
  4. Is any meaning carried by colour alone (e.g. "red = sold out")? Add text/icon.
- Check: covers perceivable (alt, contrast), operable (keyboard, focus), robust (native elements) — the POUR spine.
- Answer: It's accessible only if the action is a native `a`/`button`, the image has correct `alt`, text meets 4.5:1, focus is visible, and no meaning is colour-only. Flag whichever fails.
