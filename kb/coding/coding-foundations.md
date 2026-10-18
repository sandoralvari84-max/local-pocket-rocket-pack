# Programming — foundations (mentor-curated seed, round 1)

Curated starting reference. Facts are from the sources listed at the end. Refine and add language/stack specifics later.

## Clean code principles
- Names should reveal intent; prefer clear over clever. Small functions that do one thing.
- DRY (Don't Repeat Yourself): remove duplicated logic into one place.
- KISS / YAGNI: keep it simple; don't build what you don't yet need.
- Separation of concerns; a module should have one reason to change.
- SOLID (OO design): Single responsibility, Open/closed, Liskov substitution, Interface segregation, Dependency inversion.

## Python style (PEP 8)
- 4 spaces per indent, no tabs; limit lines to 79 chars (comments/docstrings 72).
- Naming: `CapWords` for classes, `lower_snake_case` for functions and variables, `UPPER_SNAKE` for constants.
- Avoid single-char names l, O, I. One statement per line. Use docstrings for public modules/functions/classes.

## JavaScript basics
- Prefer `const`, then `let`; avoid `var`. Use `===`/`!==` (strict equality), not `==`.
- Understand async: callbacks → Promises → async/await; don't block the event loop.
- Keep functions pure where possible; avoid mutating shared state.

## Version control (Git)
- Commit small, logical changes with clear messages (imperative mood: "Add X", "Fix Y").
- Branch per feature/fix; open a pull request for review; never rewrite shared history.
- Don't commit secrets or large build artefacts; use `.gitignore`.

## Testing
- Test behaviour, not implementation. Arrange–Act–Assert structure.
- Pyramid: many fast unit tests, fewer integration tests, few end-to-end tests.
- Cover edge cases and error paths, not only the happy path; a bug fix gets a regression test.

## Complexity & performance
- Big-O describes how cost grows with input size: O(1) < O(log n) < O(n) < O(n log n) < O(n^2).
- Choose the right data structure (hash map for lookups, etc.) before micro-optimising.
- Measure before optimising; optimise the proven bottleneck, not a guess.

## Security basics
- Never trust input: validate and sanitise. Use parameterised queries (no string-built SQL).
- Don't hardcode secrets; load from environment or a secrets store.
- Encode output for its context to prevent injection/XSS; keep dependencies updated.

## Sources (authoritative)
- Python docs — https://docs.python.org/3/
- PEP 8 Style Guide — https://peps.python.org/pep-0008/
- MDN JavaScript — https://developer.mozilla.org/en-US/docs/Web/JavaScript
- Git documentation — https://git-scm.com/doc
- OWASP (web security) — https://owasp.org/www-project-top-ten/
