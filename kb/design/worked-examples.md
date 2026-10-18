# UX design — worked examples (mentor-curated, round 3: reasoning by example)

Each example shows the method: restate → retrieve facts → reason in steps → check → concise answer. Imitate this shape.

## Example 1 — "Our signup form has a high drop-off. How do we improve completion?"
- Restate: reduce abandonment on a signup form using UX principles.
- Facts (ux-foundations.md › heuristics, laws; advanced.md › cognitive load): Hick's Law (fewer choices = faster), Miller's Law (chunk), cognitive load (cut extraneous), error prevention, visibility of system status, recognition over recall.
- Steps:
  1. Count fields; remove every non-essential one (ask for the rest later). Fewer fields = lower load and faster decision (Hick/cognitive load).
  2. Chunk remaining fields into short logical groups; show progress if multi-step (visibility of status).
  3. Prevent errors: inline validation, clear formats, sensible defaults; don't clear the form on error.
  4. Reduce memory burden: show password rules as you type (recognition over recall); allow email autofill.
  5. Make the primary action prominent and singular (Fitts's Law — large, well-placed).
- Check: each change maps to a named principle and to a plausible drop-off cause (too long, confusing, error-prone).
- Answer: Cut fields to the essential few, chunk and show progress, add inline validation with preserved input, surface rules instead of hiding them, and make one prominent submit action. Then A/B test the change.

## Example 2 — "Two navigation designs — a hamburger menu vs a visible tab bar. Which for a mobile app's main sections?"
- Restate: choose a primary navigation pattern for frequently-used mobile sections.
- Facts (foundations › heuristics; advanced › Fitts, recognition): recognition over recall; Fitts's Law (reachable, large targets); Jakob's Law (match platform conventions).
- Steps:
  1. Main sections are used often → they should be visible, not hidden behind a menu (recognition over recall; hidden nav lowers discovery/engagement).
  2. A bottom tab bar keeps 3–5 top destinations one tap away in the thumb zone (Fitts's Law).
  3. Hamburger is fine for secondary/rare items; matches conventions when sections are many/infrequent (Jakob's Law).
- Check: recommendation follows from frequency of use + reachability + convention; not just aesthetic preference.
- Answer: Use a visible bottom tab bar for the 3–5 main sections (visible, thumb-reachable, higher discovery); reserve the hamburger for secondary items. If there are more than ~5 top-level sections, reconsider the information architecture.
