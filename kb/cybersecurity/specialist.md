# Cybersecurity — specialist layer (precise, current facts)

The exact details and the dangerously-wrong defaults models repeat.

## Password & secret storage
- Use **argon2id** (memory-hard; sensible params e.g. 19 MiB, t=2, p=1 as a starting point, tune up) or bcrypt
  (cost ≥ 10–12) or scrypt. Salt is per-password and stored alongside; a pepper is an extra app-side secret.
- **Never** MD5, SHA-1, or a bare/unsalted SHA-256 for passwords — they're fast, so they're brute-forceable. "We
  SHA-256 our passwords" is a red flag, not reassurance.
- Store API keys/tokens hashed too; compare secrets in constant time to avoid timing attacks.

## Transport & tokens
- Prefer **TLS 1.3**; disable TLS 1.0/1.1 and SSLv3. Enable HSTS. Certificate pinning helps but can brick clients on
  rotation — pin to a CA/backup key, not a single leaf.
- JWT pitfalls: reject `alg: none`; don't accept the client's chosen algorithm (algorithm-confusion attack); keep
  tokens short-lived; storing JWTs in `localStorage` exposes them to XSS — prefer httpOnly cookies + CSRF defence.

## Web app specifics
- **SSRF** targets cloud metadata at `http://169.254.169.254/` — block link-local/private egress and use IMDSv2.
- XSS types: stored, reflected, DOM-based; defence is context-aware output encoding + CSP, not input blacklisting.
- IDOR/broken access control is the #1 OWASP 2021 risk — authorise every object access server-side; an unguessable ID
  is not authorisation.
- CSRF: SameSite cookies + anti-CSRF tokens for state-changing requests.

## Operations
- Most breaches exploit **known, unpatched** vulnerabilities and phishing — patching + MFA beat exotic defences.
- Logging must capture auth events and be tamper-evident; detection + response (NIST SP 800-61 lifecycle) matters as
  much as prevention. Assume breach; least privilege; segment.

## Misconceptions to reject
- "HTTPS means the site is safe" — it means the transport is encrypted, nothing about the site's trustworthiness.
- "We're too small to target" — automated scanning hits everyone. "Antivirus is enough" — it isn't.

## Sources
- OWASP Top 10 / ASVS / Cheat Sheets — https://owasp.org/ ; NIST SP 800-63B (passwords), SP 800-61 (IR).
- OWASP JWT & SSRF cheat sheets for the exact guidance.
