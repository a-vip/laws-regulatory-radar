# 📡 Global LAWS & Military AI Regulatory Radar

[![Radar Briefing](https://github.com/a-vip/laws-regulatory-radar/actions/workflows/radar-sync-and-report.yml/badge.svg)](https://github.com/a-vip/laws-regulatory-radar/actions/workflows/radar-sync-and-report.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Curated by Avi Perera](https://img.shields.io/badge/Curated_by-Avi_Perera-blue.svg)](https://aviperera.com)

An autonomous OSINT intelligence engine tracking preprints, policy declarations, and multilateral developments concerning **Lethal Autonomous Weapons Systems (LAWS)**, Meaningful Human Control (MHC), and military artificial intelligence.

Maintained by **[Avi Perera](https://aviperera.com)** — AI Governance Researcher, LAWS Expert, and Founder of [SovDash](https://sovdash.com).

---

## ⚡ What It Tracks

```mermaid
flowchart LR
    A[arXiv & Semantic Scholar APIs] -->|Filter LAWS Preprints| D[Radar Engine]
    B[UNODA CCW Disarmament Meetings] -->|Regulatory Tracking| D
    C[US DoD Directive 3000.09 / NATO] -->|Defense Policy| D
    D --> E[briefings/YYYY-MM-DD_radar_brief.md]
    D -->|Executive Email Brief| F[workwithavip@gmail.com]
    D -->|Canonical Link Injection| G[aviperera.com]
```

1. **Academic Preprints**: Ingests newly published papers on autonomous weapons, algorithmic targeting, and meaningful human control from the arXiv research network.
2. **Treaty & Multilateral Bodies**: Monitors UN CCW Group of Governmental Experts (GGE) discussions and international humanitarian law compliance.
3. **Cross-Referenced Dossiers**: Connects breaking policy shifts directly to verified weapon dossiers published on **[aviperera.com](https://aviperera.com)**.

---

## 📑 Intelligence Archive

Browse archived intelligence digests in the [**`briefings/`**](briefings/) directory.

---

## 📄 License

MIT © [Avi Perera](https://aviperera.com)
