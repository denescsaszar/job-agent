# System Architecture

This project follows a modular, agent-based architecture.
Each agent has a single responsibility and can be improved independently.

The system is designed to support quality and transparency rather than blind automation.

---

## High-level pipeline

---

## Agents

### Job Search Agent

- Discovers relevant roles from job boards and company career pages
- Normalizes job data into a common structure

### Job Validation Agent

- Uses Playwright to verify that roles are still open
- Detects closed postings, missing apply buttons, or redirects

### Fit Scoring Agent

- Compares job requirements against a personal profile
- Produces a weighted relevance score

### CV & Motivation Generator

- Optimizes CV keywords per role
- Generates role-specific motivation letters
- Maintains consistency with base CV and experience

### Notion Writer

- Persists structured data to the Notion database
- Links CV versions, keywords, and application metadata

### Supervisor / Evaluation Agent

- Monitors pipeline health
- Detects scraping failures and quality degradation
- Tracks metrics and suggests improvements
- Prevents silent regressions

---

## Design principles

- Human-in-the-loop by default
- No blind mass applications
- Privacy-first (personal data stays local)
- Modular and extensible
- Observable and debuggable

┌─────────────┐
│ Job Sources │
│ (LinkedIn, │
│ Career Pages)
└──────┬──────┘
↓
┌─────────────┐
│ Job Search │
│ Agent │
└──────┬──────┘
↓
┌─────────────┐
│ Job │
│ Validation │
│ (Playwright)│
└──────┬──────┘
↓
┌─────────────┐
│ Fit Scoring │
│ Agent │
└──────┬──────┘
↓
┌─────────────┐
│ CV & │
│ Motivation │
│ Generation │
└──────┬──────┘
↓
┌─────────────┐
│ Notion │
│ Database │
│ (Private) │
└──────┬──────┘
↓
┌─────────────┐
│ Supervisor │
│ / Evaluator │
└─────────────┘
