
import os
import time

from dotenv import load_dotenv

load_dotenv()


def recommend_security_fixes(findings):
    """Generate practical recommendations without requiring an AI API."""

    recommendations = []

    for finding in findings:
        name = finding.get("name", "Security check")
        status = str(finding.get("status", "")).lower()

        if status not in ("missing", "not present", "failed"):
            continue

        header = name.lower()

        if "content-security-policy" in header:
            fix = """
**Recommended fix:**
- Configure a Content-Security-Policy (CSP) header.
- Start with a policy that allows only trusted sources.
- Test the policy before enforcing it on a production website.

Example:
`Content-Security-Policy: default-src 'self'`
"""
        elif "strict-transport-security" in header:
            fix = """
**Recommended fix:**
- Enable HTTP Strict Transport Security (HSTS).
- Configure your server to send the HSTS header over HTTPS.

Example:
`Strict-Transport-Security: max-age=31536000`
"""
        elif "x-content-type-options" in header:
            fix = """
**Recommended fix:**
- Add the X-Content-Type-Options header.
- This helps prevent browsers from MIME-type sniffing.

Example:
`X-Content-Type-Options: nosniff`
"""
        elif "referrer-policy" in header:
            fix = """
**Recommended fix:**
- Configure a Referrer-Policy header.
- A common starting option is strict-origin-when-cross-origin.

Example:
`Referrer-Policy: strict-origin-when-cross-origin`
"""
        elif "cookie" in header:
            fix = """
**Recommended fix:**
- Review your session cookies.
- Set Secure for HTTPS-only transmission.
- Set HttpOnly to prevent JavaScript access where appropriate.
"""
        else:
            fix = """
**Recommended fix:**
- Review this security check.
- Follow the recommendation provided in the scan findings.
"""

        recommendations.append(
            f"### {name}\n"
            f"**Status:** {finding.get('status', 'Unknown')}\n"
            f"{fix}"
        )

    if not recommendations:
        return (
            "### No missing security settings detected\n"
            "The limited checks did not identify missing settings. "
            "This does not mean the website is completely secure."
        )

    return "\n\n---\n\n".join(recommendations)


def explain_findings(findings):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return (
            "**Gemini AI is not configured yet.** "
            "You can still use the Rule-Based Security Recommendations feature. "
            "Add your Gemini API key to your local `.env` file. "
            "Never commit `.env` to GitHub."
        )

    try:
        from google import genai

        client = genai.Client(api_key=api_key)

        prompt = (
            "You are a cautious website security assistant. Explain these limited "
            "security-header findings in simple language. Do not claim exploitation "
            "or confirmed vulnerabilities. Give safe remediation advice:\n"
            + str(findings)
        )

        # Try up to 3 times for temporary server errors.
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )

                if response and response.text:
                    return response.text

                return "Gemini returned an empty response. Please try again."

            except Exception as exc:
                error_message = str(exc).lower()

                temporary_error = any(
                    term in error_message
                    for term in [
                        "503",
                        "unavailable",
                        "high demand",
                        "429",
                        "resource_exhausted",
                        "500",
                        "502",
                        "504",
                        "deadline exceeded"
                    ]
                )

                if temporary_error and attempt < 2:
                    wait_seconds = 3 * (2 ** attempt)

                    time.sleep(wait_seconds)
                    continue

                raise

    except Exception as exc:
        return f"AI explanation unavailable: {exc}"
