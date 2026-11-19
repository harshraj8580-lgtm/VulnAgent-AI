from urllib.parse import urlparse
import ipaddress
import socket
import requests

TIMEOUT = 8
MAX_REDIRECTS = 3

def _validate_public_https_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme != "https":
        raise ValueError("For this MVP, please use an HTTPS URL.")
    if not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("Enter a valid URL without embedded credentials.")
    if parsed.port not in (None, 443):
        raise ValueError("Only the standard HTTPS port (443) is supported.")

    host = parsed.hostname
    try:
        ip = ipaddress.ip_address(host)
        addresses = [ip]
    except ValueError:
        try:
            infos = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
            addresses = [ipaddress.ip_address(info[4][0]) for info in infos]
        except socket.gaierror as exc:
            raise ValueError("Could not resolve the hostname.") from exc

    if not addresses or any(not addr.is_global for addr in addresses):
        raise ValueError("Private, local, and non-public network targets are blocked.")
    return url

def scan_security_headers(url: str):
    url = _validate_public_https_url(url)
    session = requests.Session()
    session.trust_env = False
    response = session.get(
        url,
        timeout=TIMEOUT,
        allow_redirects=False,
        headers={"User-Agent": "VulnAgent-Hackathon-MVP/1.0"}
    )

    # Redirects are intentionally not followed: the destination would need
    # independent authorization and validation first.
    headers = response.headers
    checks = [
        ("Content-Security-Policy", "Medium",
         "Helps reduce the impact of content injection and XSS."),
        ("Strict-Transport-Security", "Low",
         "Tells browsers to prefer HTTPS for future visits."),
        ("X-Content-Type-Options", "Low",
         "Helps prevent MIME-type sniffing."),
        ("Referrer-Policy", "Low",
         "Controls how much referrer information browsers send.")
    ]

    findings = []
    for header, severity, explanation in checks:
        present = header in headers
        findings.append({
            "name": f"{header} header",
            "severity": severity,
            "status": "Present" if present else "Missing",
            "evidence": "Header returned by server." if present else f"{header} was not present.",
            "recommendation": explanation
        } if not present else {
            "name": f"{header} header",
            "severity": "Info",
            "status": "Present",
            "evidence": "Header returned by server.",
            "recommendation": "Review the policy periodically."
        })

    cookie_headers = response.raw.headers.getlist("Set-Cookie") if hasattr(response.raw.headers, "getlist") else []
    if cookie_headers:
        for cookie in cookie_headers:
            flags = cookie.lower()
            missing = []
            if "secure" not in flags:
                missing.append("Secure")
            if "httponly" not in flags:
                missing.append("HttpOnly")
            if missing:
                findings.append({
                    "name": "Cookie security flags",
                    "severity": "Medium",
                    "status": "Review",
                    "evidence": "One or more Set-Cookie headers may be missing: " + ", ".join(missing),
                    "recommendation": "Set Secure and HttpOnly where appropriate; review SameSite too."
                })

    metadata = {
        "final_url": url,
        "status_code": response.status_code
    }
    return findings, metadata
