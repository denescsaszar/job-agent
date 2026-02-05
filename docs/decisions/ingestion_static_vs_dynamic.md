# Ingestion: Static vs Dynamic Job Boards

## Context

While building the Job Ingestion Agent, we tested multiple real-world job boards
(Stripe, Airbnb, IBM, Greenhouse embeds).

## Key Finding

Most modern career pages render job listings via JavaScript.
`requests + BeautifulSoup` cannot access these listings.

Examples confirmed as JS-rendered:

- Stripe Careers (including Greenhouse embed)
- Airbnb Careers
- IBM Careers

## Decision

We explicitly separate ingestion paths:

- Static ingestion:
  - requests + BeautifulSoup
  - only for truly static HTML job boards

- Dynamic ingestion:
  - Playwright
  - required for JS-rendered pages

## Rationale

This separation:

- avoids brittle scraping hacks
- prevents silent data loss
- keeps the system debuggable
- reflects real-world web architecture

## Status

Static ingestion path implemented.
Dynamic ingestion path to be implemented via Playwright.
