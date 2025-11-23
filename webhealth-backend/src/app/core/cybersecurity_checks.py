"""
Canonical map of passive cybersecurity checks allowed in WebHealth.

This mirrors the requirements shared by the product brief so that enforcement
logic elsewhere in the backend can import a single source of truth.
"""
from __future__ import annotations

CYBERSECURITY_CHECKS = {
    "objective": (
        "Add safe, passive cybersecurity checks to monitored websites without "
        "triggering bans, rate limits, or violating security expectations."
    ),
    "principles": [
        "No intrusion",
        "No exploitation",
        "No fingerprinting that triggers alarms",
        "No heavy scanning",
        "No port scanning",
        "No directory brute forcing",
    ],
    "safe_passive_checks": {
        "ssl_security": [
            "Check SSL certificate expiration",
            "Check certificate issuer",
            "Check protocol version (TLS 1.2, TLS 1.3)",
            "Check for weak ciphers through passive handshakes",
        ],
        "http_security_headers": [
            "Check for Content-Security-Policy header",
            "Check for Strict-Transport-Security",
            "Check for X-Frame-Options",
            "Check for X-Content-Type-Options",
            "Check for Referrer-Policy",
            "Check for Permissions-Policy",
            "Check for Access-Control-Allow-Origin",
        ],
        "basic_app_security": [
            "Check if site is using HTTPS",
            "Ensure redirects do not downgrade HTTPS to HTTP",
            "Check whether cookies include Secure/HttpOnly flags",
            "Check for open directory listings only if naturally returned",
        ],
        "exposure_checks": [
            "Fetch robots.txt and look for sensitive paths",
            "Attempt passive GET for '/.env'",
            "Attempt passive GET for '/.git/HEAD'",
            "Check server error pages for verbose version info",
        ],
        "technology_fingerprinting": {
            "method": "passive_header_analysis",
            "checks": [
                "Server header (Apache, Nginx, etc.)",
                "X-Powered-By header",
                "Framework hints from headers",
                "CDN provider headers",
            ],
            "note": "No active fingerprinting/waf bypass attempts",
        },
        "security_best_practices": [
            "Check HTTPS redirects behave correctly",
            "Inspect rate-limiting headers if exposed",
            "Inspect cache-control headers on sensitive responses",
        ],
        "dns_security": [
            "Check for CAA records",
            "Check DNSSEC support via public DNS",
            "Check MX records for email security posture",
        ],
        "safe_waf_detection": {
            "method": "observe_http_response_headers",
            "checks": ["Cloudflare", "Akamai", "CloudFront", "Sucuri", "Imperva"],
            "note": "No evasion attempts",
        },
    },
    "rate_limit_protection": {
        "strategy": "Ensure WebHealth avoids rate limits/bans",
        "controls": [
            "Max 1 request per monitor per 60 seconds",
            "Randomized User-Agent rotation",
            "Back off exponentially after 429",
            "Respect Retry-After header",
            "Automatic cooldown periods",
            "Do not crawl multiple paths beyond primary URL",
        ],
    },
    "legal_and_safety_notes": [
        "Only passive HTTP GET and SSL handshake checks",
        "Never send payloads or fuzzing strings",
        "Never brute-force or port scan",
        "Respect robots.txt and rate limits",
        "All checks must be observational only",
    ],
}

