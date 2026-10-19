# Cybersecurity — expert reasoning layer (how a security expert thinks)

Security reasoning is risk reasoning: likelihood × impact, under an attacker who is adaptive. Teach the method, not a
checklist. The expert asks "what is the attacker's cheapest path?" before reaching for the fanciest control.

## Threat-modelling method (the core skill)
- Start from assets and trust boundaries: what is worth stealing/breaking, and where does untrusted data cross into trusted code?
- Enumerate by STRIDE (spoofing, tampering, repudiation, info-disclosure, DoS, elevation) at each boundary — but prune to what is plausible for THIS system and THIS attacker, not every theoretical threat.
- Rank by risk = likelihood × impact, not by how scary it sounds. A likely medium beats an exotic critical.
- Prefer eliminating the class (parameterised queries kill SQLi) over patching the instance.

### Worked case — "is this login endpoint safe?"
- Boundaries: the form takes untrusted input; it reads from the user DB; it issues a session token.
- Cheapest attacker paths first: credential stuffing (reused passwords), not a 0-day. So: rate-limit + lockout + breached-password check + MFA beat an exotic crypto worry.
- Then injection (parameterise), then session fixation (rotate token on login), then timing oracles (constant-time compare). Order by cost-to-attacker.
- Verify by trying the attack, not by reading the code: attempt stuffing against a test account and confirm lockout fires.

## Defence-in-depth and least privilege
- Assume any single control fails; the question is what the attacker reaches next. No flat networks, no god-mode service accounts.
- Least privilege is the highest-leverage habit: a compromised component should reach almost nothing. Scope tokens, segment networks, separate duties.
- Secrets belong in a manager, never in code or images. Rotate on exposure; assume anything logged is leaked.

## Incident reasoning
- Contain before you clean: stop the bleeding (isolate host, revoke token) before forensics, but preserve evidence.
- Assume the first indicator is not the whole story; find initial access and lateral movement, not just the alert that fired.
- "We patched the box" is not "we understand how they got in." Root-cause or it recurs.

## The meta-rule
There is no "secure", only "secure enough against this threat model at acceptable cost." An expert states the threat model
and the residual risk explicitly. Security theatre is spending on controls that do not move the risk; name the risk each control buys down.
