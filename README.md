# Job Application Agent

An agent-based system that automates job discovery, validation, CV optimization, and application tracking.

This project was built to make job searching more structured, transparent, and scalable — without turning it into blind automation.

---

## ✨ What this project does

Instead of manually searching, tailoring, and tracking applications across multiple platforms, the system:

- discovers relevant job postings across different sources
- validates whether positions are still open and accepting applications
- analyzes job requirements, skills, and keywords
- scores roles based on personal fit
- generates tailored CVs and motivation letters
- tracks every application, document version, and keyword set in Notion

The result is a single, structured workflow where every application is traceable — including **which CV version was used**, **which keywords were targeted**, and **why a role was considered a good fit**.

---

## 🧠 Design philosophy

This is not about fully automated mass-applying.

The system is designed to:

- reduce repetitive work
- improve decision-making
- preserve quality and human control
- make the application process auditable and improvable over time

Automation supports the process — it does not replace judgment.

---

## 🧩 Architecture

The system follows a modular, agent-based pipeline:

Each agent has a single responsibility and can be improved or replaced independently.

---

## 🛠 Tech stack

- **Python**
- **Notion API** (application tracking & metadata)
- **Google Docs & Google Drive** (CV optimization & PDF export)
- **Playwright** (job validation & availability checks)
- **LLMs** (CV, motivation, and keyword optimization)

---

## 📊 Notion as the source of truth

All applications are tracked in a structured Notion database, including:

- company & role
- country / location / remote status
- industry and required skills
- extracted and optimized keywords
- fit score
- applied CV & cover letter (PDF versions)
- links to original job postings
- application status and timeline

This ensures full transparency and fast recall during interviews.

## 📋 Notion Database Schema (Private)

The Notion database acts as the private backend for this system.
Actual application data is not public, but the schema is documented below.

**Core fields**

- Company
- Role
- Country
- Location / Remote
- Job URL
- Source
- Status

**Analysis & optimization**

- Industry
- Keywords
- Required skills
- Required years of experience
- Fit score

**Documents**

- CV version (PDF)
- Cover letter (PDF)
- Google Docs source link

This structure enables full traceability of every application while keeping personal data private.

---

## 🚀 Current status

- [x] Project structure
- [x] Notion integration
- [x] Application tracking schema
- [ ] Job scraping (first source)
- [ ] Job validation with Playwright
- [ ] Google Docs CV optimization
- [ ] Supervisor / evaluation agent

---

## 🔒 Security & configuration

Secrets (API keys, tokens) are stored locally in `.env` and are excluded from version control.

---

## 📌 Future extensions

- automatic CV keyword regression testing
- application success analytics
- supervisor agent for prompt & scoring optimization
- optional form-filling assistance (human-in-the-loop)

---

## 🧑‍💻 Author

Built as a real-world automation and product-thinking exercise to improve the job application process through structure, clarity, and continuous improvement.
