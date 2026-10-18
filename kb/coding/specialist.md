# Coding — specialist layer (cross-language traps models get wrong)

Advanced, cross-cutting facts and the confident-but-wrong answers to watch for. (Language-specific depth is in the paid pack.)

## Numbers & encoding
- Floating point is IEEE-754: `0.1 + 0.2 != 0.3` in almost every language. Never compare floats with `==`; never use
  floats for money — use integers (cents) or a decimal type.
- Integer overflow is silent in C/C++/Rust-release/Go; Python has bignums (no overflow); JS numbers lose integer
  precision above 2^53 (use BigInt).
- Strings are Unicode: `len` may count code units, code points, or bytes depending on language. "Reverse a string"
  breaks on emoji/combining characters. Normalise (NFC) before comparing user text.

## Time — a reliable bug source
- Store and compute in UTC; convert to local only for display. A "date" without a timezone is ambiguous.
- Daylight-saving transitions mean some local times don't exist or exist twice; day length isn't always 24h.
- Unix timestamps are seconds (or ms in JS) since 1970 UTC; don't do date math by adding 86400.

## Complexity the model misstates
- `x in list` / array `includes` is **O(n)**; set/dict/hash membership is avg **O(1)**. Dictionary ordered-insertion
  is guaranteed in Python 3.7+ but that's language-specific, not universal.
- "Amortised O(1)" (dynamic array append) is not the same as worst-case O(1) — an individual resize is O(n).
- Recursion without memoisation on overlapping subproblems is exponential (naive Fibonacci is O(2^n)).

## Concurrency
- A data race needs no "visible" interleaving to corrupt state; `count += 1` is read-modify-write, not atomic.
- "Exactly-once delivery" across a network is impossible; design for **at-least-once + idempotency**.
- Double-checked locking is subtly broken without proper memory barriers/`volatile`/atomics.

## Security defaults models get wrong
- Never build SQL/shell/HTML by string concatenation — parameterise / use safe builders. Don't parse HTML with regex.
- Password storage is argon2id/bcrypt/scrypt (salted, slow), **never** MD5/SHA-1/plain SHA-256.
- Validate input server-side; client validation is UX, not security.

## Sources
- "What Every Computer Scientist Should Know About Floating-Point"; CLRS for complexity.
- OWASP Cheat Sheets — https://cheatsheetseries.owasp.org/ ; language docs for exact semantics.
