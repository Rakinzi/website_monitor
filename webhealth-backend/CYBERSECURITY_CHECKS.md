# Passive Cybersecurity Checks

WebHealth only performs **safe, observational** checks against monitored properties. The allowed scope mirrors `app/core/cybersecurity_checks.py` and is summarized below.

## Principles
- No intrusion or exploitation attempts
- No fingerprinting that triggers alarms, heavy scanning, port scans, or brute forcing
- Only standard HTTPS GET requests and SSL handshakes

## Allowed Checks
- **SSL security**: cert expiry, issuer, TLS version, weak ciphers via handshake
- **HTTP headers**: CSP, HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, CORS headers
- **Basic app posture**: HTTPS enforcement, redirect safety, Secure/HttpOnly cookies, naturally exposed directory listings
- **Exposure**: passive reads of `robots.txt`, `/.env`, `/.git/HEAD`, verbose error pages
- **Technology fingerprinting**: header analysis only (Server, X-Powered-By, CDN hints)
- **Security best practices**: redirect handling, rate-limit headers, cache-control
- **DNS posture**: CAA records, DNSSEC (via public resolvers), MX record presence
- **Safe WAF detection**: observe headers for Cloudflare, Akamai, CloudFront, Sucuri, Imperva

## Rate-Limit Strategy
- Max one request per monitor every 60s
- Randomize User-Agent, respect Retry-After, exponential backoff on 429s
- Automatic cooldown periods and no multi-path crawling

## Legal & Safety
- Never send fuzzing payloads or attempt exploitation
- Always respect robots.txt and site rate limits
- All checks remain observational only
