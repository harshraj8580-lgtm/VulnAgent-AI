# 🛡️ VulnAgent – AI-Powered Website Security Agent

VulnAgent is a beginner-friendly AI-powered cybersecurity tool that checks website security configurations, identifies missing HTTP security headers, and provides actionable security recommendations.

Built as a solo hackathon project using Python, Streamlit, and Google Gemini AI.

---

## 🚀 Features

- 🔍 **Security Header Scanner** – Checks important HTTP security headers.
- 🔒 **HTTPS Validation** – Accepts HTTPS website URLs only.
- 🛡️ **Private IP Protection** – Blocks private and local IP targets.
- 📋 **Security Analysis** – Checks CSP, HSTS, X-Content-Type-Options, and Referrer-Policy.
- 🍪 **Cookie Security Checks** – Reviews Secure and HttpOnly flags when cookies are returned.
- 🤖 **Gemini AI Analyst** – Explains security findings and recommends fixes.
- 📊 **Security Score** – Calculates an overall security score.
- ⚠️ **Risk Classification** – Displays High, Medium, and Low severity findings.
- 📥 **JSON Reports** – Downloads scan results as JSON.
- 📄 **PDF Reports** – Downloads security scan results as PDF files.
- 🎨 **Interactive Dashboard** – Professional dark-blue Streamlit interface.

---

## 🧰 Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web dashboard |
| Google Gemini AI | AI-powered security explanations |
| Requests | HTTP requests and scanning |
| HTML/CSS | Dashboard styling |
| JSON | Security report generation |
| ReportLab | PDF report generation |

---

## 📸 Project Demo

**Example Scan Results**

| Security Check | Result |
|---|---|
| HTTP Status | 200 |
| Security Score | 80/100 |
| Content-Security-Policy | Missing |
| Strict-Transport-Security | Present |
| X-Content-Type-Options | Missing |
| Referrer-Policy | Missing |

---

## ⚙️ Project Structure

```text
VulnAgent-GitHub/
│
├── app.py
├── agent/
│   └── ai_analyzer.py
├── scanner/
│   └── security_checks.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 💻 Installation (Windows)

### 1. Install Python

Install Python 3.10 or newer.

### 2. Open the project folder

Open `VulnAgent-GitHub` in VS Code.

### 3. Create a virtual environment

```powershell
python -m venv venv
```

### 4. Activate the virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```powershell
pip install -r requirements.txt
```

### 6. Configure Gemini AI (Optional)

- Copy `.env.example` to `.env`.
- Add your own Gemini API key using the variable name expected by the application.
- Never upload `.env` or expose your API key on GitHub.

### 7. Run VulnAgent

```powershell
streamlit run app.py
```

The application will open in your browser.

---

## 🔐 Important Security Disclaimer

VulnAgent performs limited, non-destructive HTTP security configuration checks.

- It is not a complete penetration testing tool.
- It does not exploit vulnerabilities.
- It does not verify application-level SQL injection or XSS.
- Missing security headers do not prove that a website is exploitable.
- Redirects are not followed in this MVP.
- Private and local network targets are blocked.

Only scan websites you own or have explicit permission to assess.

URL and DNS protections should be reviewed and strengthened before exposing this application publicly.

---

## 🔮 Future Improvements

- Integrate OWASP ZAP passive baseline scanning for authorized targets.
- Improve security scoring and risk analysis.
- Implement scan history.
- Add automated tests.
- Strengthen redirect and DNS-rebinding protections.
- Improve dashboard visualizations.

---

## 👨‍💻 Project Information

**Project Name:** VulnAgent

**Project Type:** Solo Hackathon MVP

**Category:** AI & Cybersecurity

**Developer:** Harsh Raj

---

*Built with Python, Streamlit, and Gemini AI. 🛡️*