import streamlit as st
import json
from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from scanner.security_checks import scan_security_headers
from agent.ai_analyzer import explain_findings, recommend_security_fixes


def create_pdf_report(target, status_code, score, findings):
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(
        Paragraph("VulnAgent Security Report", styles["Title"])
    )
    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(f"Target: {escape(str(target))}", styles["Normal"])
    )
    elements.append(
        Paragraph(f"HTTP Status: {escape(str(status_code))}", styles["Normal"])
    )
    elements.append(
        Paragraph(f"Security Score: {score}/100", styles["Normal"])
    )
    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph("Security Findings", styles["Heading2"])
    )
    elements.append(Spacer(1, 10))

    table_data = [[
        Paragraph("Check", styles["Normal"]),
        Paragraph("Severity", styles["Normal"]),
        Paragraph("Status", styles["Normal"]),
        Paragraph("Evidence", styles["Normal"])
    ]]

    for finding in findings:
        table_data.append([
            Paragraph(escape(str(finding["name"])), styles["BodyText"]),
            Paragraph(escape(str(finding["severity"])), styles["BodyText"]),
            Paragraph(escape(str(finding["status"])), styles["BodyText"]),
            Paragraph(escape(str(finding["evidence"])), styles["BodyText"])
        ])

    table = Table(
        table_data,
        colWidths=[130, 65, 65, 190],
        repeatRows=1
    )

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            "Note: Limited, non-destructive checks only. "
            "Not a full penetration test.",
            styles["Italic"]
        )
    )

    doc.build(elements)

    buffer.seek(0)
    return buffer.getvalue()


st.set_page_config(
    page_title="VulnAgent",
    page_icon="🛡️",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #080d20, #111b35);
    color: #edf2ff;
}

section[data-testid="stSidebar"] {
    background: #0d1430;
    border-right: 1px solid #27366b;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1 {
    color: #ffffff;
    font-weight: 800;
}

h2, h3 {
    color: #dce7ff;
}

div[data-testid="stMetric"] {
    background: #111b3a;
    padding: 18px;
    border: 1px solid #344878;
    border-radius: 14px;
}

.stButton > button {
    background: linear-gradient(90deg, #2563eb, #4f46e5);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: 600;
}

.stButton > button:hover {
    background: #1d4ed8;
    color: white;
    border: 1px solid #60a5fa;
}
</style>
""", unsafe_allow_html=True)


st.title("🛡️ VulnAgent")
st.caption("AI-powered website security configuration assistant")

st.warning(
    "Only scan websites you own or have explicit permission to test. "
    "This MVP performs limited, non-destructive HTTP checks."
)


with st.sidebar:
    st.header("VulnAgent")
    page = st.radio("Navigation", ["Dashboard", "About"])
    st.divider()
    st.caption("Beginner-friendly hackathon MVP")


if page == "About":
    st.title("🛡️ About VulnAgent")

    st.caption("AI-Powered Website Security Configuration Assistant")

    st.info(
        "VulnAgent is a beginner-friendly AI cybersecurity "
        "assistant that helps identify common website security "
        "configuration issues."
    )

    st.subheader("🎯 Project Overview")

    st.write(
        "VulnAgent scans website HTTP security headers and "
        "cookie security flags. It calculates a security score, "
        "identifies missing protections, and suggests possible fixes."
    )

    st.subheader("⚡ Key Features")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔍 Security Scanner")
        st.write("- HTTPS URL validation")
        st.write("- Security headers checking")
        st.write("- Cookie Secure and HttpOnly checks")
        st.write("- Security score calculation")

    with col2:
        st.markdown("### 🤖 AI Security Analyst")
        st.write("- Gemini AI explanations")
        st.write("- Security fix recommendations")
        st.write("- High, Medium and Low severity")
        st.write("- JSON and PDF security report download")

    st.subheader("💻 Technologies Used")

    st.markdown("""
    - **Python** – Core programming language
    - **Streamlit** – Interactive dashboard
    - **Google Gemini AI** – AI security analysis
    - **Requests** – HTTP requests and website scanning
    - **HTML/CSS** – Dashboard styling
    - **JSON** – Security report generation
    - **ReportLab** – PDF report generation
    """)

    st.subheader("⚙️ How VulnAgent Works")

    st.markdown("""
    1. Enter an authorized HTTPS website URL.
    2. VulnAgent checks selected security headers.
    3. It analyzes cookie security flags.
    4. A security score and findings are generated.
    5. Gemini AI explains findings and suggests fixes.
    6. Download the security report in JSON or PDF format.
    """)

    st.subheader("⚠️ Security Disclaimer")

    st.warning(
        "VulnAgent performs limited, non-destructive HTTP "
        "security configuration checks. It is not a complete "
        "penetration testing tool and does not exploit vulnerabilities. "
        "Only scan websites you own or have explicit permission to test."
    )

    st.divider()

    st.caption("🛡️ VulnAgent | Solo Hackathon Project")

    st.stop()


st.subheader("Website security check")

url = st.text_input(
    "Authorized website URL",
    placeholder="https://example.com"
)

run = st.button(
    "🔍 Scan website",
    type="primary",
    use_container_width=False
)


if run:
    if not url.strip():
        st.error("Please enter a website URL.")
    else:
        with st.spinner("Checking security configuration..."):
            try:
                findings, metadata = scan_security_headers(url.strip())

                st.session_state["findings"] = findings
                st.session_state["metadata"] = metadata
                st.session_state["target"] = metadata["final_url"]

            except Exception as exc:
                st.error(f"Scan could not be completed: {exc}")


findings = st.session_state.get("findings")
metadata = st.session_state.get("metadata")


if findings is not None and metadata is not None:

    total = len(findings)
    high = sum(f["severity"] == "High" for f in findings)
    medium = sum(f["severity"] == "Medium" for f in findings)
    low = sum(f["severity"] == "Low" for f in findings)

    score = max(0, 100 - high * 20 - medium * 10 - low * 5)

    st.success(f"Checks completed for {metadata['final_url']}")

    st.subheader("📊 Security Overview")

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.metric("🛡️ Security Score", f"{score}/100")

    with c2:
        st.metric("📋 Total Findings", total)

    with c3:
        st.metric("🔴 High Risk", high)

    with c4:
        st.metric("🟠 Medium Risk", medium)

    with c5:
        st.metric("🟡 Low Risk", low)

    st.progress(score / 100)

    st.subheader("Security findings")

    if findings:
        st.dataframe(
            [
                {
                    "Check": f["name"],
                    "Severity": f["severity"],
                    "Status": f["status"],
                    "Evidence": f["evidence"]
                }
                for f in findings
            ],
            width="stretch",
            hide_index=True
        )
    else:
        st.success("No issues were found by these limited checks.")

    st.subheader("🛠️ Recommended Security Fixes")

    recommendations = recommend_security_fixes(findings)

    st.markdown(recommendations)

    st.subheader("AI security analyst")

    if st.button("Explain findings"):
        with st.spinner("Preparing explanations..."):
            try:
                st.session_state["explanations"] = explain_findings(findings)
            except Exception as exc:
                st.error(str(exc))

    if st.session_state.get("explanations"):
        st.markdown(st.session_state["explanations"])

    report = {
        "target": metadata["final_url"],
        "status_code": metadata["status_code"],
        "security_score": score,
        "findings": findings,
        "note": "Limited, non-destructive checks only. Not a full penetration test."
    }

    st.divider()
    st.subheader("📥 Download Security Reports")

    col_json, col_pdf = st.columns(2)

    with col_json:
        st.download_button(
            "⬇️ Download JSON report",
            data=json.dumps(report, indent=2),
            file_name="vulnagent-report.json",
            mime="application/json"
        )

    with col_pdf:
        pdf_data = create_pdf_report(
            metadata["final_url"],
            metadata["status_code"],
            score,
            findings
        )

        st.download_button(
            "📄 Download PDF report",
            data=pdf_data,
            file_name="vulnagent-report.pdf",
            mime="application/pdf"
        )

else:
    st.info(
        "Enter an authorized HTTPS website above and click "
        "**Scan website** to begin."
    )

    st.subheader("What this MVP checks")

    st.write(
        "- HTTPS usage\n"
        "- Content-Security-Policy\n"
        "- Strict-Transport-Security\n"
        "- X-Content-Type-Options\n"
        "- Referrer-Policy\n"
        "- Cookie Secure and HttpOnly flags"
    )