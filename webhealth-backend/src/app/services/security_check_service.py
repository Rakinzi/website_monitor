from __future__ import annotations

import asyncio
import random
import socket
import ssl
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict
from urllib.parse import urlparse, urlunparse

import dns.resolver
import httpx

from app.core.cybersecurity_checks import CYBERSECURITY_CHECKS


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/121.0",
]

EXPOSURE_PATHS = {
    "robots_txt": "/robots.txt",
    "dot_env": "/.env",
    "git_head": "/.git/HEAD",
}

DNS_RECORDS = {
    "CAA": "caa",
    "DNSSEC": "dnskey",
    "MX": "mx",
}

WAF_HEADERS = [
    "cf-ray",
    "cf-visitor",
    "x-akamai-session-info",
    "x-sucuri-id",
    "x-iinfo",
    "x-cdn",
    "server",
]


@dataclass
class SecurityCheckResult:
    url: str
    checks: Dict[str, Any]


class SecurityCheckService:
    """Runs passive cybersecurity checks defined in CYBERSECURITY_CHECKS."""

    def __init__(self) -> None:
        self._client = httpx.AsyncClient(
            timeout=10,
            follow_redirects=True,
            headers={"User-Agent": random.choice(USER_AGENTS)},
        )

    async def aclose(self) -> None:
        await self._client.aclose()

    async def run_passive_checks(self, url: str) -> SecurityCheckResult:
        self._client.headers["User-Agent"] = random.choice(USER_AGENTS)
        parsed = urlparse(url)
        base_url = urlunparse((parsed.scheme, parsed.netloc, "", "", "", ""))
        response = await self._client.get(url)

        ssl_info = (
            await self._check_ssl(parsed.hostname or "", parsed.port or 443)
            if parsed.scheme == "https"
            else {
                "enabled": False,
                "reason": "URL not using HTTPS",
            }
        )

        http_header_checks = self._inspect_security_headers(response)
        basic_app_security = self._check_basic_app_security(parsed, response)
        exposure = await self._check_exposure(base_url)
        fingerprint = self._technology_fingerprint(response)
        best_practices = self._best_practices(response)
        dns_security = await self._dns_security(parsed.hostname or "")
        waf = self._detect_waf(response)

        return SecurityCheckResult(
            url=url,
            checks={
                "policy": CYBERSECURITY_CHECKS,
                "ssl_security": ssl_info,
                "http_security_headers": http_header_checks,
                "basic_app_security": basic_app_security,
                "exposure_checks": exposure,
                "technology_fingerprinting": fingerprint,
                "security_best_practices": best_practices,
                "dns_security": dns_security,
                "safe_waf_detection": waf,
            },
        )

    async def _check_ssl(self, hostname: str, port: int) -> Dict[str, Any]:
        if not hostname:
            return {"enabled": False, "reason": "Missing hostname"}

        def _pull_cert():
            context = ssl.create_default_context()
            with socket.create_connection((hostname, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    cipher = ssock.cipher()
                    version = ssock.version()
            return cert, cipher, version

        try:
            cert, cipher, version = await asyncio.to_thread(_pull_cert)
        except Exception as exc:  # pragma: no cover - network issue
            return {"enabled": True, "error": str(exc)}

        not_after = cert.get("notAfter")
        expires_at = None
        days_remaining = None
        if not_after:
            expires_at = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z").replace(
                tzinfo=timezone.utc
            )
            days_remaining = (expires_at - datetime.now(timezone.utc)).days

        issuer_data = dict(x[0] for x in cert.get("issuer", []))
        cipher_suite = cipher[0] if cipher else None
        cipher_bits = cipher[2] if cipher else None
        weak_cipher = bool(cipher_bits and cipher_bits < 128)

        return {
            "enabled": True,
            "issuer": issuer_data.get("organizationName"),
            "expires_at": expires_at.isoformat() if expires_at else None,
            "days_remaining": days_remaining,
            "protocol": version,
            "cipher_suite": cipher_suite,
            "weak_cipher": weak_cipher,
        }

    def _inspect_security_headers(self, response: httpx.Response) -> Dict[str, Any]:
        headers = response.headers
        return {
            "content_security_policy": "content-security-policy" in headers,
            "strict_transport_security": "strict-transport-security" in headers,
            "x_frame_options": "x-frame-options" in headers,
            "x_content_type_options": "x-content-type-options" in headers,
            "referrer_policy": "referrer-policy" in headers,
            "permissions_policy": "permissions-policy" in headers,
            "cors_header": "access-control-allow-origin" in headers,
        }

    def _check_basic_app_security(
        self, parsed_url, response: httpx.Response
    ) -> Dict[str, Any]:
        uses_https = parsed_url.scheme == "https"
        final_scheme = response.url.scheme
        downgraded = uses_https and final_scheme == "http"

        cookies = getattr(response.cookies, "jar", response.cookies)
        cookie_flags = []
        for cookie in cookies:
            httponly = False
            has_attr = getattr(cookie, "has_nonstandard_attr", None)
            if callable(has_attr):
                httponly = bool(has_attr("HttpOnly"))
            else:
                httponly = "httponly" in (cookie._rest or {})  # type: ignore[attr-defined]
            cookie_flags.append(
                {"name": cookie.name, "secure": cookie.secure, "httponly": httponly}
            )

        open_directory = False
        if response.status_code == 200 and response.text:
            text_lower = response.text[:4096].lower()
            open_directory = "index of /" in text_lower or "directory listing" in text_lower

        return {
            "uses_https": uses_https,
            "final_scheme": final_scheme,
            "downgraded_to_http": downgraded,
            "cookies": cookie_flags,
            "open_directory_listing": open_directory,
        }

    async def _check_exposure(self, base_url: str) -> Dict[str, Any]:
        results: Dict[str, Any] = {}
        for key, path in EXPOSURE_PATHS.items():
            try:
                resp = await self._client.get(base_url + path, follow_redirects=False)
                results[key] = {
                    "status_code": resp.status_code,
                    "exposed": resp.status_code == 200,
                }
                if key == "robots_txt" and resp.status_code == 200:
                    disallows = [
                        line.split(":")[1].strip()
                        for line in resp.text.splitlines()
                        if line.lower().startswith("disallow")
                    ]
                    results["robots_disallows"] = disallows
            except httpx.HTTPError as exc:  # pragma: no cover - network issues
                results[key] = {"error": str(exc)}
        return results

    def _technology_fingerprint(self, response: httpx.Response) -> Dict[str, Any]:
        headers = response.headers
        return {
            "server": headers.get("server"),
            "x_powered_by": headers.get("x-powered-by"),
            "framework": headers.get("x-framework"),
            "cdn": headers.get("cf-cache-status")
            or headers.get("x-akamai-session-info")
            or headers.get("x-cdn"),
        }

    def _best_practices(self, response: httpx.Response) -> Dict[str, Any]:
        history = response.history or []
        redirect_chain = [str(resp.url) for resp in history] + [str(response.url)]
        rate_limit = {
            "limit": response.headers.get("x-ratelimit-limit"),
            "remaining": response.headers.get("x-ratelimit-remaining"),
            "reset": response.headers.get("x-ratelimit-reset"),
        }
        return {
            "https_redirect_chain": redirect_chain,
            "cache_control": response.headers.get("cache-control"),
            "rate_limit_headers": rate_limit,
        }

    async def _dns_security(self, hostname: str) -> Dict[str, Any]:
        if not hostname:
            return {"error": "hostname missing"}

        results: Dict[str, Any] = {}

        async def resolve(record_type: str):
            try:
                answers = await asyncio.to_thread(
                    dns.resolver.resolve, hostname, record_type
                )
                return [str(rdata) for rdata in answers]
            except Exception:
                return []

        for record, resolver_name in DNS_RECORDS.items():
            records = await resolve(record)
            results[resolver_name] = records
        return results

    def _detect_waf(self, response: httpx.Response) -> Dict[str, Any]:
        headers = response.headers
        detected = []
        for header in WAF_HEADERS:
            if header in headers:
                detected.append(header)
        return {"headers": detected, "server": headers.get("server")}
