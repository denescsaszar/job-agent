# Job Ingestion Research Log

## Stripe

- Tested multiple Greenhouse URLs:
  - boards.greenhouse.io
  - job-boards.greenhouse.io
  - embed/job_board
- Result: jobs rendered via JavaScript
- Conclusion: requires Playwright

## Airbnb

- WordPress shell, jobs injected dynamically
- No static job cards in initial HTML
- Conclusion: requires Playwright

## Outcome

Static scraping is insufficient for modern job boards.
Dynamic browser-based ingestion is mandatory.
