# VulnAgent 🛡️

A beginner-friendly hackathon MVP for checking a small set of website security configuration headers and explaining findings.

## Features

- Streamlit dashboard
- HTTPS-only URL validation
- Blocks private/local IP targets
- Checks CSP, HSTS, X-Content-Type-Options and Referrer-Policy
- Reviews Secure and HttpOnly cookie flags when cookies are returnead
- Optional Gemini-powered explanations
- Downloadable JSON scan report

## Important safety scope

Use only websites you own or have explicit permission to assess. This starter performs limited, non-destructive HTTP checks. It is **not** a complete penetration test, does not exploit vulnerabilities, and does not verify application-level SQL injection or XSS. Missing headers are configuration findings, not proof that a site is exploitable.

Redirects are not followed in this MVP. Private and local network targets are blocked. Review and strengthen URL/DNS protections before exposing this app publicly.

## Setup (Windows)

1. Install Python 3.10 or newer.
2. Open this folder in VS Code.
3. Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

4. Install dependencies:

```powershell
pip install -r requirements.txt
```

5. Optional Gemini setup:
   - Copy `.env.example` to `.env`
   - Add your own Gemini API key
   - Never commit `.env` to GitHub

6. Run:

```powershell
streamlit run app.py
```

## GitHub upload

Create a new empty repository on GitHub, then run these commands in the project folder:

```bash
git init
git add .
git commit -m "Initial VulnAgent MVP"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Replace the remote URL with your own repository URL.

## Next improvements

- Add a controlled OWASP ZAP passive baseline scan for explicitly authorized targets
- Improve risk scoring and evidence presentation
- Add PDF report generation
- Add scan history
- Add tests and stronger redirect/DNS-rebinding protections
