# Notion Database Schema

The Notion database acts as the private backend and source of truth for this system.
Actual application data is intentionally kept private. This document describes the schema
used by the automation and agents.

---

## Core application tracking

| Field | Type | Description |
|------|-----|-------------|
| Company | Title | Company name |
| Position | Text | Job title |
| Country | Select | Germany / Austria / Switzerland / EU / Other |
| Place | Text | City or region |
| Remote | Select | Remote / Hybrid / Onsite |
| Posting URL | URL | Original job posting |
| Source | Select | LinkedIn / Company site / Other |
| Stage | Select | Found / Ready to apply / Applied / Interview / Rejected |
| Applied | Date | Date of application |

---

## Fit & analysis fields

| Field | Type | Description |
|------|-----|-------------|
| Industry | Select | E-commerce, SaaS, IT, Marketplace, etc. |
| Keywords | Multi-select | Optimized keywords used for CV tailoring |
| Required skills | Multi-select | Skills extracted from job description |
| Required years | Number | Years of experience requested |
| Fit score | Number | Automated relevance score (0–100) |

---

## Documents & traceability

| Field | Type | Description |
|------|-----|-------------|
| CV Version | Files / URL | Applied CV PDF version |
| Cover Letter | Files / URL | Applied cover letter |
| Motivation text | Text | Generated motivation letter |
| Google Doc Source | URL | Original Google Docs CV used for optimization |

---

## Notes

- PDFs are generated externally (Google Docs → PDF) and linked or attached.
- This schema enables full traceability of each application without exposing personal data.
‚