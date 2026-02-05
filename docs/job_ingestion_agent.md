# Job Ingestion Agent

## Purpose

The Job Ingestion Agent is responsible for discovering relevant job postings
and converting them into structured, normalized data.

It acts as the **entry point** of the job application pipeline.

The agent does not make decisions, score jobs, or generate documents.
Its sole responsibility is **data discovery and normalization**.

---

## Problem Statement

Manual job searching is:

- repetitive
- time-consuming
- inconsistent
- difficult to track historically

Job boards change frequently, roles disappear, and interesting postings are often missed.

The goal of this agent is to:

- reduce manual searching
- provide a consistent stream of fresh job data
- enable downstream automation and analysis

---

## Scope (What the Agent DOES)

The Job Ingestion Agent:

- visits predefined job sources
- extracts job listings
- opens individual job postings
- captures raw job data
- outputs normalized job objects

### Example Output

```json
{
  "position": "Junior Project Manager",
  "company": "IBM",
  "place": "Budapest",
  "country": "Hungary",
  "remote": "Hybrid",
  "posting_url": "https://careers.ibm.com/...",
  "source": "Company career page",
  "raw_description": "Full job description text..."
}
```

## Non-Goals (What the Agent DOES NOT Do)

The agent intentionally does NOT:

- apply to jobs
- fill application forms
- upload CVs
- contact recruiters
- score job relevance
- write to Notion directly

This separation keeps the system:

- safe
- debuggable
- modular
- human-in-the-loop

## Initial Data Sources (MVP)

### Phase 1 — Company Career Pages (Preferred)

**Reasons:**

- stable HTML structure
- no login required
- lower bot detection
- higher signal-to-noise ratio

### Phase 2 — Job Boards (Later)

**Examples:**

- LinkedIn
- Indeed
- Glassdoor

**Constraints:**

- heavier bot protection
- frequent DOM changes
- login requirements

## Technical Design

### Language

- Python

### Libraries

- `requests` / `BeautifulSoup` (static pages)
- `Playwright` (JS-heavy pages)
- `dataclasses` (job objects)
