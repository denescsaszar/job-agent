# Job Application Agent

A **product-grade, agent-based system** that automates job discovery, validation, CV optimization, and application tracking — without turning the job search into blind automation.

This project treats job hunting as a **structured decision-making process**, not a numbers game.

---

## ✨ What this project does

Instead of manually searching, tailoring, and tracking applications across multiple platforms, this system:

- discovers relevant job postings from company career pages and job boards
- supports **both static and JavaScript-rendered sites**
- validates whether positions are still open and reachable
- extracts and normalizes job data into a consistent structure
- analyzes job requirements, skills, and keywords
- scores roles based on personal fit
- generates tailored CVs and motivation letters
- tracks every application, document version, and decision in **Notion**

The result is a **single, auditable workflow** where every application is traceable — including:

- which CV version was used
- which keywords were targeted
- why a role was considered a good fit

---

## 🧠 Design philosophy

This project is **intentionally not** a mass-application bot.

It is designed to:

- reduce repetitive work
- improve decision quality
- preserve human control
- make decisions explainable and improvable over time

Automation **supports** judgment — it does not replace it.

---

## 🧩 Architecture overview

The system follows a **modular, agent-based architecture**.

Each agent has a single responsibility and can be evolved independently.

```
Job Sources (Career Pages, Job Boards)
            │
            ▼
     Job Ingestion Agent
   (Static & Dynamic Scraping)
            │
            ▼
     Job Validation Agent
        (Playwright)
            │
            ▼
      Fit Scoring Agent
            │
            ▼
 CV & Motivation Generator
            │
            ▼
     Notion Database
        (Source of Truth)
            │
            ▼
   Supervisor / Evaluator
```

---

## 🧠 Ingestion architecture

Modern career pages behave very differently. This project **explicitly separates ingestion strategies**.

### Static ingestion

- `requests` + `BeautifulSoup`
- Used only for truly static HTML pages

### Dynamic ingestion

- **Playwright**
- Required for JavaScript-rendered sites such as:
  - Stripe
  - Airbnb
  - IBM
  - Greenhouse embeds

Each job source **declares its ingestion mode via config**.

No guessing. No brittle fallbacks.

📄 See: `docs/decisions/ingestion_static_vs_dynamic.md`

---

## 🛠 Tech stack

- **Python**
- **Playwright** (dynamic ingestion & validation)
- **BeautifulSoup** (static parsing)
- **Notion API** (application tracking)
- **Google Docs & Google Drive** (CV optimization & PDF export)
- **LLMs** (CV, motivation, and keyword optimization)

---

## 📊 Notion as the source of truth

All applications are tracked in a structured Notion database, including:

- company & role
- country / location / remote status
- industry and required skills
- extracted & optimized keywords
- fit score
- applied CV & cover letter (PDFs)
- links to original job postings
- application status & timeline

This enables **full transparency**, fast recall during interviews, and long-term learning.

---

## 📋 Notion database schema (private)

The Notion database acts as the private backend for this system. Actual application data is not public, but the schema is documented.

### Core fields

- Company
- Role
- Country
- Location / Remote
- Job URL
- Source
- Status

### Analysis & optimization

- Industry
- Keywords
- Required skills
- Required years of experience
- Fit score

### Documents

- CV version (PDF)
- Cover letter (PDF)
- Google Docs source link

---

## 🚀 Current status

### ✅ Implemented

- Config-driven ingestion architecture
- Static ingestion (requests + BeautifulSoup)
- Dynamic ingestion (Playwright)
- JavaScript-rendered job pages supported
- Stripe careers page ingestion working
- Robust selector handling (explicit skips, no silent failures)
- Notion integration as application source of truth
- Documented architectural decisions

### 🚧 In progress

- Job validation heuristics (closed roles, redirects, apply button checks)
- Normalization of locations and remote status

### ⏭ Planned

- CV optimization via Google Docs
- Motivation letter generation
- Supervisor / evaluation agent
- Application success analytics

---

## 🔒 Security & configuration

Secrets (API keys, tokens) are stored locally in `.env` and are **excluded from version control**.

---

## ⚙️ Setup

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Playwright browsers

```bash
python -m playwright install
```

This step is required for JavaScript-rendered job boards.

---

## 📌 Future extensions

- additional dynamic sources (Airbnb, IBM, Greenhouse)
- job deduplication & historical tracking
- application success analytics
- CV keyword regression testing
- supervisor agent for quality & drift detection
- optional form-filling assistance (human-in-the-loop)

---

## 🧑‍💻 Author

Built as a **real-world automation and product-thinking exercise** to improve the job application process through structure, clarity, and continuous improvement.
