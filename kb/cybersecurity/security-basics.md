# Cybersecurity — basics (mentor-curated seed, round 1)

Defensive and educational security fundamentals. For authorised testing, CTFs and learning only.

## Core principles
- CIA triad: Confidentiality, Integrity, Availability — the goals security protects.
- Defence in depth: layer controls so one failure doesn't breach everything.
- Least privilege: give each user/process only the access it needs.
- Zero trust: never trust by network location; verify every request.
- Assume breach: plan detection and response, not just prevention.

## Network & protocols
- TCP/IP layers; common ports: 80/443 HTTP(S), 22 SSH, 53 DNS, 25/465/587 SMTP, 3389 RDP.
- Always prefer encrypted protocols (HTTPS, SSH, TLS) over plaintext (HTTP, Telnet, FTP).
- Firewalls filter traffic; segment networks; VPNs tunnel traffic over untrusted links.

## OWASP Top 10 (web app risks; 2021 list, 2025 released)
- Broken access control; cryptographic failures; injection (incl. SQL, XSS); insecure design;
  security misconfiguration; vulnerable/outdated components; identification & authentication failures;
  software & data integrity failures; security logging & monitoring failures; server-side request forgery (SSRF).

## Encryption
- Symmetric (AES) uses one shared key; asymmetric (RSA, ECC) uses a public/private key pair.
- Hashing (SHA-256) is one-way, for integrity; passwords use slow salted hashes (bcrypt, argon2), never plain SHA.
- TLS combines asymmetric key exchange with symmetric session encryption.

## Common attacks & defences
- Phishing/social engineering: the top breach vector; defend with training, MFA, email filtering, verification of requests.
- Brute force / credential stuffing: defend with rate limiting, lockouts, MFA, and breached-password checks.
- Malware/ransomware: patch, restrict execution, back up offline, segment.
- Keep systems patched; most breaches exploit known, unpatched issues.

## Good practice
- Multi-factor authentication everywhere; a password manager; unique long passwords.
- Log and monitor; have an incident response plan; practise least-privilege and backups.
- Only test systems you own or are explicitly authorised to test.

## Sources (authoritative)
- OWASP Top 10 — https://owasp.org/www-project-top-ten/
- NIST Cybersecurity Framework — https://www.nist.gov/cyberframework
- CISA — https://www.cisa.gov/
- MITRE ATT&CK — https://attack.mitre.org/
- OWASP Cheat Sheet Series — https://cheatsheetseries.owasp.org/
