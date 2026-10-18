# Cybersecurity — advanced / academic layer (mentor-curated, round 2)

Builds on security-basics.md. Defensive, secure-design and authorised-testing depth only.

## Applied cryptography
- Symmetric: AES (modes — GCM provides authenticated encryption; avoid ECB). Keys exchanged via asymmetric methods.
- Asymmetric: RSA, elliptic curve (ECDH/ECDSA, Ed25519). Diffie–Hellman establishes a shared secret over an open channel.
- Integrity/authenticity: cryptographic hashes (SHA-256), MACs/HMAC, and digital signatures (sign with private key, verify with public).
- PKI & TLS: certificates bind identity to a public key via a CA chain; TLS 1.3 handshake does key exchange + authentication, then symmetric session encryption; forward secrecy via ephemeral keys.
- Password storage: slow salted KDFs (argon2id, bcrypt, scrypt) — never plain or fast hashes. Use CSPRNGs; never roll your own crypto.

## Identity & access
- AuthN (who you are) vs AuthZ (what you may do). MFA factors: knowledge, possession, inherence.
- Protocols: OAuth 2.0 (delegated authorization), OpenID Connect (authentication on top), SAML (enterprise SSO).
- Sessions: secure cookies (HttpOnly, Secure, SameSite), rotation, short-lived tokens; principle of least privilege and RBAC/ABAC.

## Threat modelling
- STRIDE (Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege).
- Attack trees; data-flow diagrams and trust boundaries; map techniques to MITRE ATT&CK; rank by likelihood × impact (DREAD-style).

## Application security (depth)
- Injection: parameterise queries/commands; output-encode per context to stop XSS (stored/reflected/DOM); CSRF tokens + SameSite.
- Access control: prevent IDOR by authorising every object access server-side; SSRF defences (allowlist egress, block link-local/metadata).
- Insecure deserialization, SSTI, path traversal; secrets management and key rotation; supply-chain (pin, verify, SBOM).

## Testing & operations
- SAST (static), DAST (dynamic), IAST, fuzzing, dependency scanning; authorised pen-test phases: recon → scanning → exploitation → post-exploitation → reporting (with written scope/authorisation).
- Detection & response: NIST IR lifecycle (prepare, detect & analyse, contain/eradicate/recover, post-incident); centralised logging, SIEM, and alerting.

## Sources (authoritative)
- OWASP Top 10 & Cheat Sheets — https://owasp.org/ ; https://cheatsheetseries.owasp.org/
- NIST (CSF, SP 800-series, IR SP 800-61) — https://csrc.nist.gov/
- MITRE ATT&CK — https://attack.mitre.org/
- NIST password guidance SP 800-63B — https://pages.nist.gov/800-63-3/
