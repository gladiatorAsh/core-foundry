# Web security

## OWASP Top 10:2025

| # | Category | Example | Key defenses |
|---|---|---|---|
| A01 | **Broken Access Control** | Changing `/orders/123` to `/orders/124` shows someone else's order (IDOR) | Deny by default; check object-level ownership on the server for every request; never trust client-side checks |
| A02 | **Security Misconfiguration** | Debug mode in prod, default credentials, open storage buckets, verbose errors | Hardened defaults, infrastructure as code with policy checks, minimal surface |
| A03 | **Software Supply Chain Failures** (new) | A compromised npm package or build pipeline | Lockfiles, dependency scanning (Dependabot), SBOMs, pinned and signed artifacts, least-privilege CI |
| A04 | **Cryptographic Failures** | Plaintext passwords, weak hashing, HTTP | TLS everywhere; hash passwords with Argon2id/bcrypt/scrypt; encrypt sensitive data at rest; managed keys |
| A05 | **Injection** | SQL injection via string concatenation; command injection | Parameterized queries / ORM; input validation; escape output by context |
| A06 | **Insecure Design** | No rate limit on password reset; business-logic abuse | Threat modeling, abuse cases, secure design patterns |
| A07 | **Authentication Failures** | Credential stuffing, weak session handling | MFA, rate limiting + lockout, secure session management, breached-password checks |
| A08 | **Software or Data Integrity Failures** | Unsigned updates, insecure deserialization | Signature verification, integrity checks, safe deserializers |
| A09 | **Security Logging and Alerting Failures** | Breach undetected for months | Log auth events and access-control failures; alert; protect logs |
| A10 | **Mishandling of Exceptional Conditions** (new) | Error paths that fail open or leak stack traces | Fail closed, handle errors explicitly, generic error messages to users |

Source: [OWASP Top 10](https://owasp.org/Top10/); overview of the 2025 changes from [Qualys](https://blog.qualys.com/qualys-insights/2026/06/15/what-changed-in-owasp-top-10-2025-and-recommendations-for-each-category).

## XSS (cross-site scripting)

- **Stored** (saved in the DB and shown to others), **reflected** (in the URL/request), **DOM-based** (client-side JS writes untrusted data to the DOM).
- Defenses: frameworks escape by default (React escapes text, so avoid `dangerouslySetInnerHTML` or sanitize with DOMPurify);
  context-aware output encoding; **Content Security Policy** (`script-src 'self'` with nonces, no `unsafe-inline`); `HttpOnly` cookies so scripts can't read sessions; Trusted Types.
- **LLM apps:** model output is untrusted. Render Markdown with a sanitizer and never inject raw HTML from a model.

## CSRF (cross-site request forgery)

An attacker's site makes the victim's browser send an authenticated request (cookies attach automatically).
Defenses: **`SameSite=Lax` or `Strict` cookies** (Lax is the browser default in Chromium), anti-CSRF tokens (synchronizer or double-submit),
checking `Origin`/`Referer`, and requiring non-simple requests (custom headers / JSON) for state changes. Token auth in headers (not cookies) isn't vulnerable to CSRF.

## CORS (often misunderstood)

The **same-origin policy** stops scripts on origin A from reading responses from origin B. **CORS** lets server B opt in with
`Access-Control-Allow-Origin`. Non-simple requests (custom headers, JSON content type, PUT/DELETE) trigger a **preflight** `OPTIONS` request.
`Access-Control-Allow-Credentials: true` can't be combined with `*`. CORS is **not** a server-side protection: it doesn't stop curl or server-to-server calls.

## SSRF (server-side request forgery)

The server fetches a user-supplied URL and can be tricked into hitting internal services (e.g. the cloud metadata endpoint `169.254.169.254`).
Defenses: allow-lists of destinations, block private IP ranges after DNS resolution (watch DNS rebinding), disable redirects, use IMDSv2-style protections, egress firewalls.
Relevant to AI agents that browse URLs or fetch documents.

## Cookies

`HttpOnly` (no JS access) · `Secure` (HTTPS only) · `SameSite=Lax|Strict|None` (None requires Secure) · `__Host-` prefix (locks to host and path /) · short lifetimes for session cookies.

## Other must-knows

- Passwords: Argon2id or bcrypt with per-user salts; never encrypt passwords (hashing is one-way).
- Secrets in a vault (Key Vault, Secrets Manager), never in code or client bundles; rotate them.
- Security headers: `Strict-Transport-Security`, `Content-Security-Policy`, `X-Content-Type-Options: nosniff`, `Referrer-Policy`, frame protection (`frame-ancestors`).
- File uploads: validate type by content, size limits, store outside the web root / in object storage, scan for malware, serve from a separate domain.
- Rate limiting and bot protection on login, signup, password reset, and expensive endpoints (including LLM endpoints).
