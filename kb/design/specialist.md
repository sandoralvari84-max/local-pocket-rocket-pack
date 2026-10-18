# UX design — specialist layer (precise facts and corrected myths)

The exact research facts and the widely-repeated claims that are wrong or oversimplified.

## Research numbers, stated correctly
- Nielsen's "5 users" applies to **qualitative usability discovery per round** (≈5 find ~85% of issues) — NOT to
  quantitative benchmarks or A/B tests, which need larger samples (often 20+ per cell for metrics; thousands for web A/B).
- **Miller's "7±2" is outdated** for working memory. Cowan (2001) puts the limit at **~4 chunks**. Models cite 7±2 as
  gospel — the modern figure is lower. Chunking still helps.
- Iterate: test → fix → retest. One round of 5 is discovery, not proof.

## Effects that are real (and often misattributed)
- **Aesthetic-usability effect**: attractive interfaces are *perceived* as more usable and users forgive minor issues.
- **Peak-end rule**: people judge an experience by its most intense point and its end, not the average.
- **Von Restorff/isolation**: the item that differs is remembered. **Serial position**: first and last items recalled best.
- **Jakob's Law**: users spend most time on *other* sites, so they expect yours to work like them — convention beats novelty.

## Myths to reject
- "Users read pages" — they **scan** (F/Z patterns); front-load meaning. "Three-click rule" — unsupported; success
  depends on whether each click is obviously right, not the count.
- "Carousels/hero sliders boost engagement" — usually not; most users never see slide 2, and they hurt CLS/performance.
- "Hamburger menus are fine for primary nav" — hidden nav lowers discovery/engagement vs visible tabs for key sections.
- "More options = more value" — choice overload (Hick's Law) slows and deters decisions.

## Accessibility & ethics (the serious bits)
- WCAG 2.1/2.2 **AA** is the common legal bar (ADA case law in the US, EN 301 549 / European Accessibility Act in the EU).
  Touch target ≥ 24×24 CSS px (2.2 AA) or 44×44 (AAA).
- Dark patterns (forced continuity, confirmshaming, sneaking) are increasingly **illegal** (GDPR, FTC, EU DSA), not just unethical.

## Sources
- Nielsen Norman Group — https://www.nngroup.com/articles/ ; Cowan (2001) on working-memory capacity.
- WCAG 2.2 — https://www.w3.org/TR/WCAG22/ ; Laws of UX — https://lawsofux.com/
