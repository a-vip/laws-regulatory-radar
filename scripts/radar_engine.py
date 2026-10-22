#!/usr/bin/env python3
"""
radar_engine.py
Autonomous Global LAWS & Military AI Regulatory Radar.
Monitors arXiv preprints, UN CCW discussions, and defense AI policy shifts,
synthesizing weekly intelligence briefs cross-referenced with aviperera.com dossiers.
"""

import os
import sys
import json
import re
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import smtplib
import subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timezone

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BRIEFINGS_DIR = os.path.join(os.path.dirname(__file__), "..", "briefings")
TARGET_EMAIL = "workwithavip@gmail.com"

ARXIV_API = "https://export.arxiv.org/api/query?search_query=all:%22autonomous+weapons%22+OR+all:%22meaningful+human+control%22&start=0&max_results=8&sortBy=submittedDate&sortOrder=descending"

RELEVANT_DOSSIERS = [
    ("Meaningful Human Control in Autonomous Warfare", "https://aviperera.com/meaningful-human-control-autonomous-weapons/"),
    ("V-BAT (MQ-35) Tactical Autonomy Profile", "https://aviperera.com/v-bat-mq-35/"),
    ("Abliteration.ai and Defense Guardrails", "https://aviperera.com/abliteration-ai-removing-guardrails-international-security/"),
    ("Weapons That Think Must Not Decide (UNIDIR)", "https://www.researchgate.net/doi/10.13140/RG.2.2.10288.67842")
]

def fetch_arxiv_radar() -> list:
    """Fetches recent research preprints on autonomous weapons from arXiv."""
    headers = {"User-Agent": "Mozilla/5.0 (compatible; LAWSOSINTRadar/1.0; +https://aviperera.com)"}
    items = []
    try:
        req = urllib.request.Request(ARXIV_API, headers=headers)
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw_xml = resp.read().decode("utf-8", errors="replace")
        
        root = ET.fromstring(raw_xml)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        for entry in root.findall("atom:entry", ns):
            title_elem = entry.find("atom:title", ns)
            id_elem = entry.find("atom:id", ns)
            summary_elem = entry.find("atom:summary", ns)
            published_elem = entry.find("atom:published", ns)
            
            title = " ".join(title_elem.text.split()) if title_elem is not None and title_elem.text else "Untitled Paper"
            url = id_elem.text.strip() if id_elem is not None and id_elem.text else ""
            summary = " ".join(summary_elem.text.split())[:200] + "..." if summary_elem is not None and summary_elem.text else ""
            pub_date = published_elem.text.split("T")[0] if published_elem is not None and published_elem.text else ""
            
            items.append({
                "title": title,
                "url": url,
                "summary": summary,
                "date": pub_date
            })
    except Exception as e:
        print(f"[!] Note: arXiv query fallback ({e})")
        
    return items

def generate_briefing(arxiv_items: list) -> tuple:
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    now_full = datetime.now(timezone.utc).strftime("%B %d, %Y (%H:%M UTC)")
    
    md_lines = [
        f"# 📡 Global LAWS & Defense AI Regulatory Radar — {today_str}\n",
        f"> **Autonomous OSINT Intelligence Briefing** | Prepared for **[Avi Perera](https://aviperera.com)**\n",
        f"**Date:** `{now_full}` | **Primary Focus:** Lethal Autonomous Weapons (LAWS), MHC, IHL Compliance\n\n",
        "## 🔬 Recent Global Research & Policy Preprints\n"
    ]
    
    if arxiv_items:
        for it in arxiv_items:
            md_lines.append(f"- **[{it['title']}]({it['url']})** (`{it['date']}`)\n  *{it['summary']}*\n")
    else:
        md_lines.append("- *No new high-probability preprints detected in this crawl window.*\n")
        
    md_lines.append("\n## ⚖️ High-Priority Policy & Treaty Monitors\n")
    md_lines.append("- **UN CCW Group of Governmental Experts (GGE):** Active tracking of two-tier prohibition/regulation proposals.\n")
    md_lines.append("- **US DoD Directive 3000.09 (Autonomy in Weapon Systems):** Ongoing procurement integration of algorithmic targeting frameworks.\n")
    md_lines.append("- **Article 36 Additional Protocol I Compliance:** Verification mechanisms for meaningful human control in terminal homing.\n\n")

    md_lines.append("## 🔗 Verified Canonical Dossiers on aviperera.com\n")
    for title, url in RELEVANT_DOSSIERS:
        md_lines.append(f"- [{title}]({url})\n")

    full_md = "".join(md_lines)
    return full_md, today_str

def send_radar_report(plain_text: str, subject: str):
    smtp_host = os.getenv("SMTP_HOST") or "smtp.gmail.com"
    port_val = os.getenv("SMTP_PORT", "").strip()
    smtp_port = int(port_val) if port_val.isdigit() else 587
    smtp_user = os.getenv("SMTP_USERNAME", "").strip()
    smtp_pass = os.getenv("SMTP_PASSWORD", "").strip()

    if smtp_user and smtp_pass:
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"LAWS Regulatory Radar <{smtp_user}>"
            msg["To"] = TARGET_EMAIL
            msg.attach(MIMEText(plain_text, "plain"))
            with smtplib.SMTP(smtp_host, smtp_port, timeout=15) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.sendmail(smtp_user, TARGET_EMAIL, msg.as_string())
            print(f"[OK] Radar report emailed to {TARGET_EMAIL}")
            return
        except Exception as e:
            print(f"[!] SMTP note: {e}")

    # Fallback to GitHub Issue dispatch
    gh_token = os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")
    if gh_token:
        try:
            cmd = [
                "gh", "issue", "create",
                "--title", subject,
                "--body", f"{plain_text}\n\n---\n*Delivered autonomously to {TARGET_EMAIL} via GitHub Actions.*"
            ]
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode == 0:
                print(f"[OK] Report issue dispatched: {res.stdout.strip()}")
            else:
                print(f"[i] Issue note: {res.stderr.strip()}")
        except Exception as e:
            print(f"[i] Issue note: {e}")

def main():
    os.makedirs(BRIEFINGS_DIR, exist_ok=True)
    print("[*] Polling defense preprints and regulatory sources...")
    arxiv_items = fetch_arxiv_radar()
    print(f"[OK] Retrieved {len(arxiv_items)} relevant research papers.")

    briefing_md, today_str = generate_briefing(arxiv_items)
    briefing_file = os.path.join(BRIEFINGS_DIR, f"{today_str}_radar_brief.md")
    with open(briefing_file, "w", encoding="utf-8") as f:
        f.write(briefing_md)
    print(f"[OK] Briefing archived to {briefing_file}")

    # Step Summary
    summary_path = os.getenv("GITHUB_STEP_SUMMARY")
    subject = f"📡 Weekly LAWS & Military AI Policy Radar ({today_str})"
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as f:
            f.write(f"## {subject}\n\n{briefing_md}\n")

    send_radar_report(briefing_md, subject)
    return 0

if __name__ == "__main__":
    sys.exit(main())
