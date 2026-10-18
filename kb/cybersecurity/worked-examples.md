# Cybersecurity — worked examples (mentor-curated, round 3: reasoning by example)

Method: restate → retrieve facts → reason in steps → check → concise answer. Defensive/authorised context only.

## Example 1 — "Our app shows an order at /orders?id=123. Users can change the number. Is that a problem?"
- Restate: assess whether a user-controlled object ID in the URL is a security risk.
- Facts (advanced.md › Application security): broken access control / IDOR — authorise every object access server-side; obscurity is not access control.
- Steps:
  1. Changing `id=123` to `id=124` requests another record. If the server returns it without checking ownership, that's an Insecure Direct Object Reference (IDOR) — broken access control, #1 in the OWASP Top 10.
  2. The fix is not to hide or encrypt the ID; it is to check on every request that the logged-in user is authorised for that object.
  3. Add server-side authorisation; log and alert on repeated denied access.
- Check: the risk (unauthorised data access) maps to the control (server-side authZ per object); matches the KB.
- Answer: Yes — likely an IDOR. Enforce server-side authorisation so each user can only fetch their own orders; don't rely on the ID being hard to guess.

## Example 2 — "How should we store passwords and stop brute-force logins?"
- Restate: choose password storage and anti-brute-force controls.
- Facts (advanced.md › Applied cryptography, Identity): slow salted KDFs (argon2id/bcrypt/scrypt), never fast/plain hashes; MFA; rate limiting.
- Steps:
  1. Storage: hash with a slow salted KDF (argon2id or bcrypt). Never store plaintext or a bare SHA-256.
  2. Brute force: add per-account and per-IP rate limiting plus temporary lockout/backoff.
  3. Add MFA and check credentials against known-breached-password lists.
- Check: storage (slow salted hash) and online-guessing defences (rate limit + MFA) are separate controls; both present.
- Answer: Store passwords with argon2id or bcrypt (salted, slow). Stop brute force with rate limiting, lockout/backoff, and MFA; reject breached passwords.
